from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class CandidateDBModel(BaseModel):
    id: int = 0
    name: str
    manifesto: Optional[str] = None
    is_active: bool = True


CandidatesDB: Dict[int, CandidateDBModel] = {}


def get_candidates_db() -> Dict[int, CandidateDBModel]:
    """Return the in-memory candidate store."""
    global CandidatesDB
    return CandidatesDB


def get_next_candidate_id() -> int:
    """Compute the next candidate identifier."""
    candidates = get_candidates_db()
    if candidates:
        return max(candidates.keys()) + 1
    return 1


def list_candidates() -> List[CandidateDBModel]:
    """Return all persisted candidates."""
    return list(get_candidates_db().values())


def get_candidate_by_id(candidate_id: int) -> Optional[CandidateDBModel]:
    """Return a candidate by identifier if it exists."""
    return get_candidates_db().get(candidate_id)


def get_candidate_by_name(name: str) -> Optional[CandidateDBModel]:
    """Return a candidate by name (case insensitive)."""
    for candidate in list_candidates():
        if candidate.name.lower() == name.lower():
            return candidate
    return None


def add_candidate(candidate: CandidateDBModel) -> CandidateDBModel:
    """Persist a candidate in the in-memory store."""
    candidates = get_candidates_db()
    candidate.id = get_next_candidate_id()
    candidates[candidate.id] = candidate
    return candidate
