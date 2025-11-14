"""
Seed database with demo data for hackathon
Quick and simple - no complex logic
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from config.database import SessionLocal, engine, Base
from db.models import Scholarship, StudentProfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database():
    """Seed database with mock data"""

    # Create all tables first
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(Scholarship).count()
        if existing > 0:
            logger.info(f"Database already has {existing} scholarships. Skipping seed.")
            return

        # Load mock data
        data_dir = Path(__file__).parent.parent.parent / "data"
        scholarships_file = data_dir / "mock_scholarships.json"
        students_file = data_dir / "mock_student_profiles.json"

        # Seed scholarships
        if scholarships_file.exists():
            logger.info("Loading scholarships...")
            with open(scholarships_file, 'r') as f:
                scholarships = json.load(f)

            for s in scholarships:
                scholarship = Scholarship(
                    name=s["name"],
                    organization=s["organization"],
                    description=s["description"],
                    amount=s.get("amount", 0),
                    deadline=datetime.strptime(s["deadline"], "%Y-%m-%d").date() if s.get("deadline") else None,
                    criteria=s.get("criteria", ""),
                    url=s.get("url", ""),
                    meta_data={"mock": True}
                )
                db.add(scholarship)

            db.commit()
            logger.info(f"✅ Seeded {len(scholarships)} scholarships")
        else:
            logger.warning(f"Scholarships file not found: {scholarships_file}")

        # Seed student profiles
        if students_file.exists():
            logger.info("Loading student profiles...")
            with open(students_file, 'r') as f:
                students = json.load(f)

            for s in students:
                student = StudentProfile(
                    name=s["name"],
                    email=s["email"],
                    gpa=s["gpa"],
                    activities=s["activities"],
                    achievements=s["achievements"],
                    goals=s["goals"]
                )
                db.add(student)

            db.commit()
            logger.info(f"✅ Seeded {len(students)} student profiles")
        else:
            logger.warning(f"Students file not found: {students_file}")

        logger.info("✅ Database seeding complete!")

        # Show what we have
        final_count = db.query(Scholarship).count()
        student_count = db.query(StudentProfile).count()
        logger.info(f"Final counts: {final_count} scholarships, {student_count} students")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()