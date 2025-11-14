"""
Student Profile model
"""
from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, CheckConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base


class StudentProfile(Base):
    """
    Student profile information
    Stores student GPA, activities, achievements, goals
    """
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # For future authentication integration
    name = Column(String(100), nullable=False)
    email = Column(String(255))
    gpa = Column(DECIMAL(3, 2))
    activities = Column(JSONB)  # Array: ["robotics", "volunteering"]
    achievements = Column(JSONB)  # Array: ["organized STEM workshop", ...]
    goals = Column(Text)

    # New fields for resume/profile extraction
    profile_source = Column(String(50), default='manual')  # 'manual', 'resume', 'ai_extracted'
    resume_filename = Column(String(255))
    resume_file_path = Column(String(500))
    raw_resume_text = Column(Text)  # Extracted text from resume

    # Enhanced profile fields from AI extraction
    phone = Column(String(20))  # Phone number
    skills = Column(JSONB)  # ["Python", "Leadership", "Public Speaking"]
    education = Column(JSONB)  # [{"school": "...", "degree": "...", "year": "..."}]
    work_experience = Column(JSONB)  # [{"company": "...", "role": "...", "duration": "..."}]
    certifications = Column(JSONB)  # ["AWS Certified", "Google Analytics"]
    languages = Column(JSONB)  # ["English (Native)", "Spanish (Fluent)"]
    awards = Column(JSONB)  # ["Dean's List 2023", "Best Hackathon Project"]

    # AI extraction metadata
    extraction_confidence = Column(DECIMAL(3, 2))  # 0.00-1.00
    last_extracted_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Constraints
    __table_args__ = (
        CheckConstraint('gpa >= 0 AND gpa <= 4.0', name='valid_gpa'),
    )

    # Relationships
    essays = relationship("Essay", back_populates="student_profile", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<StudentProfile(id={self.id}, name='{self.name}')>"
