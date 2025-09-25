from fastapi import FastAPI, status
import uvicorn

from api.candidates.CandidateEndpoints import CandidateRouter
from api.users.UserEndpoints import UserRouter
from api.votes.VoteEndpoints import VoteRouter
from utils.constants import Endpoints, ResponseMessages

voting_app = FastAPI(
    title="Voting App",
    description="A simple voting application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

voting_app.include_router(UserRouter)
voting_app.include_router(CandidateRouter)
voting_app.include_router(VoteRouter)


@voting_app.get(Endpoints.ROOT)
def read_root():
    """A docstring describing the root endpoint"""
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}


@voting_app.get(Endpoints.HEALTH)
def read_health():
    return {"message": ResponseMessages.HEALTH_OK, "status": status.HTTP_200_OK}


if __name__ == "__main__":
    uvicorn.run("main:voting_app", host="0.0.0.0", port=8000, reload=True)
