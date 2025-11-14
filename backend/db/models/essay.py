"""
Essay model
"""
from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base


class Essay(Base):
    """
    Generated or submitted essays
    Stores essay paragraphs with focus tags and alignment scores
    """
    __tablename__ = "essays"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(
        Integer,
        ForeignKey("student_profiles.id", ondelete="CASCADE"),
        nullable=False
    )
    persona_id = Column(
        Integer,
        ForeignKey("personas.id", ondelete="CASCADE"),
        nullable=False
    )
    essay_type = Column(String(20))  # 'adaptive', 'baseline', 'user_submitted'
    paragraphs = Column(JSONB, nullable=False)  # Array of {paragraph, focus, reason, alignment_score}
    tone_used = Column(String(100))
    overall_alignment = Column(DECIMAL(4, 3))
    summary = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "essay_type IN ('adaptive', 'baseline', 'user_submitted')",
            name='valid_essay_type'
        ),
    )

    # Relationships
    student_profile = relationship("StudentProfile", back_populates="essays")
    persona = relationship("Persona", back_populates="essays")
    adaptive_evaluations = relationship(
        "Evaluation",
        foreign_keys="Evaluation.adaptive_essay_id",
        back_populates="adaptive_essay"
    )
    baseline_evaluations = relationship(
        "Evaluation",
        foreign_keys="Evaluation.baseline_essay_id",
        back_populates="baseline_essay"
    )

    def __repr__(self):
        return f"<Essay(id={self.id}, type='{self.essay_type}')>"
