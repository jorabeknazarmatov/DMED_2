import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.medical_card import MedicalCard
from app.core.logging import get_logger

logger = get_logger(__name__)


async def generate_unique_medical_card_number(db: AsyncSession, max_attempts: int = 100) -> str:
    """
    Generate unique medical card number.
    Format: 2 uppercase letters + 4 digits (e.g., AB1234)

    Strategy: Generate random card number and check uniqueness in database.
    If duplicate found, retry up to max_attempts times.

    Args:
        db: Database session
        max_attempts: Maximum number of generation attempts

    Returns:
        Unique medical card number

    Raises:
        Exception: If unable to generate unique number after max_attempts
    """
    for attempt in range(max_attempts):
        # Generate 2 random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))

        # Generate 4 random digits
        digits = ''.join(random.choices(string.digits, k=4))

        # Combine to create card number
        card_number = f"{letters}{digits}"

        # Check if card number already exists
        result = await db.execute(
            select(MedicalCard).where(MedicalCard.card_number == card_number)
        )
        existing_card = result.scalar_one_or_none()

        if not existing_card:
            logger.info(f"Generated unique medical card number: {card_number} (attempt {attempt + 1})")
            return card_number

        logger.warning(f"Duplicate card number {card_number} found, retrying... (attempt {attempt + 1})")

    # If we couldn't generate unique number after max_attempts
    error_msg = f"Failed to generate unique medical card number after {max_attempts} attempts"
    logger.error(error_msg)
    raise Exception(error_msg)


async def generate_unique_medical_card_number_bulk_check(db: AsyncSession) -> str:
    """
    Alternative strategy: Load all existing card numbers first, then generate unique one.
    This is more efficient when there are many cards in database.

    Args:
        db: Database session

    Returns:
        Unique medical card number
    """
    # Load all existing card numbers
    result = await db.execute(select(MedicalCard.card_number))
    existing_cards = set(result.scalars().all())

    logger.info(f"Loaded {len(existing_cards)} existing medical card numbers")

    # Generate unique card number
    max_attempts = 1000
    for attempt in range(max_attempts):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=4))
        card_number = f"{letters}{digits}"

        if card_number not in existing_cards:
            logger.info(f"Generated unique medical card number: {card_number} (attempt {attempt + 1})")
            return card_number

    # If we couldn't generate unique number
    error_msg = f"Failed to generate unique medical card number after {max_attempts} attempts"
    logger.error(error_msg)
    raise Exception(error_msg)


def generate_password() -> str:
    """
    Generate random 6-digit password for new user.
    Format: 6 random digits (e.g., 123456)

    Returns:
        6-digit password as string
    """
    password = ''.join(random.choices(string.digits, k=6))
    logger.info(f"Generated new 6-digit password")
    return password
