# Shift Handoff Log

A FastAPI + Jinja2 application for logging shift handoff details (Shift A/B/C, operator, notes, open issues). Uses SQLite for storage and a vLLM endpoint to summarize open issues.

## Features

- Record shift handoff logs for shifts A, B, C
- Capture operator name and shift notes
- Maintain a list of open issues
- Summarize open issues using vLLM at `http://127.0.0.1:8000/v1`

## Running the App

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
uvicorn app.main:app --reload
```

3. Open `http://127.0.0.1:8000` in a browser.

## Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8000`.

## Health Check

The service provides a `GET /health` endpoint that returns `OK`.

## Configuration

- The vLLM summarization endpoint URL can be configured via environment variable `VLLM_ENDPOINT`.

## License

MIT