# 🚀 ScholarLens Backend - Quick Start Guide

## ✅ What's Ready

- ✅ Claude service với 3 functions chính (analyze, generate, compare)
- ✅ Demo API endpoints
- ✅ Mock data (5 scholarships, 3 students)
- ✅ Database models ready
- ✅ Test script

---

## 📋 Setup in 5 Minutes

### Step 1: Start PostgreSQL (Choose one)

#### Option A: Docker (Recommended)
```bash
docker run --name scholarlens-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=scholarlens_dev \
  -p 5432:5432 -d postgres:14
```

#### Option B: Use SQLite (Faster, no setup)
Change in `backend/config/database.py`:
```python
# Replace DATABASE_URL with:
DATABASE_URL = "sqlite:///./scholarlens.db"
# And change imports
```

### Step 2: Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install fastapi uvicorn anthropic sqlalchemy psycopg2-binary python-dotenv
```

### Step 3: Setup Environment
```bash
cp .env.example .env
```

**IMPORTANT: Edit `.env` and add your Claude API key:**
```
CLAUDE_API_KEY=sk-ant-xxxxx  # ← ADD YOUR KEY HERE
```

### Step 4: Initialize Database
```bash
# Create tables
python scripts/init_db.py init

# Seed with mock data
python scripts/seed_demo_data.py
```

### Step 5: Start Server
```bash
python main.py

# Or with uvicorn directly:
uvicorn main:app --reload --port 8000
```

---

## 🧪 Test Everything Works

### Quick Test
```bash
# Run test script
./test_backend.sh
```

### Manual Test
1. Open browser: http://localhost:8000/docs
2. Try these endpoints:
   - `GET /api/v1/demo/scholarships` - Get all scholarships
   - `POST /api/v1/demo/analyze-scholarship?scholarship_id=1` - Build persona
   - `POST /api/v1/demo/generate-essay` - Generate essay
   - `GET /api/v1/demo/test-flow/1?student_id=1` - Test complete flow

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api/v1/demo`

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/scholarships` | GET | Get all scholarships | - |
| `/students` | GET | Get all students | - |
| `/analyze-scholarship` | POST | Build persona for scholarship | `scholarship_id` |
| `/generate-essay` | POST | Generate adaptive/baseline essay | `{scholarship_id, student_id, essay_type}` |
| `/compare-essays` | POST | Compare two essays | `{scholarship_id, adaptive_essay, baseline_essay}` |
| `/test-flow/{id}` | GET | Test complete flow | `scholarship_id`, `student_id` |

---

## 🎯 Testing the Core Flow

### Via API Docs (Easiest)
1. Go to http://localhost:8000/docs
2. Click on endpoint
3. Click "Try it out"
4. Fill parameters
5. Click "Execute"

### Via cURL
```bash
# 1. Analyze scholarship
curl -X POST "http://localhost:8000/api/v1/demo/analyze-scholarship?scholarship_id=1"

# 2. Generate essay
curl -X POST "http://localhost:8000/api/v1/demo/generate-essay" \
  -H "Content-Type: application/json" \
  -d '{
    "scholarship_id": 1,
    "student_id": 1,
    "essay_type": "adaptive"
  }'

# 3. Test complete flow
curl "http://localhost:8000/api/v1/demo/test-flow/1?student_id=1"
```

---

## 🔍 Mock Data Available

### Scholarships (IDs 1-5):
1. STEM Leadership Excellence Award
2. Community Impact Scholarship
3. Academic Excellence Merit Scholarship
4. Innovation and Entrepreneurship Grant
5. First-Generation College Student Support Award

### Students (IDs 1-3):
1. Alex Chen - STEM focused, robotics leader
2. Maria Rodriguez - Community service focused
3. James Thompson - Academic excellence focused

---

## ⚠️ Troubleshooting

### Issue: "CLAUDE_API_KEY not found"
**Solution:** Add your API key to `.env` file

### Issue: Database connection error
**Solution:**
- Check PostgreSQL is running: `docker ps`
- Or switch to SQLite (see Option B above)

### Issue: Import errors
**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Claude API returns mock data
**Solution:** This means API key is missing or invalid. The service returns mock data for testing.

---

## 🏃 Next Steps

### Backend is Ready! Now:
1. ✅ Test all endpoints work
2. ✅ Verify Claude integration (with API key)
3. ✅ Check mock data loads correctly

### Move to Frontend:
```bash
# Create frontend
cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm run dev
```

---

## 📝 Notes for Hackathon

### What Works:
- ✅ Complete API flow
- ✅ Claude integration (with fallback to mock)
- ✅ Database persistence
- ✅ All CRUD operations

### Simplifications Made:
- No authentication
- No complex validation
- Mock data fallback if Claude fails
- Simple error handling
- No unit tests (manual testing only)

### Time to Complete Backend: ~4-6 hours

---

## 💡 Tips

1. **If Claude API fails**, the service returns mock data automatically
2. **For demo**, you can use just mock data without Claude API
3. **Database is optional** - API works with in-memory mock data
4. **CORS is wide open** for hackathon - any frontend can connect

---

## 📞 Quick Commands Cheatsheet

```bash
# Start everything
docker start scholarlens-db  # If using Docker
cd backend
source venv/bin/activate
python main.py

# Reset database
python scripts/init_db.py drop
python scripts/init_db.py init
python scripts/seed_demo_data.py

# Test
./test_backend.sh

# View logs
tail -f logs/app.log  # If logging enabled
```

---

Ready to build the frontend? The backend is fully functional! 🎉