from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.repositories.patient import PatientRepository
from app.repositories.medical_card import MedicalCardRepository
from app.repositories.region import RegionRepository
from app.repositories.city import CityRepository
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse, PatientListResponse
from app.utils.generators import generate_unique_medical_card_number
from app.core.exceptions import not_found_exception, validation_exception
from app.core.logging import get_logger

logger = get_logger(__name__)


class PatientService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.patient_repo = PatientRepository(db)
        self.medical_card_repo = MedicalCardRepository(db)
        self.region_repo = RegionRepository(db)
        self.city_repo = CityRepository(db)

    async def get_all_patients(
        self,
        search: Optional[str] = None,
        region_id: Optional[int] = None,
        city_id: Optional[int] = None,
        medical_card_number: Optional[str] = None
    ) -> list[PatientListResponse]:
        """Get all patients with optional filters."""
        logger.info(
            f"Fetching patients with filters: search={search}, "
            f"region_id={region_id}, city_id={city_id}, medical_card={medical_card_number}"
        )

        # If searching by medical card number, use specific query
        if medical_card_number:
            patient = await self.patient_repo.get_by_medical_card_number(medical_card_number)
            if patient:
                return [PatientListResponse.model_validate(patient)]
            return []

        # Otherwise, use general query with filters
        patients = await self.patient_repo.get_all(
            search=search,
            region_id=region_id,
            city_id=city_id
        )
        return [PatientListResponse.model_validate(patient) for patient in patients]

    async def get_patient_by_id(self, patient_id: int) -> PatientResponse:
        """Get patient by ID."""
        logger.info(f"Fetching patient with id={patient_id}")
        patient = await self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise not_found_exception("Patient", patient_id)
        return PatientResponse.model_validate(patient)

    async def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        """Create new patient with automatic medical card generation."""
        logger.info(f"Creating patient: {patient_data.first_name} {patient_data.last_name}")

        # Validate region and city if provided
        if patient_data.region_id:
            region = await self.region_repo.get_by_id(patient_data.region_id)
            if not region:
                raise validation_exception(f"Region with id={patient_data.region_id} not found")

        if patient_data.city_id:
            city = await self.city_repo.get_by_id(patient_data.city_id)
            if not city:
                raise validation_exception(f"City with id={patient_data.city_id} not found")

            # Validate that city belongs to region
            if patient_data.region_id and city.region_id != patient_data.region_id:
                raise validation_exception(
                    f"City with id={patient_data.city_id} does not belong to "
                    f"region with id={patient_data.region_id}"
                )

        # Create patient
        patient = await self.patient_repo.create(patient_data)

        # Generate unique medical card number
        card_number = await generate_unique_medical_card_number(self.db)

        # Create medical card
        await self.medical_card_repo.create(card_number, patient.id)

        # Refresh patient to get medical card
        patient = await self.patient_repo.get_by_id(patient.id)

        logger.info(
            f"Patient created successfully: {patient.first_name} {patient.last_name} "
            f"(id={patient.id}, card={card_number})"
        )

        return PatientResponse.model_validate(patient)

    async def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> PatientResponse:
        """Update patient."""
        logger.info(f"Updating patient with id={patient_id}")

        # Get existing patient
        patient = await self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise not_found_exception("Patient", patient_id)

        # Validate region and city if provided
        if patient_data.region_id:
            region = await self.region_repo.get_by_id(patient_data.region_id)
            if not region:
                raise validation_exception(f"Region with id={patient_data.region_id} not found")

        if patient_data.city_id:
            city = await self.city_repo.get_by_id(patient_data.city_id)
            if not city:
                raise validation_exception(f"City with id={patient_data.city_id} not found")

            # Validate that city belongs to region
            region_id = patient_data.region_id or patient.region_id
            if region_id and city.region_id != region_id:
                raise validation_exception(
                    f"City with id={patient_data.city_id} does not belong to "
                    f"region with id={region_id}"
                )

        # Update patient
        updated_patient = await self.patient_repo.update(patient, patient_data)

        logger.info(f"Patient updated successfully: id={patient_id}")

        return PatientResponse.model_validate(updated_patient)

    async def delete_patient(self, patient_id: int) -> None:
        """Delete patient (cascade deletes medical card)."""
        logger.info(f"Deleting patient with id={patient_id}")

        # Get existing patient
        patient = await self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise not_found_exception("Patient", patient_id)

        # Delete patient
        await self.patient_repo.delete(patient)

        logger.info(f"Patient deleted successfully: id={patient_id}")
