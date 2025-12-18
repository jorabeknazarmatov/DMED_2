from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)  # male, female
    phone = Column(String(20), nullable=True)

    # Location
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="SET NULL"), nullable=True)
    address = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    region = relationship("Region", back_populates="patients")
    city = relationship("City", back_populates="patients")
    medical_card = relationship("MedicalCard", back_populates="patient", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"
