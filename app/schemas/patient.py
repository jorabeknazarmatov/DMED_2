from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from app.schemas.medical_card import MedicalCardResponse


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    gender: str
    phone: Optional[str] = None
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    address: Optional[str] = None


class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    medical_card: Optional[MedicalCardResponse] = None

    model_config = ConfigDict(from_attributes=True)


class PatientListResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    gender: str
    phone: Optional[str] = None
    medical_card: Optional[MedicalCardResponse] = None

    model_config = ConfigDict(from_attributes=True)
