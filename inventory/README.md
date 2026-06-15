# Inventory Tracker

A simple FastAPI-based inventory management application for tracking spare parts.

Features:
- Web UI using Jinja2 templates
- SQLite storage for part data
- Health check endpoint
- Automatic suggestion for reorder actions using LLM (vLLM) for low-stock items

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn inventory.app:app --reload
   ```

3. Access the UI at `http://localhost:80`.

## Running with Docker

```bash
docker compose up --build
```

The service will be available at `http://localhost:80`.

## Endpoints

- `GET /health` - Health check
- `GET /` - Main inventory view

## LLM Integration

Low-stock items (quantity < 5) trigger a request to the local vLLM API at
`http://127.0.0.1:8000/v1` to suggest reorder actions.