import sqlite3
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import os
from datetime import datetime

app = FastAPI()

# Database setup
DB_PATH = "sqlite.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB on startup
@app.on_event("startup")
def startup():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS shift_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shift TEXT NOT NULL,
            operator TEXT NOT NULL,
            notes TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Serve static files and templates
app.mount("/static", StaticFiles(directory="/home/dcloud/openclaw/workspace/coding-agent/shift_log_app/app/static", html=True), name="static")
templates = Jinja2Templates(directory="/home/dcloud/openclaw/workspace/coding-agent/shift_log_app/app/templates")

# Pydantic model for log creation
class LogEntry(BaseModel):
    shift: str
    operator: str
    notes: str

# Health endpoint
@app.get("/health")
async def health():
    return JSONResponse(content={"status": "OK"})

# Root route - serves HTML form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API to create a new log entry
@app.post("/logs")
async def create_log(entry: LogEntry):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO shift_logs (shift, operator, notes) VALUES (?, ?, ?)",
        (entry.shift.upper(), entry.operator, entry.notes)
    )
    conn.commit()
    conn.close()
    return {"message": "Log entry created"}

# Retrieve all logs (optional)
@app.get("/logs")
async def read_logs():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM shift_logs ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Summarize open issues using vLLM
@app.get("/summarize")
async def summarize_open_issues():
    conn = get_db_connection()
    rows = conn.execute("SELECT shift, operator, notes FROM shift_logs").fetchall()
    conn.close()
    issues_text = "\n".join([f"Shift: {r['shift']}, Operator: {r['operator']}, Notes: {r['notes']}" for r in rows])
    if not issues_text.strip():
        return {"summary": "No open issues."}
    
    # Call vLLM endpoint
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/v1/completions",
                json={
                    "model": "meta-llama/Llama-2-7b-chat",  # placeholder model name
                    "prompt": f"Summarize the following open issues:\n{issues_text}\nSummary:",
                    "max_tokens": 150
                }
            )
            response.raise_for_status()
            data = response.json()
            # Assume the summary is in the first choice's message
            summary = data["choices"][0]["text"].strip()
            return {"summary": summary}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")