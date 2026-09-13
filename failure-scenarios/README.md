# Failure scenarios

TaskFlow's healthy branch stays runnable. Each scenario is a small, reversible unified diff that is applied only on a demo branch or inside a disposable clone.

## Reproduce a scenario

```powershell
git switch -c demo/logic-error
git apply failure-scenarios/logic/pending-count.patch
Push-Location backend
pytest -q
Pop-Location
```

The patch is reversible with `git apply -R failure-scenarios/logic/pending-count.patch`. Remove the demo branch when finished:

```powershell
git switch main
git branch -D demo/logic-error
```

Do not apply scenario patches to the healthy branch. Every patch changes a realistic application or configuration mistake, and every `expected_behavior` entry in `scenarios.json` describes the signal an automated repair system should observe.

## Scenario matrix

| Scenario | Category | Validation |
| --- | --- | --- |
| syntax-error | Python syntax | App import or pytest collection |
| import-error | Python import | App import |
| logic-error | Business logic | `pytest -q` |
| test-error | Test expectation | `pytest -q` |
| dependency-error | Package resolution | `pip install -r backend/requirements.txt` |
| frontend-error | Client utility | `npm test` |
| docker-error | Container startup | `docker build` then `docker run` |
| yaml-error | CI configuration | GitHub Actions job |

The patches intentionally do not introduce `raise Exception('demo failure')`; they mimic edits that can occur during ordinary maintenance.
