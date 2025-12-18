from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class MedicalCard(Base):
    __tablename__ = "medical_cards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_number = Column(String(6), nullable=False, unique=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="medical_card")

    def __repr__(self):
        return f"<MedicalCard(id={self.id}, card_number={self.card_number}, patient_id={self.patient_id})>"
