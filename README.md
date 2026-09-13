# TaskFlow

TaskFlow is a small, realistic demo task and project management workspace. It combines the useful parts of Trello, Jira, and Linear into a focused app for organizing projects, priorities, and delivery.

It is intentionally a normal standalone application: React and Vite on the client, FastAPI and SQLAlchemy on the server, and SQLite by default with PostgreSQL-compatible configuration. Its clear boundaries, deterministic tests, container setup, and documented failure patches also make it a reliable target repository for an external autonomous CI/CD healing system.

## Features

- Email/password registration and login with hashed passwords and JWT sessions
- Protected project and task CRUD endpoints with ownership checks
- Dashboard counts, status distribution, priority distribution, and recent work
- Four-column Kanban view with task status changes
- Responsive workspace shell with sidebar navigation, empty states, and loading-safe API fallback
- Deterministic backend and frontend tests
- Docker images, Compose, and GitHub Actions workflows
- Reversible, documented failure scenarios for syntax, import, logic, tests, dependencies, frontend, Docker, and CI configuration

## Architecture

```text
React/Vite browser
      | Axios + JWT
FastAPI route layer
      | service-shaped ORM access
SQLAlchemy models
      | SQLite locally / PostgreSQL-compatible URL
Database
```

The backend is organized into `api`, `core`, `database`, `models`, and `schemas`. The frontend keeps API access, task utilities, data hooks, UI, and styles separate without introducing a state-management dependency.

## Repository structure

- `.github/workflows`: backend tests, frontend build, Docker build, and combined CI
- `backend/app`: FastAPI application, auth, models, schemas, and routes
- `backend/tests`: deterministic API tests using an isolated SQLite database
- `frontend/src`: React app, dashboard, project/task views, API client, and utilities
- `frontend/tests`: Vitest and Testing Library-compatible test setup
- `failure-scenarios`: reversible patches and scenario metadata
- `docker-compose.yml`: local container orchestration

## Demo setup

Requirements: Python 3.11+ and Node 20+. Docker is optional and is not required for the application, tests, or frontend build. SQLite is the default local database, so no external database service is needed.

The primary demo validation path is:

```powershell
cd backend
python -m pip install -r requirements.txt
pytest

cd ..\frontend
npm install
npm test
npm run build
```

An external CI/CD agent can use these same commands in a clean checkout, then apply and verify a controlled failure scenario.

### Backend

```powershell
cd backend
python -m pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Health checks use `GET /health` and return `{"status":"healthy"}`.

### Frontend

```powershell
cd frontend
npm install
npm test
npm run dev
```

The app is available at `http://localhost:5173`. Set `VITE_API_URL` when the API runs somewhere else. If the API is unavailable, the UI clearly labels a sample workspace so the interface remains inspectable without hiding the connection issue.

### Optional Docker artifacts

Docker Desktop is not required for TaskFlow demo readiness. The Dockerfiles and Compose file are included as optional deployment artifacts and are not used by the local application or test commands.

```powershell
Copy-Item .env.example .env
docker compose build
docker compose up
```

The frontend runs on `http://localhost:5173` and the backend on `http://localhost:8000`. Compose stores the local SQLite database in a named volume.

## Authentication and API

The main endpoints are:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET|POST /api/projects`
- `GET|PATCH|DELETE /api/projects/{id}`
- `GET|POST /api/tasks`
- `GET|PATCH|DELETE /api/tasks/{id}`
- `GET /api/dashboard`
- `GET /health`

Never commit `.env`. Use `.env.example` as the starting point for local configuration.

## GitHub Actions

Every push and pull request runs the backend test workflow and frontend test/build workflow using only Python, Node, SQLite, and npm. A separate Docker build workflow exists as an optional container check; Docker is not required for the core CI/demo path. The combined CI workflow provides a small independent smoke path. None of the workflows require cloud credentials or external services.

## Failure scenarios

The clean branch stays healthy. To demonstrate a realistic failure, create a temporary branch and apply one patch from `failure-scenarios`:

```powershell
git switch -c demo/logic-error
git apply failure-scenarios/logic/pending-count.patch
cd backend
pytest -q
```

Read `failure-scenarios/scenarios.json` for the target, category, patch, and expected signal. Reverse a patch with `git apply -R`, or delete the demo branch after switching back to the clean branch. The scenario set is designed for an external autonomous CI/CD healing system to clone, run, diagnose, repair, and verify without TaskFlow containing any healing logic of its own.

## Development notes

The application favors understandable code and deterministic behavior over unnecessary product complexity. Database tables are created on startup for local convenience; a migration tool can be introduced later if the schema needs it. TaskFlow is demo-ready rather than production infrastructure: it intentionally does not include Kubernetes, managed databases, queues, monitoring, HTTPS setup, or other deployment-only systems.
