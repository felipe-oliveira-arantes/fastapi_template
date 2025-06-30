from typing import List, Optional
from sqlalchemy.orm import Session

from app.adapters.dbBase import DBAdapterBase
from app.adapters.postgresAdapter import PostgreSQLAdapter
from app.models.patient import PatientDates

class PatientsBO:
    def __init__(
        self,
        db_adapter: Optional[DBAdapterBase[PatientDates]] = None,
    ):
        self.adapter = db_adapter or PostgreSQLAdapter(PatientDates)

    def create_patient(self, db: Session, patient: PatientDates) -> PatientDates:
        # Aqui no futuro você pode validar se o paciente existe, se já tem agendamento no horário, etc.
        return self.adapter.create(db, patient)

    def get_patients(self, db: Session, query: dict = {}) -> List[PatientDates]:
        return self.adapter.read(db, query)

    def update_patient(self, db: Session, db_obj: PatientDates, new_data: dict) -> PatientDates:
        return self.adapter.update(db, db_obj, new_data)

    def delete_patient(self, db: Session, obj_id) -> bool:
        return self.adapter.delete(db, obj_id)
