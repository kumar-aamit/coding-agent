# Health appointment app (health-bot branch)

Scaffold only — coding agent should **implement TODOs**, not rewrite structure.

## Stack

- FastAPI + SQLite (`health.db`)
- SQLAlchemy in `database.py`, `models.py`
- Pydantic in `schemas.py`
- App runtime LLM via `llm_client.py` (OpenAI-compatible vLLM)

## App LLM (not OpenCode)

- Base URL: `http://127.0.0.1:8000/v1`
- Model: `nvidia/llama-3.1-nemotron-nano-8b-v1`

Used only by `POST /best-time` and `POST /waiting-time`.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET/POST | `/appointments` | List / create |
| GET/PATCH/DELETE | `/appointments/{id}` | Read / update / delete |
| POST | `/best-time` | LLM suggests best booking time |
| POST | `/waiting-time` | LLM estimates wait |

## Done when

```bash
pip install -r requirements.txt
python -c "import main"
uvicorn main:app --host 0.0.0.0 --port 8080
curl http://127.0.0.1:8080/health
```

No `NotImplementedError` left in implemented paths.
