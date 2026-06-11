# Clinic Wait Times API backend
import asyncio
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI()

# ----------------------------------------------------------------------
# In‑memory data structures
# ----------------------------------------------------------------------
queue: List[dict] = []          # patient records
clients: List[WebSocket] = []   # connected WebSocket clients

# ----------------------------------------------------------------------
# Pydantic models
# ----------------------------------------------------------------------
class CheckInPatient(BaseModel):
    patient_id: str
    name: str
    check_in_time: datetime


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def calculate_wait_time(check_in: datetime) -> float:
    """Return wait time in seconds."""
    now = datetime.now()
    return (now - check_in).total_seconds()


def broadcast_queue():
    """Send updated queue to all connected WebSocket clients."""
    if clients:
        for client in list(clients):  # copy to avoid modification during iteration
            asyncio.create_task(client.send_json({"queue": queue}))


# ----------------------------------------------------------------------
# API endpoints
# ----------------------------------------------------------------------
@app.get("/")
async def read_root():
    return {"message": "Clinic Wait Times API"}


@app.post("/patients/check-in")
async def patient_check_in(patient: CheckInPatient):
    """Add a patient to the queue and compute wait time."""
    wait_seconds = calculate_wait_time(patient.check_in_time)
    item = {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "check_in_time": patient.check_in_time,
        "wait_time": wait_seconds,
        "longest_wait": False,
    }
    queue.append(item)

    # Determine if this patient now has the longest wait
    max_wait = max((i["wait_time"] for i in queue), default=0)
    item["longest_wait"] = item["wait_time"] == max_wait

    await broadcast_queue()
    return {"msg": "Patient checked in", "queue": queue}


@app.get("/queue")
async def get_queue():
    """Return current queue with wait times."""
    return queue


# ----------------------------------------------------------------------
# WebSocket endpoint for real‑time updates
# ----------------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # Keep connection alive; optionally listen for messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)


# ----------------------------------------------------------------------
# Run with `uvicorn backend.main:app` when executed directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)