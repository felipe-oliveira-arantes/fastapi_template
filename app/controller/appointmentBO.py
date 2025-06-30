# app/controller/appointment_bo.py

from typing import List, Optional
from sqlalchemy.orm import Session

from app.adapters.dbBase import DBAdapterBase
from app.adapters.postgresAdapter import PostgreSQLAdapter
from app.models.appointment import AppointmentDates

class AppointmentBO:
    def __init__(
        self,
        db_adapter: Optional[DBAdapterBase[AppointmentDates]] = None,
    ):
        self.adapter = db_adapter or PostgreSQLAdapter(AppointmentDates)

    def create_appointment(self, db: Session, appointment: AppointmentDates) -> AppointmentDates:
        # Aqui no futuro você pode validar se o paciente existe, se já tem agendamento no horário, etc.
        return self.adapter.create(db, appointment)

    def get_appointments(self, db: Session, query: dict = {}) -> List[AppointmentDates]:
        return self.adapter.read(db, query)

    def update_appointment(self, db: Session, db_obj: AppointmentDates, new_data: dict) -> AppointmentDates:
        return self.adapter.update(db, db_obj, new_data)

    def delete_appointment(self, db: Session, obj_id) -> bool:
        return self.adapter.delete(db, obj_id)
