from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.static_files import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base, DowntimeTicket
from app.database import engine
from app.llm import LLMApiClient
import os
import json
from datetime import datetime

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize LLMApi client
llm_client = LLMApiClient()

# Create FastAPI app
app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint to create a new downtime ticket
@app.post("/api/tickets")
async def create_ticket(
    machine_id: str = Form(None),
    line_area: str = Form(None),
    stop_reason_category: str = Form(None),
    description: str = Form(None),
    severity: str = Form('medium'),
    operator_name: str = Form(None)
):
    # Create a new downtime ticket
    ticket = DowntimeTicket(
        machine_id=machine_id,
        line_area=line_area,
        stop_reason_category=stop_reason_category,
        description=description,
        severity=severity,
        operator_name=operator_name
    )
    
    # Add to database (we'll implement database session management properly)
    # For now, we'll just return the ticket info
    ticket_dict = ticket.to_dict()
    
    # Generate LLM summary if LLMApiClient is available
    try:
        summary = llm_client.generate_summary(ticket_dict)
        ticket_dict['summary'] = summary
    except Exception as e:
        ticket_dict['summary'] = f"Could not generate summary: {str(e)}"
    
    return JSONResponse(content=ticket_dict)

# API endpoint to get all tickets
@app.get("/api/tickets")
async def get_tickets():
    # This is a simplified version - in a real app we'd use proper DB sessions
    # For now, we'll return a mock response
    return {"tickets": []}

# API endpoint to get ticket by ID
@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    # Return mock ticket data
    return {
        "id": ticket_id,
        "machine_id": f"MACH-{ticket_id}",
        "line_area": "Line 1",
        "stop_reason_category": "Mechanical Issue",
        "description": "Unexpected stoppage during operation",
        "severity": "high",
        "operator_name": "John Doe",
        "timestamp": datetime.now(),
        "status": "open",
        "resolution_notes": None
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)