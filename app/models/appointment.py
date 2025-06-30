from typing import Optional
from datetime import datetime
from enum import Enum
import uuid
from sqlmodel import Field, Relationship, SQLModel

class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    rescheduled = "rescheduled"
    canceled = "canceled"
    attended = "attended"

class AppointmentBase(SQLModel):
    pacient_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    datetime: datetime
    status: AppointmentStatus = Field(default=AppointmentStatus.scheduled)
    
class AppointmentID(AppointmentBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class AppointmentDates(AppointmentID, table=True):
    __tablename__ = "appointments"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

