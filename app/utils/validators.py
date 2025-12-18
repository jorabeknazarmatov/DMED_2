"""
Validators for application data.
Frontend handles most validation, but critical validations can be added here.
"""

from app.core.logging import get_logger

logger = get_logger(__name__)


def validate_gender(gender: str) -> bool:
    """Validate gender value."""
    valid_genders = ["male", "female"]
    return gender.lower() in valid_genders
