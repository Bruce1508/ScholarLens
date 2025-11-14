"""
Scholarship model
"""
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Date, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base


class Scholarship(Base):
    """
    Scholarship information table
    Stores scholarship descriptions, criteria, deadlines, etc.
    """
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    organization = Column(String(200))
    description = Column(Text, nullable=False)
    criteria = Column(Text)
    amount = Column(DECIMAL(10, 2))
    deadline = Column(Date)
    url = Column(String(500))
    meta_data = Column(JSONB)  # Flexible JSON storage (renamed from metadata)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Relationships
    personas = relationship("Persona", back_populates="scholarship", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scholarship(id={self.id}, name='{self.name}')>"
