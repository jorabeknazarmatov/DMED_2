from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.services.location import LocationService
from app.core.security import verify_admin_credentials

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/import-regions", status_code=status.HTTP_200_OK)
async def import_regions(
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Import regions and cities from JSON file (one-time admin operation).
    This will clear existing regions/cities and import fresh data.

    Requires admin authentication (username: admin, password: admin123)
    """
    service = LocationService(db)

    # Path to JSON file (relative to project root)
    json_file_path = "regions_and_cities.json"

    result = await service.import_regions_from_json(json_file_path)
    return result
