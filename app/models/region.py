from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True, index=True)

    # Relationships
    cities = relationship("City", back_populates="region", cascade="all, delete-orphan")
    patients = relationship("Patient", back_populates="region")

    def __repr__(self):
        return f"<Region(id={self.id}, name={self.name})>"
