# Task 3 – Database & Admin Controls

Extends the voting API by persisting data in Postgres, introducing admin-managed candidates, and exposing vote operations with proper authentication.

## What's new
- SQLAlchemy models backed by a Postgres service (via Docker Compose)
- JWT-protected user update and voting endpoints (/users/, /users/vote)
- Admin-only candidate management with token header X-Admin-Token
- Health check verifies database connectivity and logs still persist to logs/logs.log

## Environment variables
Copy example.env.txt to .env and fill in:
- JWT_SECRET_KEY – secret for tokens
- DATABASE_URL – defaults to the in-cluster Postgres DSN
- ADMIN_API_TOKEN – token the admin must send in the X-Admin-Token header

## Run with Docker Compose
`
cd Task3
docker compose build
docker compose up -d
`
This starts both the API (http://localhost:8000) and Postgres (localhost:5432). Logs are written to Task3/logs/logs.log on the host.

Stop everything with:
`
docker compose down
`

## Run locally without Docker
`
cd Task3
poetry install
poetry run uvicorn main:voting_app --reload
`

## Key endpoints
- POST /users/register – create user
- POST /users/login – JWT login
- PATCH /users/ – update profile (needs bearer token)
- POST /users/vote – vote for a candidate (needs bearer token)
- POST|PATCH|DELETE /admin/candidate – admin CRUD (requires X-Admin-Token)
- GET /admin/candidate – list candidates with vote counts
- GET /admin/candidate/{id} – get vote count for a candidate
- GET /health – application + database health
