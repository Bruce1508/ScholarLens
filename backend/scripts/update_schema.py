"""
Update database schema - hackathon version
Simply drops and recreates tables (WARNING: destroys all data)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.database import engine, Base
from db.models.scholarship import Scholarship
from db.models.student_profile import StudentProfile
from db.models.persona import Persona
from db.models.essay import Essay
from db.models.evaluation import Evaluation
from db.models.api_log import APILog
from db.models.winner_cluster import WinnerEssayCluster

def update_schema():
    """
    Update database schema by dropping and recreating all tables
    WARNING: This will delete all existing data!
    """
    print("⚠️  WARNING: This will delete all existing data!")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() != 'yes':
        print("Aborted.")
        return

    print("\n🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("🔨 Creating all tables with updated schema...")
    Base.metadata.create_all(bind=engine)

    print("✅ Schema updated successfully!")
    print("\nNew fields added to StudentProfile:")
    print("  - phone")
    print("  - certifications")
    print("  - languages")
    print("  - awards")

    print("\n⚠️  Remember to re-seed the database with:")
    print("  python scripts/seed_demo_data.py")


if __name__ == "__main__":
    update_schema()