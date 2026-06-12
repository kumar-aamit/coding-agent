# Machine Downtime Log

A field services ticket tracker for manufacturing floor machine stoppages. This application allows operators to log downtime events and automatically generates summaries using a local vLLM model.

## Features

- Log machine stoppages with machine ID, line/area, reason, description, severity, and operator
- Automatic AI-powered summaries using local vLLM model
- Status tracking (open/in-progress/resolved) with resolution notes
- Search and filter capabilities
- Docker containerization for easy deployment

## Prerequisites

- Docker and Docker Compose
- A running vLLM model on port 8000 (accessible at http://localhost:8000/v1)
- Python 3.11+ (for development)

## Setup

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Access the application at http://localhost:8080

### Docker Setup

1. Build and run the application:
   ```bash
   docker-compose up --build
   ```

2. The application will be available at http://localhost:8080

3. To stop:
   ```bash
   docker-compose down
   ```

## Configuration

All configuration is done through environment variables in `.env.example`. Copy this file to `.env` and modify as needed.

## API Endpoints

- `POST /api/tickets` - Create a new downtime ticket
- `GET /api/tickets` - Get all tickets
- `GET /api/tickets/{id}` - Get a specific ticket by ID
- `GET /health` - Health check endpoint

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./data/downtime.db` |
| `VLLM_BASE_URL` | Base URL for vLLM API | `http://localhost:8000/v1` |
| `VLLM_MODEL` | Model name to use | `nemotron-3-nano` |
| `APP_HOST` | Application host | `0.0.0.0` |
| `APP_PORT` | Application port | `8080` |

## Notes

- The application will run even if the vLLM model is not available (will show a message instead of summary)
- Data is stored in the `data/` directory as SQLite database
- In production, you may want to configure a more robust database