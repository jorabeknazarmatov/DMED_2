from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional
from app.models.patient import Patient
from app.models.medical_card import MedicalCard
from app.schemas.patient import PatientCreate, PatientUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)


class PatientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        search: Optional[str] = None,
        region_id: Optional[int] = None,
        city_id: Optional[int] = None
    ) -> list[Patient]:
        """Get all patients with optional filters."""
        query = select(Patient).options(selectinload(Patient.medical_card))

        # Apply filters
        if search:
            search_filter = or_(
                Patient.first_name.ilike(f"%{search}%"),
                Patient.last_name.ilike(f"%{search}%"),
                Patient.middle_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)

        if region_id:
            query = query.where(Patient.region_id == region_id)

        if city_id:
            query = query.where(Patient.city_id == city_id)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, patient_id: int) -> Optional[Patient]:
        """Get patient by ID with medical card."""
        result = await self.db.execute(
            select(Patient)
            .options(selectinload(Patient.medical_card))
            .where(Patient.id == patient_id)
        )
        return result.scalar_one_or_none()

    async def get_by_medical_card_number(self, card_number: str) -> Optional[Patient]:
        """Get patient by medical card number."""
        result = await self.db.execute(
            select(Patient)
            .join(MedicalCard)
            .where(MedicalCard.card_number == card_number)
            .options(selectinload(Patient.medical_card))
        )
        return result.scalar_one_or_none()

    async def create(self, patient_data: PatientCreate) -> Patient:
        """Create new patient."""
        patient = Patient(**patient_data.model_dump())
        self.db.add(patient)
        await self.db.commit()
        await self.db.refresh(patient)
        logger.info(f"Created patient: {patient.first_name} {patient.last_name} (id={patient.id})")
        return patient

    async def update(self, patient: Patient, patient_data: PatientUpdate) -> Patient:
        """Update patient."""
        update_data = patient_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(patient, field, value)

        await self.db.commit()
        await self.db.refresh(patient)
        logger.info(f"Updated patient: {patient.first_name} {patient.last_name} (id={patient.id})")
        return patient

    async def delete(self, patient: Patient) -> None:
        """Delete patient (cascade deletes medical card)."""
        patient_id = patient.id
        patient_name = f"{patient.first_name} {patient.last_name}"
        await self.db.delete(patient)
        await self.db.commit()
        logger.info(f"Deleted patient: {patient_name} (id={patient_id})")
