from sqlalchemy import Column, Integer, String, Date, DateTime, ARRAY
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False, index=True)
    jshshir = Column(String(14), nullable=False, unique=True, index=True)  # Passport 14-digit number
    password = Column(String(6), nullable=False)  # 6-digit password (plain text)
    roles = Column(ARRAY(String), nullable=False)  # List of roles
    gender = Column(String(10), nullable=False)  # male, female
    birth_date = Column(Date, nullable=False)
    phone = Column(String(20), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, full_name={self.full_name}, jshshir={self.jshshir}, roles={self.roles})>"
