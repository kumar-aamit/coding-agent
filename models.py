"""SQLAlchemy models. TODO: implement Appointment model and any helpers."""

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=False)
    provider_name = Column(String(255), nullable=False)
    # TODO: store as ISO datetime strings or proper DateTime columns
    scheduled_at = Column(DateTime, nullable=False)
    reason = Column(String(512), nullable=True)
    status = Column(String(50), nullable=False, default="scheduled")

    # TODO: add __repr__ or helper methods if useful
