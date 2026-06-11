---
name: "machine-downtime-log-final"
description: "Finalize Machine Downtime Log repository"
---

# Machine Downtime Log

A FastAPI web service that tracks machine stoppages and integrates with a vLLM model running on port 8008 for natural language query support.

## Project Structure
```
/app
  ├── main.py          # FastAPI entry point
  ├── models.py        # Pydantic models
  ├── db.py            # SQLite DB connection
  ├── llm.py           # vLLM client wrapper
  ├── requirements.txt
  └── Dockerfile
