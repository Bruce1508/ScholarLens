"""
Profile management routes
Handles resume upload, AI extraction, and profile CRUD operations
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from pathlib import Path

from config.database import get_db
from db.models.student_profile import StudentProfile
from api.services.file_service import file_service
from api.services.pdf_parser import pdf_parser
from api.services.ai_extractor import ai_extractor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/profiles/upload-resume")
async def upload_resume(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload a resume PDF file for a student profile

    Args:
        student_id: Student profile ID
        file: PDF file upload
        db: Database session

    Returns:
        Upload status and file info
    """
    try:
        # Verify student exists
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        # Validate and save file
        is_valid = await file_service.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid file. Must be PDF under 10MB")

        # Save file
        filename, file_path = await file_service.save_upload(file, student_id)

        # Extract text from PDF
        full_path = str(file_service.UPLOAD_DIR / file_path)
        resume_text = pdf_parser.extract_text(full_path)

        if not resume_text:
            raise HTTPException(status_code=422, detail="Could not extract text from PDF")

        # Update student profile with resume info
        student.resume_filename = filename
        student.resume_file_path = file_path
        student.raw_resume_text = resume_text[:50000]  # Limit to 50k chars
        student.profile_source = 'resume'

        db.commit()
        db.refresh(student)

        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "data": {
                "student_id": student_id,
                "filename": filename,
                "file_path": file_path,
                "text_length": len(resume_text),
                "text_preview": resume_text[:500]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/profiles/extract-from-resume/{student_id}")
async def extract_profile_from_resume(
    student_id: int,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> Dict[str, Any]:
    """
    Extract structured profile data from uploaded resume using AI

    Args:
        student_id: Student profile ID
        db: Database session
        background_tasks: Background task runner

    Returns:
        Extracted profile data
    """
    try:
        # Get student profile
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        if not student.raw_resume_text:
            raise HTTPException(
                status_code=400,
                detail="No resume text found. Please upload a resume first"
            )

        # Extract profile using AI
        extracted_data = ai_extractor.extract_profile_from_resume(student.raw_resume_text)

        # Update student profile with extracted data
        if extracted_data.get("name"):
            student.name = extracted_data["name"]
        if extracted_data.get("email"):
            student.email = extracted_data["email"]
        if extracted_data.get("phone"):
            student.phone = extracted_data["phone"]
        if extracted_data.get("gpa") is not None:
            student.gpa = extracted_data["gpa"]

        # Update JSON fields
        student.activities = extracted_data.get("activities", [])
        student.achievements = extracted_data.get("achievements", [])
        student.goals = extracted_data.get("goals", "")
        student.skills = extracted_data.get("skills", [])
        student.education = extracted_data.get("education", [])
        student.work_experience = extracted_data.get("work_experience", [])
        student.certifications = extracted_data.get("certifications", [])
        student.languages = extracted_data.get("languages", [])
        student.awards = extracted_data.get("awards", [])

        # Update metadata
        student.extraction_confidence = extracted_data.get("extraction_confidence", 0.5)
        student.last_extracted_at = datetime.utcnow()
        student.profile_source = 'ai_extracted'

        db.commit()
        db.refresh(student)

        return {
            "success": True,
            "message": "Profile extracted successfully",
            "data": {
                "student_id": student_id,
                "name": student.name,
                "email": student.email,
                "gpa": float(student.gpa) if student.gpa else None,
                "skills": student.skills,
                "education": student.education,
                "work_experience": student.work_experience,
                "activities": student.activities,
                "achievements": student.achievements,
                "extraction_confidence": float(student.extraction_confidence) if student.extraction_confidence else 0
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.get("/profiles/{student_id}")
async def get_profile(
    student_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get a student profile by ID

    Args:
        student_id: Student profile ID
        db: Database session

    Returns:
        Student profile data
    """
    try:
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        return {
            "success": True,
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
                "gpa": float(student.gpa) if student.gpa else None,
                "activities": student.activities or [],
                "achievements": student.achievements or [],
                "goals": student.goals or "",
                "skills": student.skills or [],
                "education": student.education or [],
                "work_experience": student.work_experience or [],
                "certifications": student.certifications or [],
                "languages": student.languages or [],
                "awards": student.awards or [],
                "profile_source": student.profile_source,
                "resume_filename": student.resume_filename,
                "extraction_confidence": float(student.extraction_confidence) if student.extraction_confidence else None,
                "last_extracted_at": student.last_extracted_at.isoformat() if student.last_extracted_at else None
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")


@router.put("/profiles/{student_id}")
async def update_profile(
    student_id: int,
    profile_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update a student profile (manual edits)

    Args:
        student_id: Student profile ID
        profile_data: Updated profile fields
        db: Database session

    Returns:
        Updated profile data
    """
    try:
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        # Update allowed fields
        updateable_fields = [
            "name", "email", "phone", "gpa", "activities", "achievements",
            "goals", "skills", "education", "work_experience",
            "certifications", "languages", "awards"
        ]

        for field in updateable_fields:
            if field in profile_data:
                setattr(student, field, profile_data[field])

        # Mark as manually updated
        if any(field in profile_data for field in updateable_fields):
            student.profile_source = 'manual'

        db.commit()
        db.refresh(student)

        return {
            "success": True,
            "message": "Profile updated successfully",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "updated_fields": list(profile_data.keys())
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.delete("/profiles/{student_id}/resume")
async def delete_resume(
    student_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Delete uploaded resume file and clear resume data

    Args:
        student_id: Student profile ID
        db: Database session

    Returns:
        Deletion status
    """
    try:
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        # Delete physical file if exists
        if student.resume_file_path:
            full_path = str(file_service.UPLOAD_DIR / student.resume_file_path)
            file_service.delete_file(full_path)

        # Clear resume fields
        student.resume_filename = None
        student.resume_file_path = None
        student.raw_resume_text = None

        db.commit()

        return {
            "success": True,
            "message": "Resume deleted successfully",
            "data": {
                "student_id": student_id
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete resume: {str(e)}")


@router.post("/profiles/create")
async def create_profile(
    profile_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a new student profile (for testing)

    Args:
        profile_data: Profile data
        db: Database session

    Returns:
        Created profile data
    """
    try:
        # Create new profile
        student = StudentProfile(
            name=profile_data.get("name", ""),
            email=profile_data.get("email"),
            phone=profile_data.get("phone"),
            gpa=profile_data.get("gpa"),
            activities=profile_data.get("activities", []),
            achievements=profile_data.get("achievements", []),
            goals=profile_data.get("goals", ""),
            skills=profile_data.get("skills", []),
            education=profile_data.get("education", []),
            work_experience=profile_data.get("work_experience", []),
            profile_source='manual'
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return {
            "success": True,
            "message": "Profile created successfully",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email
            }
        }

    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")