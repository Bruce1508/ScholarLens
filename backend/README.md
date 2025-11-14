# ScholarLens Backend

PostgreSQL + FastAPI backend for ScholarLens project.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env and add your DATABASE_URL and CLAUDE_API_KEY
```

### 3. Setup Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL
docker run --name scholarlens-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=scholarlens_dev \
  -p 5432:5432 \
  -d postgres:14

# Wait a few seconds for DB to start, then initialize
python scripts/init_db.py init
```

#### Option B: Local PostgreSQL

```bash
# Install PostgreSQL 14+ on your system
# macOS: brew install postgresql@14
# Ubuntu: sudo apt install postgresql-14

# Create database
createdb scholarlens_dev

# Initialize tables
python scripts/init_db.py init
```

### 4. Create Indexes

```bash
# Connect to PostgreSQL and run
psql scholarlens_dev < scripts/create_indexes.sql
```

### 5. Run Migrations (Alternative to init_db.py)

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### 6. Start Server

```bash
python main.py
# or
uvicorn main:app --reload
```

API will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
backend/
├── config/
│   └── database.py          # Database connection & session
├── db/
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── scholarship.py
│   │   ├── student_profile.py
│   │   ├── persona.py
│   │   ├── essay.py
│   │   ├── evaluation.py
│   │   ├── winner_cluster.py
│   │   └── api_log.py
│   └── migrations/          # Alembic migrations
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
├── api/
│   ├── routes/              # FastAPI route handlers (TODO: implement)
│   ├── controllers/         # Business logic (TODO: implement)
│   └── services/            # Claude API integration (TODO: implement)
├── scripts/
│   ├── init_db.py           # Database initialization
│   └── create_indexes.sql   # Index creation
├── alembic.ini              # Alembic config
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🗄️ Database Schema

### Tables

1. **scholarships** - Scholarship information
2. **student_profiles** - Student data (GPA, activities, goals)
3. **personas** - Scholarship personality genome (cached analysis)
4. **essays** - Generated or submitted essays
5. **evaluations** - Essay comparison results
6. **winner_essay_clusters** - Winner essay archetypes
7. **api_logs** - Claude API call logs

### Relationships

```
scholarships (1) → (many) personas
personas (1) → (many) essays
personas (1) → (many) evaluations
student_profiles (1) → (many) essays
essays (1) → (many) evaluations (as adaptive or baseline)
```

---

## 🛠️ Useful Commands

### Database Management

```bash
# Initialize database
python scripts/init_db.py init

# Drop all tables (CAUTION!)
python scripts/init_db.py drop

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Development

```bash
# Run server with auto-reload
uvicorn main:app --reload --port 8000

# Run tests (when implemented)
pytest

# Format code
black .

# Type checking
mypy .
```

---

## 🔧 Database Configuration

Edit `config/database.py` to customize:
- Connection pool size
- SQL echo logging
- Connection timeout

---

## 📝 Next Steps (TODO)

User needs to implement:

1. **API Routes** (`api/routes/`)
   - Scholarship CRUD
   - Persona analysis endpoints
   - Essay generation endpoints
   - Evaluation endpoints

2. **Controllers** (`api/controllers/`)
   - Business logic for each feature

3. **Services** (`api/services/`)
   - Claude API integration
   - Prompt loading and execution
   - Response validation

4. **Tests** (`tests/`)
   - Unit tests
   - Integration tests

---

## 🐛 Troubleshooting

### Database connection errors

```bash
# Check if PostgreSQL is running
docker ps  # if using Docker
# or
pg_isready

# Test connection
psql postgresql://postgres:password@localhost:5432/scholarlens_dev
```

### Import errors

```bash
# Make sure you're in backend directory
cd backend
# Activate virtual environment
source venv/bin/activate
```

### Alembic errors

```bash
# Clear migrations and start fresh
rm -rf db/migrations/versions/*.py
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
