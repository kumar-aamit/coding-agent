---
name: "create-field-service-ticket-tracker"
description: "Initialize field-service-ticket-tracker repository with basic structure"
---

# Field Service Ticket Tracker

A Python application that simulates a field service ticket tracking system for utilities and telecom. It includes ticket management, technician dispatch, SLA breach detection, and Docker containerization.

## Project Structure
```
field-service-ticket-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── main.py
├── tests/
│   └── test_services.py
├── docker/
│   └── Dockerfile
├── requirements.txt
├── README.md
└── .dockerignore
```

## Core Features
- Ticket creation with auto-assignment based on location and priority
- Technician dispatch algorithm
- SLA breach detection with visual indicators
- SQLite database storage
- Docker containerization

## Requirements
- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Docker Configuration
- Base image: python:3.11-slim
- Installs dependencies
- Copies app code
- Exposes port 8000
- Command: uvicorn app.main:app --host 0.0.0.0 --port 8000

## Environment Variables
- DB_PATH=sqlite:///tickets.db
- LOG_LEVEL=INFO

## Project Files
- `app/models.py`: Pydantic models for ticket data
- `app/services.py`: Core business logic for ticket management
- `app/main.py`: FastAPI application entry point
- `docker/Dockerfile`: Container build definition
- `requirements.txt`: Python dependencies
- `README.md`: Documentation
- `.dockerignore`: Build context exclusion rules
