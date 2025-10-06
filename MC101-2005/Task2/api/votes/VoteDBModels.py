from __future__ import annotations

from collections import Counter
from typing import Dict


# user_id -> candidate_id
VotesDB: Dict[int, int] = {}


def get_votes_db() -> Dict[int, int]:
    """Return the in-memory vote store."""
    global VotesDB
    return VotesDB


def has_user_voted(user_id: int) -> bool:
    """Check whether a user has already cast a vote."""
    return user_id in get_votes_db()


def add_vote(user_id: int, candidate_id: int) -> None:
    """Persist the vote in the in-memory store."""
    votes = get_votes_db()
    votes[user_id] = candidate_id


def get_vote_totals() -> Dict[int, int]:
    """Aggregate vote totals per candidate."""
    votes = get_votes_db()
    return dict(Counter(votes.values()))
