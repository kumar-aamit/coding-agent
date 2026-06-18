"""FastAPI health appointment app. TODO: wire CRUD + LLM endpoints."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas
from database import get_db, init_db

app = FastAPI(title="Health Appointment Tracker", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    # TODO: call init_db()
    pass


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


# --- Appointments CRUD (TODO) ---


@app.get("/appointments", response_model=list[schemas.Appointment])
def list_appointments(db: Session = Depends(get_db)):
    raise NotImplementedError


@app.post("/appointments", response_model=schemas.Appointment, status_code=201)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    raise NotImplementedError


@app.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError


@app.patch("/appointments/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(
    appointment_id: int,
    payload: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
):
    raise NotImplementedError


@app.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError


# --- LLM-assisted endpoints (TODO) ---


@app.post("/best-time", response_model=schemas.BestTimeResponse)
async def suggest_best_time(payload: schemas.BestTimeRequest):
    """Use vLLM (llm_client) to recommend best appointment time."""
    raise NotImplementedError


@app.post("/waiting-time", response_model=schemas.WaitingTimeResponse)
async def estimate_waiting_time(payload: schemas.WaitingTimeRequest):
    """Use vLLM (llm_client) to estimate waiting time."""
    raise NotImplementedError
