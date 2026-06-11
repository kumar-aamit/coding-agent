---
name: "create-clinic-wait-times"
description: "Create clinic wait times AI board app"
---

We need to scaffold a full-stack app for clinic wait times using FastAPI or Flask, with real-time UI showing queue metrics. Requirements include:

- Backend in FastAPI or Flask (Python 3.11+) that manages patient check-in, timestamps, queue ordering, wait time calculations
- Real-time dashboard showing current average wait time and flagging the longest-waiting patient
- Patient check-in form (web) with name and optional reason
- Backend stores timestamps and computes wait times, maintains ordered queue
- Dashboard updates in real time when patients are checked in or marked "seen", using SSE or WebSocket
- Include Dockerfile, docker-compose.yml, requirements.txt, README with run instructions
- Include pytest tests for wait time calculation and queue ordering
- Include GitHub Actions CI workflow (.github/workflows/ci.yml) for test+docker build
- Simple deployable stack

We will create a directory clinic-wait-times with the following structure:
clinic-wait-times/
├─ src/
│  ├─ __init__.py
│  ├─ main.py (FastAPI app)
│  ├─ models.py (Pydantic models)
│  ├─ schemas.py (request/response schemas)
│  ├─ queue.py (queue management logic)
│  └─ database.py (if needed)
├─ templates/
│  └─ index.html (dashboard)
├─ static/
│  └─ script.js (client-side logic for SSE/WebSocket)
├─ tests/
│  └─ test_queue.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .github/
│  └─ workflows/
│    └─ ci.yml
└─ README.md

We'll implement queue logic maintaining patient entries with timestamp, name, reason, and computed wait time. Dashboard will show average wait time, longest-waiting patient, and live updates via Server-Sent Events (SSE) as it's simpler to implement in FastAPI.

The backend will expose:
- GET /queue - returns current queue with patients and computed wait times
- POST /check-in - receives patient name and optional reason, adds to queue
- POST /seen/{patient_id} - marks patient as seen, removes from queue
- GET /updates (SSE) - streams updates to dashboard

We'll store queue in memory for simplicity (reset on restart). In production, this could be Redis or DB.

Test cases will verify:
- Wait time calculation correctly reflects time differences
- Queue ordering respects insertion order and removal
- Longest-waiting patient is correctly identified

CI workflow will:
- Install dependencies
- Run pytest
- Lint code (if configured)
- Build Docker image

This approach keeps the implementation lightweight while meeting all functional requirements.
