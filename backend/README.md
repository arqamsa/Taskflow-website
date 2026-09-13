# TaskFlow API

FastAPI backend for TaskFlow. It uses SQLAlchemy models with a SQLite default and accepts any compatible `DATABASE_URL` through environment configuration.

```powershell
python -m pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

The public health endpoint is `GET /health`. Authenticated routes use a bearer JWT returned from the register and login endpoints.
