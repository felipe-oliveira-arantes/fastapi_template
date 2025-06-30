# app/routers/appointment_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.appointment_schema import AppointmentCreateSchema
from app.models.appointment import AppointmentDates
from app.controller.appointmentBO import AppointmentBO
from app.dependencies.container import get_db

router = APIRouter(prefix="/appointment", tags=["Consultas"])

appointment_bo = AppointmentBO()  # usa adapter default internamente

@router.post("/create", response_model=AppointmentDates)
def create_consulta(
    appointment: AppointmentCreateSchema,
    db: Session = Depends(get_db)
):
    """Creates a new appointment in the database.

    Args:
        appointment (AppointmentCreateSchema): The appointment data to be created.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        AppointmentDates: The created appointment's data with dates.
    """
    return appointment_bo.create_appointment(db=db, appointment=AppointmentDates(**appointment.dict()))
