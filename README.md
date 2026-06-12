# Downtime Ticket Tracker

A FastAPI-based ticket tracker for monitoring machine downtime on the factory floor.

## Tech Stack

- **FastAPI** - Web framework
- **Jinja2** - Templating engine
- **SQLite** - Local database
- **vLLM** - Language model for ticket summary & next steps (http://127.0.0.1:8000/v1)

## Features

- Health check endpoint: `GET /health`
- SQLite-backed ticket storage
- Jinja2 templates for UI
- Integration with vLLM for automated summaries & recommendations

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `uvicorn app.main:app --reload`
3. Access the app at `http://localhost:8000`
4. Use `docker-compose up --build` for containerized deployment

## Usage

- `GET /health` - Health check
- (Additional endpoints will be implemented for ticket creation, summary, and next steps.)

## License

MIT