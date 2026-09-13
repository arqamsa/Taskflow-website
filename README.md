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

## Demo deployment: Render + Vercel

The simplest hosted demo uses Render for the FastAPI backend and Vercel for the Vite frontend. Docker is not required.

### Deploy the backend to Render

Create a Render **Web Service** connected to this repository with:

- Root directory: `backend`
- Runtime: `Python 3`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

The repository also includes `render.yaml` with these settings. You can use Render's Blueprint flow to apply them automatically. `backend/runtime.txt` pins the service to Python 3.11, which avoids source builds for older dependency versions on Python 3.14.

Add these environment variables in Render:

```text
DATABASE_URL=sqlite:///./taskflow.db
SECRET_KEY=<a-long-random-value>
FRONTEND_URL=https://<your-vercel-domain>
```

After deployment, verify `https://<your-render-service>.onrender.com/health` returns `{"status":"healthy"}`. Copy this Render URL for the frontend API variable.

### Deploy the frontend to Vercel

Import the same repository into Vercel and set:

- Root directory: `frontend`
- Framework preset: `Vite`
- Build command: `npm run build`
- Output directory: `dist`

Add this Vercel environment variable before deploying:

```text
VITE_API_URL=https://<your-render-service>.onrender.com/api
```

The `frontend/vercel.json` rewrite keeps React Router routes such as `/projects` and `/profile` working when opened directly.

### Important demo limitation

The default SQLite database is suitable for this demo and requires no external service, but Render's local filesystem may be reset when a service is redeployed or restarted. This can remove registered users and task data. That is acceptable for the TaskFlow patient/demo scope; use a persistent database only if durable hosted data becomes a requirement.

### Hosted smoke test

1. Open the Render `/health` endpoint.
2. Open the Vercel URL and register a user.
3. Create a project and task.
4. Move the task across Kanban statuses.
5. Refresh `/dashboard` and `/projects` to verify the API URL and CORS configuration.

### Render dependency mismatch troubleshooting

The backend requirements for TaskFlow contain only FastAPI, SQLAlchemy, JWT/password security, and test packages. If Render logs mention packages such as `e2b`, `openai`, `groq`, or `psycopg2`, Render is not building this TaskFlow commit. Check that the service repository is `chetankumar-rs/Taskflow-website`, branch is `main`, and root directory is `backend`. Then trigger **Clear build cache & deploy**. The expected first install line is `fastapi==0.115.6` from `backend/requirements.txt`.

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
