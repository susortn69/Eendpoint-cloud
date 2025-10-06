from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from api.candidates.CandidateDBModels import get_candidate_by_id
from api.users.UserDBModels import get_user_by_email
from utils.constants import Endpoints, ResponseMessages
from utils.security import decode_access_token

from .VoteDBModels import add_vote, get_vote_totals, has_user_voted
from .VoteSchemas import VoteCreateSchema


VoteRouter = APIRouter(prefix="/votes", tags=["Votes"])


@VoteRouter.post(Endpoints.VOTES, status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteCreateSchema, payload: dict = Depends(decode_access_token)):
    """Cast a vote for a candidate. Authentication required."""
    user_id = payload.get("user_id")
    email = payload.get("email")

    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseMessages.INVALID_TOKEN,
        )

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseMessages.USER_NOT_FOUND,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ResponseMessages.USER_INACTIVE,
        )

    if has_user_voted(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseMessages.VOTE_ALREADY_CAST,
        )

    candidate = get_candidate_by_id(vote.candidate_id)
    if candidate is None or not candidate.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResponseMessages.CANDIDATE_NOT_FOUND,
        )

    add_vote(user_id=user_id, candidate_id=candidate.id)

    return {
        "message": ResponseMessages.VOTE_RECORDED,
        "candidate": {
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
        },
    }


@VoteRouter.get(Endpoints.VOTE_RESULTS, status_code=status.HTTP_200_OK)
def read_vote_results():
    """Return aggregate vote results."""
    totals = get_vote_totals()
    if not totals:
        return {
            "message": ResponseMessages.NO_VOTES_RECORDED,
            "results": [],
        }

    results = []
    for candidate_id, total_votes in totals.items():
        candidate = get_candidate_by_id(candidate_id)
        candidate_name = candidate.name if candidate else ResponseMessages.CANDIDATE_NOT_FOUND
        results.append(
            {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "total_votes": total_votes,
            }
        )

    return {
        "message": ResponseMessages.VOTE_RESULTS,
        "results": results,
    }
