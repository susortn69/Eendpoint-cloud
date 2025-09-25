from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from utils.constants import Endpoints, ResponseMessages
from utils.security import decode_access_token

from .CandidateDBModels import (
    CandidateDBModel,
    add_candidate,
    get_candidate_by_id,
    get_candidate_by_name,
    list_candidates,
)
from .CandidateSchemas import CandidateCreateSchema, CandidatePublicSchema


CandidateRouter = APIRouter(prefix="/candidates", tags=["Candidates"])


@CandidateRouter.post(Endpoints.CANDIDATES, status_code=status.HTTP_201_CREATED)
def create_candidate(
    candidate: CandidateCreateSchema,
    payload: dict = Depends(decode_access_token),
):
    """Register a new candidate. Authentication required."""
    if get_candidate_by_name(candidate.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseMessages.CANDIDATE_ALREADY_EXISTS,
        )

    new_candidate = add_candidate(CandidateDBModel(**candidate.model_dump()))

    return {
        "message": ResponseMessages.CANDIDATE_CREATED,
        "candidate": CandidatePublicSchema(**new_candidate.model_dump()).model_dump(),
    }


@CandidateRouter.get(Endpoints.CANDIDATES, status_code=status.HTTP_200_OK)
def read_candidates():
    """Return the list of registered candidates."""
    candidates = [
        CandidatePublicSchema(**candidate.model_dump()).model_dump()
        for candidate in list_candidates()
        if candidate.is_active
    ]

    return {
        "message": ResponseMessages.CANDIDATES_LIST,
        "candidates": candidates,
    }


@CandidateRouter.get(Endpoints.CANDIDATE_DETAIL, status_code=status.HTTP_200_OK)
def read_candidate(candidate_id: int):
    """Return a single candidate if it exists."""
    candidate = get_candidate_by_id(candidate_id)
    if candidate is None or not candidate.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseMessages.CANDIDATE_NOT_FOUND,
        )

    return {
        "message": ResponseMessages.CANDIDATE_FOUND,
        "candidate": CandidatePublicSchema(**candidate.model_dump()).model_dump(),
    }
