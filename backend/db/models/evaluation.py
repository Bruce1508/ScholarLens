"""
Evaluation model
"""
from sqlalchemy import Column, Integer, Text, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base


class Evaluation(Base):
    """
    Essay evaluation results
    Compares adaptive vs baseline essays
    """
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(
        Integer,
        ForeignKey("personas.id", ondelete="CASCADE"),
        nullable=False
    )
    adaptive_essay_id = Column(
        Integer,
        ForeignKey("essays.id"),
        nullable=False
    )
    baseline_essay_id = Column(
        Integer,
        ForeignKey("essays.id"),
        nullable=False
    )
    trait_alignment = Column(JSONB)  # Adaptive scores per trait
    baseline_alignment = Column(JSONB)  # Baseline scores per trait
    alignment_gain = Column(DECIMAL(4, 3))
    tone_consistency_score = Column(DECIMAL(4, 3))
    summary = Column(Text)
    recommendation = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    persona = relationship("Persona", back_populates="evaluations")
    adaptive_essay = relationship(
        "Essay",
        foreign_keys=[adaptive_essay_id],
        back_populates="adaptive_evaluations"
    )
    baseline_essay = relationship(
        "Essay",
        foreign_keys=[baseline_essay_id],
        back_populates="baseline_evaluations"
    )

    def __repr__(self):
        return f"<Evaluation(id={self.id}, gain={self.alignment_gain})>"
