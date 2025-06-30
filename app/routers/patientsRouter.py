# app/routers/appointment_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.patient_schema import PatientCreateSchema
from app.models.patient import PatientDates
from app.controller.patientsBO import PatientsBO
from app.dependencies.container import get_db

router = APIRouter(prefix="/patients", tags=["Pacientes"])

patients_bo = PatientsBO()  # usa adapter default internamente

@router.post("/create", response_model=PatientDates)
def create_consulta(
    patient: PatientCreateSchema,
    db: Session = Depends(get_db)
):
    return patients_bo.create_patient(db=db, patient=PatientDates(**patient.dict()))
