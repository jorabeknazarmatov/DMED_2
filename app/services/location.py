from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json
from pathlib import Path
from app.repositories.region import RegionRepository
from app.repositories.city import CityRepository
from app.schemas.location import RegionResponse, RegionWithCities, CityResponse
from app.core.exceptions import not_found_exception
from app.core.logging import get_logger

logger = get_logger(__name__)


class LocationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.region_repo = RegionRepository(db)
        self.city_repo = CityRepository(db)

    async def get_all_regions(self) -> list[RegionResponse]:
        """Get all regions."""
        logger.info("Fetching all regions")
        regions = await self.region_repo.get_all()
        return [RegionResponse.model_validate(region) for region in regions]

    async def get_region_by_id(self, region_id: int) -> RegionResponse:
        """Get region by ID."""
        logger.info(f"Fetching region with id={region_id}")
        region = await self.region_repo.get_by_id(region_id)
        if not region:
            raise not_found_exception("Region", region_id)
        return RegionResponse.model_validate(region)

    async def get_region_with_cities(self, region_id: int) -> RegionWithCities:
        """Get region with cities."""
        logger.info(f"Fetching region with cities for id={region_id}")
        region = await self.region_repo.get_by_id_with_cities(region_id)
        if not region:
            raise not_found_exception("Region", region_id)
        return RegionWithCities.model_validate(region)

    async def get_cities_by_region(self, region_id: int) -> list[CityResponse]:
        """Get all cities in a region."""
        logger.info(f"Fetching cities for region_id={region_id}")

        # Check if region exists
        region = await self.region_repo.get_by_id(region_id)
        if not region:
            raise not_found_exception("Region", region_id)

        cities = await self.city_repo.get_by_region_id(region_id)
        return [CityResponse.model_validate(city) for city in cities]

    async def import_regions_from_json(self, json_file_path: str) -> dict:
        """
        Import regions and cities from JSON file.
        This is a one-time admin operation.
        """
        logger.info(f"Starting import from {json_file_path}")

        # Read JSON file
        file_path = Path(json_file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {json_file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clear existing data (optional - for fresh import)
        await self.region_repo.delete_all()

        # Prepare data for bulk insert
        regions_data = []
        for item in data:
            # Handle both "region" and "reqion" (typo in JSON)
            region_name = item.get("region") or item.get("reqion")
            cities = item.get("cities", [])

            regions_data.append({
                "name": region_name,
                "cities": cities
            })

        # Bulk create regions and cities
        regions = await self.region_repo.bulk_create(regions_data)

        total_cities = sum(len(r.cities) for r in regions)

        logger.info(
            f"Import completed: {len(regions)} regions, {total_cities} cities"
        )

        return {
            "message": "Import successful",
            "regions_count": len(regions),
            "cities_count": total_cities
        }
