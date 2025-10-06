import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text

from api.candidates.CandidateEndpoints import CandidateRouter
from api.users.UserEndpoints import UserRouter
from api.votes.VoteEndpoints import VoteRouter
from utils.constants import Endpoints, ResponseMessages
from utils.database import Base, SessionLocal, engine

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "logs.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

voting_app = FastAPI(
    title="Voting App",
    description="Voting system API with authentication and admin tooling",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

voting_app.include_router(UserRouter)
voting_app.include_router(CandidateRouter)
voting_app.include_router(VoteRouter)


@voting_app.on_event("startup")
async def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Voting app startup complete")


@voting_app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Voting app shutting down")


@voting_app.get(Endpoints.ROOT)
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}


@voting_app.get(Endpoints.HEALTH)
def read_health():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - health failures are unexpected
        logger.exception("Health check failed: %s", exc)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection failed") from exc

    logger.info("Health endpoint accessed")
    return {"message": ResponseMessages.HEALTH_OK, "status": status.HTTP_200_OK}


if __name__ == "__main__":
    logger.info("Starting Uvicorn server")
    uvicorn.run("main:voting_app", host="0.0.0.0", port=8000, reload=True)
