# Inventory Tracker

A simple inventory management web application built with FastAPI, Jinja2, and SQLite. It tracks spare parts (part number, quantity, location) and uses an LLM via vLLM at http://127.0.0.1:8000/v1 to suggest reorder actions for low-stock items.

## Features

- Add, view, update, and delete parts
- Health check endpoint at `/health`
- Low-stock detection and LLM-powered reorder suggestions
- Docker support with `docker-compose`

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload

# Or using Docker Compose
docker-compose up --build
```

## Endpoints

- `GET /health` - Health check
- `GET /parts` - List all parts
- `POST /parts` - Create a new part
- `GET /parts/{id}` - Get part details
- `PUT /parts/{id}` - Update a part
- `DELETE /parts/{id}` - Delete a part
- `GET /parts/low-stock` - Get low-stock parts and reorder suggestions