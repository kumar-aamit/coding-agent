# coding-agent

A minimal FastAPI application that serves as a chat interface to vLLM models.

## Features

- FastAPI web server exposing REST endpoints
- Integration with vLLM for model inference at http://127.0.0.1:8080/v1
- Docker support with docker-compose.yml
- Health check endpoint at /health

## Getting Started

1. Configure vLLM server at the specified endpoint
2. Run the application
3. Access the API at the root endpoint

## Endpoints

- `GET /`: Root endpoint returning basic service status
- `GET /health`: Health check endpoint that verifies connection to vLLM

## Configuration

The application expects the vLLM API to be running at `http://127.0.0.1:8080/v1` with model `nvidia/nemotron-3-nano` specified.

## Development

Requires Python 3.11+, FastAPI, uvicorn, and vllm packages.

## Docker

The application can be built and run using Docker or docker-compose.

## License

This project is licensed under the MIT License.