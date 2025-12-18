from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from app.models.region import Region
from app.models.city import City
from app.core.logging import get_logger

logger = get_logger(__name__)


class RegionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Region]:
        """Get all regions."""
        result = await self.db.execute(select(Region))
        return list(result.scalars().all())

    async def get_by_id(self, region_id: int) -> Optional[Region]:
        """Get region by ID."""
        result = await self.db.execute(
            select(Region).where(Region.id == region_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_cities(self, region_id: int) -> Optional[Region]:
        """Get region by ID with cities."""
        result = await self.db.execute(
            select(Region)
            .options(selectinload(Region.cities))
            .where(Region.id == region_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Region]:
        """Get region by name."""
        result = await self.db.execute(
            select(Region).where(Region.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Region:
        """Create new region."""
        region = Region(name=name)
        self.db.add(region)
        await self.db.commit()
        await self.db.refresh(region)
        logger.info(f"Created region: {region.name} (id={region.id})")
        return region

    async def bulk_create(self, regions_data: list[dict]) -> list[Region]:
        """Bulk create regions with cities."""
        regions = []
        for region_data in regions_data:
            region = Region(name=region_data["name"])
            self.db.add(region)
            await self.db.flush()  # Get region.id

            # Add cities
            for city_name in region_data.get("cities", []):
                city = City(name=city_name, region_id=region.id)
                self.db.add(city)

            regions.append(region)

        await self.db.commit()
        logger.info(f"Bulk created {len(regions)} regions with cities")
        return regions

    async def delete_all(self) -> None:
        """Delete all regions (cascade deletes cities)."""
        await self.db.execute(select(Region))
        regions = (await self.db.execute(select(Region))).scalars().all()
        for region in regions:
            await self.db.delete(region)
        await self.db.commit()
        logger.info("Deleted all regions")
