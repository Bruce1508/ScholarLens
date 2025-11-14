"""
Database initialization script
Creates all tables and indexes
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from config.database import engine, Base
from db.models import (
    Scholarship,
    StudentProfile,
    Persona,
    Essay,
    Evaluation,
    WinnerEssayCluster,
    APILog
)


def init_database():
    """
    Initialize database - create all tables
    """
    print("Creating database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")

        # List created tables
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def drop_database():
    """
    Drop all tables (use with caution!)
    """
    confirm = input("⚠️  This will DROP ALL TABLES. Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped!")
    else:
        print("❌ Cancelled.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization")
    parser.add_argument(
        "action",
        choices=["init", "drop"],
        help="Action to perform: init (create tables) or drop (remove all tables)"
    )

    args = parser.parse_args()

    if args.action == "init":
        init_database()
    elif args.action == "drop":
        drop_database()
