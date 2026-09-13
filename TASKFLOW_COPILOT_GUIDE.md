# TaskFlow — Copilot Build Guide

**What it is:** Standalone full-stack task/project management app (Trello+Jira+Linear-lite). Serves as the "patient" target repo for a separate Autonomous CI/CD Healing Agent — TaskFlow must NEVER depend on or reference that agent, Hindsight, CascadeFlow, or any AI features.

## Stack
- **Frontend:** React + Vite (JS/TS) + Tailwind + Axios + React Router
- **Backend:** Python + FastAPI + SQLAlchemy + Pydantic + Pytest
- **DB:** PostgreSQL preferred; SQLite fallback for local dev (keep ORM portable)
- **Infra:** Docker (backend + frontend Dockerfiles), docker-compose, GitHub Actions

## Repo Structure
```
TaskFlow/
├── .github/workflows/ (ci.yml, backend-tests.yml, frontend-build.yml, docker-build.yml)
├── .github/ISSUE_TEMPLATE/, pull_request_template.md
├── backend/app/{api,core,database,models,schemas,services}/, main.py
├── backend/tests/ (test_auth, test_projects, test_tasks, test_dashboard, test_health)
├── backend/{requirements.txt, pytest.ini, Dockerfile, README.md}
├── frontend/src/{components,pages,services,hooks,utils}/, App.jsx, main.jsx
├── frontend/tests/, package.json, vite.config.js, Dockerfile, README.md
├── failure-scenarios/{README.md, scenarios.json, syntax/, import/, logic/, dependency/, frontend/, docker/, yaml/, test/}
├── docker-compose.yml, .dockerignore, .gitignore, .env.example, README.md, LICENSE
```

## Core Features
1. **Auth:** register, login, logout, password hashing, protected routes, profile
2. **Projects CRUD:** id, name, description, status, created_at, updated_at, owner_id
3. **Tasks CRUD:** id, title, description, status(TODO/IN_PROGRESS/REVIEW/DONE), priority(LOW/MEDIUM/HIGH/CRITICAL), project_id, assigned_to, due_date, timestamps
4. **Dashboard:** counts (projects, tasks, completed, pending), tasks by status/priority, recent tasks
5. **Kanban board:** 4 columns, simple status-change mechanism (no heavy drag-and-drop needed)
6. **Pages:** /login /register /dashboard /projects /projects/:id /tasks /profile — with sidebar, header, cards, table, loading/error/empty states

## Backend Requirements
- Clean layered architecture: api/ (routes) → services/ → models/ + schemas/
- Proper validation, HTTP status codes, error handling, FK relationships (User→Projects→Tasks, User→Assigned Tasks)
- `GET /health` → `{"status": "healthy"}`, no auth required

## Testing (must be deterministic, no external API calls)
- Backend: auth (register/login/invalid/duplicate), projects CRUD + unauthorized access, tasks CRUD + status/priority validation, dashboard counts, health check
- Frontend: Login component, Dashboard render, Task component, status calc, utils

## Docker & CI
- Backend Dockerfile: Python 3.11, uvicorn start
- Frontend Dockerfile: Node 20+, build + serve
- docker-compose: frontend + backend (+ db if Postgres), env vars only, no hardcoded secrets
- GitHub Actions: separate backend-test / frontend-build / docker-build workflows, triggered on push + PR

## Failure Scenario System (critical — for the healing agent to consume)
- `failure-scenarios/scenarios.json` documents each failure: type, description, target file, expected_behavior
- Types required: SYNTAX, IMPORT, LOGIC, TEST, DEPENDENCY, DOCKER, CI_CONFIGURATION(yaml), FRONTEND
- Failures must be **realistic** (wrong function names, inverted logic, bad imports, dependency mismatches, broken Docker paths, bad CI commands) — never a fake `raise Exception("demo failure")`
- Each failure must be isolated, reversible, and reproducible via dedicated branches (e.g. `demo/logic-error`) or documented patch scripts — **main branch must always stay healthy**

## Hard Constraints
- ❌ No healing-agent code, Hindsight, CascadeFlow, or AI features inside TaskFlow
- ❌ No hardcoded secrets — use `.env.example`
- ❌ No TODO placeholders on core functionality, no dead/fake code
- ❌ README must NOT mention hackathon/RIFT/judging language — treat as a standalone portfolio app

## Workflow for Copilot
1. Inspect existing repo state first — don't blindly overwrite.
2. Implement backend → run `pytest` → implement frontend → `npm run build` → Docker build → verify `/health` and end-to-end connectivity → validate GitHub Actions YAML → verify each failure scenario reproduces and is reversible.
3. Deliver a final report: architecture, files changed, test results, build results, Docker results, known issues, next steps — only claim something works if actually tested.

## Acceptance Checklist (condensed)
Frontend/backend/db run · auth + CRUD (projects/tasks) work · dashboard + kanban work · backend & frontend tests pass · frontend build passes · both Docker images build · compose config valid · `/health` works · all 4 CI workflows present & passing · `.env.example` present, no secrets committed · all 8 failure types documented & reproducible · main branch stays healthy · README complete.
