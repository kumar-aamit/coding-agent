# Clinic Wait Times

A simple FastAPI application to track patient check‑ins, compute wait times, and display a real‑time board.

## Prerequisites

- Python 3.11+
- Docker
- Docker Compose

## Running the Application

1. Clone the repository.
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start the backend server:

   ```bash
   uvicorn backend.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

4. Serve the frontend:

   ```bash
   cd frontend
   python -m http.server 8080
   ```

   Then open `http://localhost:8080` in a browser.

5. Use the UI to simulate patient check‑ins; the queue will update in real time via WebSocket.

## Docker

To run with Docker Compose:

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8000` and static files at `http://localhost:80`.

## Testing

```bash
pytest tests
```

## CI

The GitHub Actions workflow in `.github/workflows/ci.yml` runs tests and builds the Docker image on each push.