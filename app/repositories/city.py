from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.city import City
from app.core.logging import get_logger

logger = get_logger(__name__)


class CityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[City]:
        """Get all cities."""
        result = await self.db.execute(select(City))
        return list(result.scalars().all())

    async def get_by_id(self, city_id: int) -> Optional[City]:
        """Get city by ID."""
        result = await self.db.execute(
            select(City).where(City.id == city_id)
        )
        return result.scalar_one_or_none()

    async def get_by_region_id(self, region_id: int) -> list[City]:
        """Get all cities in a region."""
        result = await self.db.execute(
            select(City).where(City.region_id == region_id)
        )
        return list(result.scalars().all())

    async def create(self, name: str, region_id: int) -> City:
        """Create new city."""
        city = City(name=name, region_id=region_id)
        self.db.add(city)
        await self.db.commit()
        await self.db.refresh(city)
        logger.info(f"Created city: {city.name} (id={city.id}, region_id={city.region_id})")
        return city
