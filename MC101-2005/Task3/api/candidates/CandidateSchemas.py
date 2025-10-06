from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CandidateCreateSchema(BaseModel):
    name: str
    manifesto: Optional[str] = None
    is_active: bool = True


class CandidateUpdateSchema(BaseModel):
    name: Optional[str] = None
    manifesto: Optional[str] = None
    is_active: Optional[bool] = None


class CandidatePublicSchema(BaseModel):
    id: int
    name: str
    manifesto: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class CandidateVoteCountSchema(CandidatePublicSchema):
    total_votes: int = 0
