# app/schemas/appointment_schema.py

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.appointment import AppointmentStatus

class PatientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    birth_date: date
    cpf: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
