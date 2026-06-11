---
name: "create-machine-downtime-log"
description: "Initialize Machine Downtime Log repository with FastAPI structure"
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
```

## Core Features
- POST /downtime - Log a downtime event with machine_id, start_time, end_time, reason
- GET /downtime/{machine_id} - Retrieve downtime history for a machine
- POST /query - Send natural language query to vLLM model for analysis
- GET /health - Health check endpoint

## Database Schema
```sql
CREATE TABLE downtime_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## vLLM Integration
- Uses http://localhost:8008/v1/completions endpoint
- Model: nemotron-3-nano
- Sends user queries for downtime analysis

## Docker Configuration
- Base image: python:3.11-slim
- Installs dependencies
- Copies app code
- Exposes port 8000
- Command: uvicorn main:app --host 0.0.0.0 --port 8000

## Environment Variables
- DB_PATH=sqlite:///downtime.db
- LLM_API_URL=http://localhost:8008/v1/completions
- LLM_MODEL=nemotron-3-nano

## Project Files
- `app/main.py`: FastAPI application with endpoints
- `app/models.py`: Pydantic models for request/response
- `app/db.py`: SQLite database utility
- `app/llm.py`: vLLM client wrapper
- `app/requirements.txt`: Python dependencies
- `app/Dockerfile`: Container build definition

## Constraints
1. Application must run on first attempt
2. Must connect to vLLM model on port 8008
3. Must be containerized
4. Must push to https://github.com/kumar-aamit/coding-agent/tree/healthcare
