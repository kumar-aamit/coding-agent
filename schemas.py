"""Pydantic schemas. TODO: complete validation and response models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_name: str
    provider_name: str
    scheduled_at: datetime
    reason: Optional[str] = None
    status: str = "scheduled"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_name: Optional[str] = None
    provider_name: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None


class Appointment(AppointmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BestTimeRequest(BaseModel):
    """TODO: fields for preferred days, time windows, provider, urgency, etc."""
    provider_name: str
    preferred_date: Optional[str] = None
    reason: Optional[str] = None


class BestTimeResponse(BaseModel):
    """TODO: recommended slot from LLM."""
    recommended_time: str
    explanation: str


class WaitingTimeRequest(BaseModel):
    """TODO: fields needed to estimate wait."""
    provider_name: str
    scheduled_at: datetime
    reason: Optional[str] = None


class WaitingTimeResponse(BaseModel):
    """TODO: estimated wait from LLM."""
    estimated_wait_minutes: int
    explanation: str
