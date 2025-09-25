from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


class VoteCreateSchema(BaseModel):
    candidate_id: int


class VoteResultSchema(BaseModel):
    candidate_id: int
    candidate_name: str
    total_votes: int


class VoteResultsResponseSchema(BaseModel):
    totals: Dict[int, VoteResultSchema]
