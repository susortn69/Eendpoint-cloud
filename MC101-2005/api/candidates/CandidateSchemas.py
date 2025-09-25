from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CandidateCreateSchema(BaseModel):
    name: str
    manifesto: Optional[str] = None
    is_active: bool = True


class CandidatePublicSchema(BaseModel):
    id: int
    name: str
    manifesto: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True
