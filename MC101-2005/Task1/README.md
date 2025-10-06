# Task 1 – Authentication API

FastAPI service that handles user registration, login, profile lookup, and self-delete for the voting system. Tokens expire after 1 minute as required.

## Requirements
- Python 3.11+
- Poetry 1.8+

## Getting started
1. `poetry install`
2. Copy `example.env.txt` to `.env` and fill in the JWT secrets (sample already provided)
3. `poetry run uvicorn main:voting_app --reload`

## Endpoints
- `POST /users/register`
- `POST /users/login`
- `GET /users/info`
- `DELETE /users/delete`
- `GET /` & `GET /health` for simple checks
