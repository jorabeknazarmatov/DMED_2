from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MedicalCardBase(BaseModel):
    card_number: str


class MedicalCardResponse(MedicalCardBase):
    id: int
    patient_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
