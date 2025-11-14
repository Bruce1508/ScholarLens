"""
Demo API Routes - Simplified for Hackathon
Fast implementation, focus on working demo
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
from pathlib import Path
from datetime import datetime

from config.database import get_db
from db.models import Scholarship, StudentProfile, Persona, Essay, Evaluation
from api.services.claude_service import claude_service

router = APIRouter(prefix="/demo", tags=["demo"])

# Load mock data
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"

def load_mock_data():
    """Load mock data from JSON files"""
    scholarships_file = DATA_DIR / "mock_scholarships.json"
    students_file = DATA_DIR / "mock_student_profiles.json"

    scholarships = []
    students = []

    if scholarships_file.exists():
        with open(scholarships_file, 'r') as f:
            scholarships = json.load(f)

    if students_file.exists():
        with open(students_file, 'r') as f:
            students = json.load(f)

    return scholarships, students

# Cache mock data
MOCK_SCHOLARSHIPS, MOCK_STUDENTS = load_mock_data()

@router.get("/")
async def demo_info():
    """Get demo API information"""
    return {
        "message": "ScholarLens Demo API",
        "version": "1.0.0-hackathon",
        "endpoints": [
            "/demo/scholarships - Get all scholarships",
            "/demo/students - Get all student profiles",
            "/demo/analyze-scholarship - Build persona for scholarship",
            "/demo/generate-essay - Generate adaptive essay",
            "/demo/compare-essays - Compare two essays"
        ]
    }

@router.get("/scholarships")
async def get_scholarships(db: Session = Depends(get_db)):
    """
    Get all scholarships (from mock data or database)
    """
    # First try database
    db_scholarships = db.query(Scholarship).all()

    if db_scholarships:
        return {
            "source": "database",
            "count": len(db_scholarships),
            "scholarships": [
                {
                    "id": s.id,
                    "name": s.name,
                    "organization": s.organization,
                    "description": s.description,
                    "amount": float(s.amount) if s.amount else 0,
                    "deadline": s.deadline.isoformat() if s.deadline else None,
                    "criteria": s.criteria
                }
                for s in db_scholarships
            ]
        }

    # Fallback to mock data
    return {
        "source": "mock_data",
        "count": len(MOCK_SCHOLARSHIPS),
        "scholarships": MOCK_SCHOLARSHIPS
    }

@router.get("/students")
async def get_students():
    """
    Get all student profiles (from mock data)
    """
    return {
        "source": "mock_data",
        "count": len(MOCK_STUDENTS),
        "students": MOCK_STUDENTS
    }

@router.post("/analyze-scholarship")
async def analyze_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze a scholarship and build its persona

    Flow:
    1. Get scholarship (from DB or mock)
    2. Call Claude to analyze
    3. Save persona to DB
    4. Return persona
    """
    # Get scholarship
    scholarship = None

    # Try database first
    db_scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()

    if db_scholarship:
        scholarship = {
            "id": db_scholarship.id,
            "name": db_scholarship.name,
            "description": db_scholarship.description
        }
    else:
        # Try mock data
        for mock in MOCK_SCHOLARSHIPS:
            if mock["id"] == scholarship_id:
                scholarship = mock
                break

    if not scholarship:
        raise HTTPException(status_code=404, detail=f"Scholarship {scholarship_id} not found")

    # Check if persona already exists
    existing_persona = db.query(Persona).filter(
        Persona.scholarship_id == scholarship_id
    ).first()

    if existing_persona:
        return {
            "message": "Persona already exists",
            "cached": True,
            "persona": {
                "id": existing_persona.id,
                "persona_name": existing_persona.persona_name,
                "tone": existing_persona.tone,
                "weights": existing_persona.weights,
                "rationale": existing_persona.rationale,
                "scholarship_id": existing_persona.scholarship_id
            }
        }

    # Analyze with Claude
    persona_result = claude_service.analyze_persona(scholarship["description"])

    # Save to database if we have a DB scholarship
    if db_scholarship:
        new_persona = Persona(
            scholarship_id=scholarship_id,
            persona_name=persona_result["persona_name"],
            tone=persona_result["tone"],
            weights=persona_result["weights"],
            rationale=persona_result["rationale"],
            version=1
        )

        db.add(new_persona)
        db.commit()
        db.refresh(new_persona)

        persona_result["id"] = new_persona.id
        persona_result["scholarship_id"] = scholarship_id

    return {
        "message": "Persona analyzed successfully",
        "cached": False,
        "scholarship_name": scholarship["name"],
        "persona": persona_result
    }

@router.post("/generate-essay")
async def generate_essay(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Generate adaptive essay

    Request body:
    {
        "scholarship_id": int,
        "student_id": int,
        "essay_type": "adaptive" or "baseline"
    }
    """
    scholarship_id = request.get("scholarship_id")
    student_id = request.get("student_id")
    essay_type = request.get("essay_type", "adaptive")

    # Get scholarship persona
    persona = db.query(Persona).filter(
        Persona.scholarship_id == scholarship_id
    ).first()

    if not persona and essay_type == "adaptive":
        # Try to build persona first
        scholarship = None
        for mock in MOCK_SCHOLARSHIPS:
            if mock["id"] == scholarship_id:
                scholarship = mock
                break

        if scholarship:
            persona_result = claude_service.analyze_persona(scholarship["description"])
            persona_dict = {
                "persona_name": persona_result["persona_name"],
                "tone": persona_result["tone"],
                "weights": persona_result["weights"]
            }
        else:
            raise HTTPException(status_code=404, detail="Scholarship not found")
    elif persona:
        persona_dict = {
            "persona_name": persona.persona_name,
            "tone": persona.tone,
            "weights": persona.weights
        }
    else:
        # Baseline essay - use generic persona
        persona_dict = {
            "persona_name": "Generic Scholar",
            "tone": "Professional and Academic",
            "weights": {
                "Academics": 0.40,
                "Leadership": 0.20,
                "Community": 0.20,
                "Innovation": 0.10,
                "FinancialNeed": 0.05,
                "Research": 0.05
            }
        }

    # Get student profile
    student = None
    for mock in MOCK_STUDENTS:
        if mock["id"] == student_id:
            student = mock
            break

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Generate essay
    if essay_type == "adaptive":
        essay_result = claude_service.generate_essay(persona_dict, student)
    else:
        # For baseline, use generic approach
        essay_result = claude_service.generate_essay(persona_dict, student)
        essay_result["tone_used"] = "Generic Academic"

    # Optionally save to database
    if persona and student:
        # Get or create student profile in DB
        db_student = db.query(StudentProfile).filter(
            StudentProfile.email == student["email"]
        ).first()

        if not db_student:
            db_student = StudentProfile(
                name=student["name"],
                email=student["email"],
                gpa=student["gpa"],
                activities=student["activities"],
                achievements=student["achievements"],
                goals=student["goals"]
            )
            db.add(db_student)
            db.commit()
            db.refresh(db_student)

        # Save essay
        new_essay = Essay(
            student_profile_id=db_student.id,
            persona_id=persona.id if persona else 1,  # Use 1 as default for baseline
            essay_type=essay_type,
            paragraphs=essay_result["essay"],
            tone_used=essay_result["tone_used"],
            overall_alignment=essay_result["overall_alignment"],
            summary=essay_result["summary"]
        )

        db.add(new_essay)
        db.commit()
        db.refresh(new_essay)

        essay_result["essay_id"] = new_essay.id

    return {
        "message": f"{essay_type.capitalize()} essay generated successfully",
        "student_name": student["name"],
        "essay_type": essay_type,
        "essay": essay_result
    }

@router.post("/compare-essays")
async def compare_essays(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Compare adaptive vs baseline essays

    Request body:
    {
        "scholarship_id": int,
        "adaptive_essay": [...],  # Array of paragraphs or essay_id
        "baseline_essay": [...]   # Array of paragraphs or essay_id
    }
    """
    scholarship_id = request.get("scholarship_id")
    adaptive_input = request.get("adaptive_essay")
    baseline_input = request.get("baseline_essay")

    # Get persona
    persona = db.query(Persona).filter(
        Persona.scholarship_id == scholarship_id
    ).first()

    if not persona:
        # Try mock data
        scholarship = None
        for mock in MOCK_SCHOLARSHIPS:
            if mock["id"] == scholarship_id:
                scholarship = mock
                break

        if scholarship:
            persona_result = claude_service.analyze_persona(scholarship["description"])
            persona_dict = {
                "persona_name": persona_result["persona_name"],
                "tone": persona_result["tone"],
                "weights": persona_result["weights"]
            }
        else:
            raise HTTPException(status_code=404, detail="Scholarship not found")
    else:
        persona_dict = {
            "persona_name": persona.persona_name,
            "tone": persona.tone,
            "weights": persona.weights
        }

    # Handle essay inputs (could be arrays or IDs)
    if isinstance(adaptive_input, int):
        # It's an essay ID
        adaptive_essay = db.query(Essay).filter(Essay.id == adaptive_input).first()
        if adaptive_essay:
            adaptive_paragraphs = [p["paragraph"] for p in adaptive_essay.paragraphs]
        else:
            raise HTTPException(status_code=404, detail="Adaptive essay not found")
    else:
        # It's already an array
        adaptive_paragraphs = adaptive_input

    if isinstance(baseline_input, int):
        baseline_essay = db.query(Essay).filter(Essay.id == baseline_input).first()
        if baseline_essay:
            baseline_paragraphs = [p["paragraph"] for p in baseline_essay.paragraphs]
        else:
            raise HTTPException(status_code=404, detail="Baseline essay not found")
    else:
        baseline_paragraphs = baseline_input

    # Compare essays
    evaluation_result = claude_service.compare_essays(
        persona_dict,
        adaptive_paragraphs,
        baseline_paragraphs
    )

    # Optionally save evaluation to DB
    if persona:
        new_evaluation = Evaluation(
            persona_id=persona.id,
            adaptive_essay_id=adaptive_input if isinstance(adaptive_input, int) else None,
            baseline_essay_id=baseline_input if isinstance(baseline_input, int) else None,
            trait_alignment=evaluation_result["trait_alignment"],
            baseline_alignment=evaluation_result["baseline_alignment"],
            alignment_gain=evaluation_result["alignment_gain"],
            tone_consistency_score=evaluation_result["tone_consistency_score"],
            summary=evaluation_result["summary"],
            recommendation=evaluation_result["recommendation"]
        )

        db.add(new_evaluation)
        db.commit()
        db.refresh(new_evaluation)

        evaluation_result["evaluation_id"] = new_evaluation.id

    return {
        "message": "Essays compared successfully",
        "scholarship_id": scholarship_id,
        "evaluation": evaluation_result
    }

@router.get("/test-flow/{scholarship_id}")
async def test_complete_flow(
    scholarship_id: int,
    student_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Test complete flow: Scholarship → Persona → Essay → Evaluation
    Quick way to test everything works
    """
    results = {}

    # Step 1: Analyze scholarship
    try:
        persona_response = await analyze_scholarship(scholarship_id, db)
        results["persona"] = persona_response
    except Exception as e:
        results["persona_error"] = str(e)
        return results

    # Step 2: Generate adaptive essay
    try:
        adaptive_request = {
            "scholarship_id": scholarship_id,
            "student_id": student_id,
            "essay_type": "adaptive"
        }
        adaptive_response = await generate_essay(adaptive_request, db)
        results["adaptive_essay"] = adaptive_response
    except Exception as e:
        results["adaptive_essay_error"] = str(e)
        return results

    # Step 3: Generate baseline essay
    try:
        baseline_request = {
            "scholarship_id": scholarship_id,
            "student_id": student_id,
            "essay_type": "baseline"
        }
        baseline_response = await generate_essay(baseline_request, db)
        results["baseline_essay"] = baseline_response
    except Exception as e:
        results["baseline_essay_error"] = str(e)
        return results

    # Step 4: Compare essays
    try:
        compare_request = {
            "scholarship_id": scholarship_id,
            "adaptive_essay": [p["paragraph"] for p in adaptive_response["essay"]["essay"]],
            "baseline_essay": [p["paragraph"] for p in baseline_response["essay"]["essay"]]
        }
        evaluation_response = await compare_essays(compare_request, db)
        results["evaluation"] = evaluation_response
    except Exception as e:
        results["evaluation_error"] = str(e)

    return {
        "message": "Complete flow test finished",
        "success": "evaluation" in results,
        "results": results
    }