import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime
import os

from app.models import DowntimeCreate, DowntimeResponse
from app.db import init_db, log_downtime, get_downtime_history
from app.llm import LLMClient

app = FastAPI()
llm_client = LLMClient()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/downtime", response_model=DowntimeResponse)
async def create_downtime(event: DowntimeCreate):
    try:
        # Convert datetime to ISO format string for storage
        start_str = event.start_time.isoformat()
        end_str = event.end_time.isoformat() if event.end_time else None
        
        log_downtime(
            machine_id=event.machine_id,
            start_time=start_str,
            end_time=end_str,
            reason=event.reason
        )
        response = DowntimeResponse(**event.model_dump(), created_at=datetime.utcnow())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/downtime/{machine_id}")
async def read_downtime(machine_id: str):
    try:
        history = get_downtime_history(machine_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_llm(prompt: str):
    try:
        result = llm_client.query(prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        db_ok = True
        llm_ok = True
        
        # Check DB connection
        from app.db import init_db
        init_db()
        
        # Check LLM connectivity
        llm_client.health_check()
        
        return {"status": "healthy", "database": db_ok, "llm": llm_ok}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)