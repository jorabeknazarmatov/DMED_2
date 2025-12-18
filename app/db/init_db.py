from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger

logger = get_logger(__name__)


async def init_db(session: AsyncSession) -> None:
    """Initialize database with seed data if needed."""
    logger.info("Database initialization started")
    # Database tables will be created via Alembic migrations
    # Seed data will be loaded via admin import endpoint
    logger.info("Database initialization completed")
