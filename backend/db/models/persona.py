"""
Persona model
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base


class Persona(Base):
    """
    Scholarship personality genome
    Cached analysis of scholarship values and tone
    """
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False)
    persona_name = Column(String(100), nullable=False)
    tone = Column(String(100))
    weights = Column(JSONB, nullable=False)  # {"Academics": 0.25, "Leadership": 0.40, ...}
    rationale = Column(Text)
    version = Column(Integer, default=1)  # Track re-analysis
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    scholarship = relationship("Scholarship", back_populates="personas")
    essays = relationship("Essay", back_populates="persona", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="persona", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Persona(id={self.id}, name='{self.persona_name}')>"
