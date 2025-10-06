# Task 2 – Logging & Containerization

Builds on the Task 1 authentication API by adding structured logging and Docker Compose tooling.

## Highlights
- Logs INFO+ events to `logs/logs.log` (mounted from the host when running via Compose)
- Dockerfile targeting Python 3.11 slim image
- `docker-compose.yml` to build/run the FastAPI app with the shared logs volume

## Requirements
- Docker Desktop with Compose plugin
- (Optional) Python 3.11 + Poetry if you want to run without Docker

## Running with Docker Compose

### Build the image
`docker compose build`

### Start the app (detached)
`docker compose up -d`

### Stop and clean up
`docker compose down`

## Running locally (without Docker)
1. `poetry install`
2. Copy `example.env.txt` to `.env` and set secrets
3. `poetry run uvicorn main:voting_app --reload`
