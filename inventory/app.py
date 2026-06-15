import sqlite3
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
BASE_DIR = Path(__file__).parent
TEMPLATES = Jinja2Templates(directory=BASE_DIR / "templates")
DB_PATH = BASE_DIR / "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def setup_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS parts (
            part_number TEXT PRIMARY KEY,
            qty INTEGER NOT NULL,
            location TEXT NOT NULL
        )
        """
    )
    conn.commit()
    # Insert sample data if table is empty
    cur = conn.execute("SELECT COUNT(*) FROM parts")
    if cur.fetchone()[0] == 0:
        sample_parts = [
            ("P001", 10, "Shelf A1"),
            ("P002", 2, "Shelf B2"),
            ("P003", 0, "Shelf C3"),
            ("P004", 7, "Shelf A2"),
        ]
        conn.executemany("INSERT INTO parts (part_number, qty, location) VALUES (?,?,?)", sample_parts)
        conn.commit()
    conn.close()


@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})


@app.get("/")
async def index(request: Request):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM parts").fetchall()
    parts = [dict(row) for row in rows]
    low_stock_parts = [p for p in parts if p["qty"] < 5]
    suggestions = []
    for part in low_stock_parts:
        prompt = (
            f"Suggest reorder quantity for part {part['part_number']} "
            f"with current stock {part['qty']} at {part['location']}"
        )
        try:
            resp = requests.post(
                "http://127.0.0.1:8000/v1/completions",
                json={"prompt": prompt},
                timeout=5,
            )
            if resp.status_code == 200:
                suggestion = resp.json().get("choices", [{}])[0].get("text", "").strip()
                suggestions.append({"part": part, "suggestion": suggestion})
        except Exception:
            suggestions.append({"part": part, "suggestion": "Error contacting LLM"})
    conn.close()
    return templates.TemplateResponse(
        "index.html", {"request": request, "parts": parts, "suggestions": suggestions}
    )