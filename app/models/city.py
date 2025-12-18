from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    region = relationship("Region", back_populates="cities")
    patients = relationship("Patient", back_populates="city")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, region_id={self.region_id})>"
