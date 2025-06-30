# app/schemas/appointment_schema.py

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.models.appointment import AppointmentStatus

class AppointmentCreateSchema(BaseModel):
    pacient_id: UUID
    datetime: datetime
    status: AppointmentStatus = AppointmentStatus.scheduled
