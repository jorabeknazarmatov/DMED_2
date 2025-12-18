from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medical_card import MedicalCard
from app.core.logging import get_logger

logger = get_logger(__name__)


class MedicalCardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, card_number: str, patient_id: int) -> MedicalCard:
        """Create medical card for patient."""
        medical_card = MedicalCard(
            card_number=card_number,
            patient_id=patient_id
        )
        self.db.add(medical_card)
        await self.db.commit()
        await self.db.refresh(medical_card)
        logger.info(f"Created medical card: {card_number} for patient_id={patient_id}")
        return medical_card
