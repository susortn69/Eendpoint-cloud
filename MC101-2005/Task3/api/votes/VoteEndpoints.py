from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.candidates.CandidateDBModels import Candidate
from api.users.UserDBModels import User
from api.votes.VoteDBModels import Vote
from utils.constants import Endpoints, ResponseMessages
from utils.database import get_db
from utils.security import ensure_active_user
from .VoteSchemas import VoteCreateSchema


VoteRouter = APIRouter(prefix="/users", tags=["Votes"])


@VoteRouter.post(Endpoints.USER_VOTE, status_code=status.HTTP_201_CREATED)
def cast_vote(
    vote: VoteCreateSchema,
    current_user: User = Depends(ensure_active_user),
    db: Session = Depends(get_db),
):
    current_user = db.merge(current_user)

    candidate = db.get(Candidate, vote.candidate_id)
    if candidate is None or not candidate.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseMessages.CANDIDATE_NOT_FOUND,
        )

    existing_vote = db.query(Vote).filter(Vote.user_id == current_user.id).first()
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseMessages.VOTE_ALREADY_CAST,
        )

    new_vote = Vote(user_id=current_user.id, candidate_id=candidate.id)
    db.add(new_vote)
    db.commit()

    return {
        "message": ResponseMessages.VOTE_RECORDED,
        "candidate": {
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
        },
    }
