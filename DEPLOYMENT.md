# Deployment Guide

This document outlines the steps to deploy and run the FastAPI chatbot application with vLLM integration.

## Prerequisites

- Docker and Docker Compose installed
- Access to the vLLM inference endpoint at `http://127.0.0.1:8080/v1`
- The model `nvidia/nemotron-3-nano` must be available at the endpoint

## Deployment Steps

### 1. Clone the Repository
```bash
git clone https://github.com/kumar-aamit/coding-agent.git
cd coding-agent
```

### 2. Build and Run with Docker Compose
```bash
docker-compose.yml up --build
```

### 3. Verify the Service
- The API will be available at `http://localhost:8080`
- Health check endpoint: `GET /health` 
- Root endpoint: `GET /`

### 4. Configuration Options

Environment variables can be modified in `docker-compose.yml`:
- `VLLM_BASE_URL`: Override the vLLM API endpoint URL
- `VLLM_MODEL`: Specify the model to use for inference

## Configuration Details

The application expects the vLLM server to be accessible at the configured endpoint. The default configuration assumes the server is running locally at port 8080.

## Maintenance

To update the application:
1. Pull the latest changes from the repository
2. Rebuild the Docker images: `docker-compose.yml up --build`
3. Restart the containers

## Troubleshooting

- If the health check fails, verify that the vLLM endpoint is accessible and the model is loaded
- Check container logs for detailed error information
- Ensure all required dependencies are installed and up to date