from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.api.deps import get_database
from app.services.location import LocationService
from app.schemas.location import RegionResponse, RegionWithCities, CityResponse

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/regions/", response_model=list[RegionResponse])
async def get_regions(
    db: AsyncSession = Depends(get_database)
):
    """Get all regions."""
    service = LocationService(db)
    return await service.get_all_regions()


@router.get("/regions/{region_id}", response_model=RegionResponse)
async def get_region(
    region_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get region by ID."""
    service = LocationService(db)
    return await service.get_region_by_id(region_id)


@router.get("/regions/{region_id}/cities/", response_model=list[CityResponse])
async def get_region_cities(
    region_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get all cities in a region."""
    service = LocationService(db)
    return await service.get_cities_by_region(region_id)


@router.get("/cities/", response_model=list[CityResponse])
async def get_cities_by_region(
    region_id: Optional[int] = Query(None, description="Filter cities by region ID"),
    db: AsyncSession = Depends(get_database)
):
    """Get cities filtered by region."""
    service = LocationService(db)
    if region_id:
        return await service.get_cities_by_region(region_id)
    # If no region_id, return empty list (or all cities if you prefer)
    return []
