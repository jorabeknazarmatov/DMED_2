from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.api.deps import get_database
from app.services.patient import PatientService
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse, PatientListResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/", response_model=list[PatientListResponse])
async def get_patients(
    search: Optional[str] = Query(None, description="Search by first name, last name, or middle name"),
    region_id: Optional[int] = Query(None, description="Filter by region ID"),
    city_id: Optional[int] = Query(None, description="Filter by city ID"),
    medical_card_number: Optional[str] = Query(None, description="Search by medical card number"),
    db: AsyncSession = Depends(get_database)
):
    """Get all patients with optional filters."""
    service = PatientService(db)
    return await service.get_all_patients(
        search=search,
        region_id=region_id,
        city_id=city_id,
        medical_card_number=medical_card_number
    )


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create new patient (automatically generates medical card)."""
    service = PatientService(db)
    return await service.create_patient(patient_data)


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get patient by ID."""
    service = PatientService(db)
    return await service.get_patient_by_id(patient_id)


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update patient by ID."""
    service = PatientService(db)
    return await service.update_patient(patient_id, patient_data)


@router.patch("/{patient_id}", response_model=PatientResponse)
async def partial_update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Partially update patient by ID."""
    service = PatientService(db)
    return await service.update_patient(patient_id, patient_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete patient by ID (hard delete)."""
    service = PatientService(db)
    await service.delete_patient(patient_id)
