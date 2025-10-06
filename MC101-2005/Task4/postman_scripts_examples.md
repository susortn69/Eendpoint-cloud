# Postman Script Examples

## Random email pre-request
`js
const randomValue = Math.floor(Math.random() * 100000);
pm.environment.set('random_email', 	ester_@example.com);
`
Use {{random_email}} in the registration payload.

## Login test script
`js
pm.test('Login succeeded', function () {
  pm.response.to.have.status(200);
});
const json = pm.response.json();
pm.environment.set('auth_token', json.access_token);
pm.environment.set('token_expiry', Date.now() + 50 * 1000); // refresh after 50s
`

## Candidate creation test
`js
pm.test('Candidate created', function () {
  pm.response.to.have.status(201);
});
const json = pm.response.json();
pm.environment.set('candidate_id', json.candidate.id);
pm.expect(json.candidate.name).to.eql(pm.variables.get('candidate_name'));
`

## Vote test
`js
pm.test('Vote accepted', function () {
  pm.response.to.have.status(201);
});
const json = pm.response.json();
pm.expect(json.candidate.candidate_id).to.eql(Number(pm.environment.get('candidate_id')));
`

## Health check test
`js
pm.test('Health OK', function () {
  pm.response.to.have.status(200);
});
pm.expect(pm.response.json().message).to.eql('The service is up and running!');
`

Add or adapt these snippets per request.
