from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.candidates.CandidateDBModels import Candidate
from api.votes.VoteDBModels import Vote
from utils.constants import Endpoints, ResponseMessages
from utils.database import get_db
from utils.security import require_admin
from .CandidateSchemas import (
    CandidateCreateSchema,
    CandidatePublicSchema,
    CandidateUpdateSchema,
    CandidateVoteCountSchema,
)


CandidateRouter = APIRouter(prefix="/admin/candidate", tags=["Admin Candidates"])


@CandidateRouter.post(Endpoints.ADMIN_CANDIDATES, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_candidate(candidate: CandidateCreateSchema, db: Session = Depends(get_db)):
    existing = (
        db.query(Candidate)
        .filter(func.lower(Candidate.name) == candidate.name.lower())
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseMessages.CANDIDATE_ALREADY_EXISTS,
        )

    new_candidate = Candidate(
        name=candidate.name,
        manifesto=candidate.manifesto,
        is_active=candidate.is_active,
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return {
        "message": ResponseMessages.CANDIDATE_CREATED,
        "candidate": CandidatePublicSchema.model_validate(new_candidate),
    }


@CandidateRouter.patch(Endpoints.ADMIN_CANDIDATE_DETAIL, dependencies=[Depends(require_admin)])
def update_candidate(
    candidate_id: int,
    update: CandidateUpdateSchema,
    db: Session = Depends(get_db),
):
    candidate = db.get(Candidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessages.CANDIDATE_NOT_FOUND)

    if update.name and update.name.lower() != candidate.name.lower():
        exists = (
            db.query(Candidate)
            .filter(func.lower(Candidate.name) == update.name.lower(), Candidate.id != candidate_id)
            .first()
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.CANDIDATE_ALREADY_EXISTS)
        candidate.name = update.name

    if update.manifesto is not None:
        candidate.manifesto = update.manifesto

    if update.is_active is not None:
        candidate.is_active = update.is_active

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "message": ResponseMessages.CANDIDATE_UPDATED,
        "candidate": CandidatePublicSchema.model_validate(candidate),
    }


@CandidateRouter.delete(Endpoints.ADMIN_CANDIDATE_DETAIL, dependencies=[Depends(require_admin)])
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.get(Candidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessages.CANDIDATE_NOT_FOUND)

    db.delete(candidate)
    db.commit()

    return {"message": ResponseMessages.CANDIDATE_DELETED}


@CandidateRouter.get(Endpoints.ADMIN_CANDIDATES)
def list_candidates(db: Session = Depends(get_db)):
    rows = (
        db.query(Candidate, func.count(Vote.id).label("total_votes"))
        .outerjoin(Vote, Candidate.id == Vote.candidate_id)
        .group_by(Candidate.id)
        .order_by(Candidate.id)
        .all()
    )

    candidates = [
        CandidateVoteCountSchema(
            **CandidatePublicSchema.model_validate(candidate).model_dump(),
            total_votes=total_votes,
        )
        for candidate, total_votes in rows
    ]

    return {
        "message": ResponseMessages.CANDIDATES_LIST,
        "candidates": candidates,
    }


@CandidateRouter.get(Endpoints.ADMIN_CANDIDATE_DETAIL)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(Candidate, func.count(Vote.id).label("total_votes"))
        .outerjoin(Vote, Candidate.id == Vote.candidate_id)
        .filter(Candidate.id == candidate_id)
        .group_by(Candidate.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessages.CANDIDATE_NOT_FOUND)

    candidate, total_votes = row
    payload = CandidateVoteCountSchema(
        **CandidatePublicSchema.model_validate(candidate).model_dump(),
        total_votes=total_votes,
    )
    return {
        "message": ResponseMessages.CANDIDATE_FOUND,
        "candidate": payload,
    }
