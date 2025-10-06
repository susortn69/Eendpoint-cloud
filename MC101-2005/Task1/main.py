from fastapi import FastAPI, status
import uvicorn

from api.users.UserEndpoints import UserRouter
from utils.constants import Endpoints, ResponseMessages

voting_app = FastAPI(
    title="Voting App",
    description="Authentication service for the voting system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

voting_app.include_router(UserRouter)


@voting_app.get(Endpoints.ROOT)
def read_root():
    """Basic welcome endpoint."""
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}


@voting_app.get(Endpoints.HEALTH)
def read_health():
    return {"message": ResponseMessages.HEALTH_OK, "status": status.HTTP_200_OK}


if __name__ == "__main__":
    uvicorn.run("main:voting_app", host="0.0.0.0", port=8000, reload=True)
