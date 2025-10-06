# Task 4 – Postman Test Suite

This task verifies the Task 3 API using an automated Postman collection and runner.

## Deliverables
1. Postman collection JSON export (all endpoints from Task 3).
2. Postman environment JSON export (contains variables such as ase_url, dmin_token, user_email, etc.).
3. Runner results JSON export (evidence that the test set was executed).

Import these JSON files to Canvas once generated.

## Suggested Structure
Organise a Postman **Collection** with folders like:
- Users
  - Register user
  - Login user
  - Update user
  - Get user info
  - Delete user
- Admin
  - Create candidate
  - List candidates
  - Get candidate
  - Update candidate
  - Delete candidate
- Votes
  - Cast vote
- Health
  - Health check

## Environment Variables
Create a Postman **Environment** with at least:
- ase_url ? http://localhost:8000
- dmin_token ? super-secret-admin-token
- andom_email ? set in pre-request script using pm.variables.replaceIn('test+{{randomInt}}@example.com')
- uth_token ? populated after login response (pm.environment.set('auth_token', json.access_token))
- candidate_id ? set after candidate creation (pm.environment.set('candidate_id', json.candidate.id))
- user_id (optional) ? if you return it in login response, capture for updates/deletes.

## Pre-request / Test Scripts
Each request should have:
- A **pre-request script** (when needed) to seed random values.
- A **test script** to assert at minimum the status code. Example:
`js
pm.test('Status code is 201', function () {
  pm.response.to.have.status(201);
});
`
Enrich with payload assertions, e.g.:
`js
const json = pm.response.json();
pm.test('Candidate id stored', function () {
  pm.expect(json.candidate.id).to.be.a('number');
  pm.environment.set('candidate_id', json.candidate.id);
});
`

## Runner Execution
1. Start Task 3 Docker stack: cd Task3 && docker compose up -d.
2. In Postman, choose the Task 4 collection ? Run.
3. Select the environment created above, ensure iterations: 1 (or more if desired).
4. After the runner completes, click View Report ? three dots ? Export Results ? JSON.
5. Stop services with docker compose down when done.

## Repository Usage
Place exported JSON files under this folder before submission (e.g. Task4/postman_collection.json, Task4/postman_environment.json, Task4/postman_runner_results.json). Update .gitignore if you want to exclude originals after uploading to Canvas.

## Tips
- Use the Postman Snippets panel for common test assertions.
- Remember Task 3 tokens expire after one minute, so refresh user login before vote/delete steps by adding another login request in the collection sequence.
- Validate negative cases (e.g. duplicate vote) via additional requests if time allows.
