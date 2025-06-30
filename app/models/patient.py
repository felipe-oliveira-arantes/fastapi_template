from typing import Optional
from datetime import date, datetime
from enum import Enum
import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class PatientBase(SQLModel):
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

class PatientID(PatientBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class PatientDates(PatientID, table=True):
    __tablename__ = "patients"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

