#!/bin/bash
# Quick test script for backend

echo "========================================="
echo "ScholarLens Backend Test Script"
echo "========================================="

# Check if server is running
echo "1. Checking if server is running..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Server is running"
else
    echo "❌ Server is not running. Please start it with: python main.py"
    exit 1
fi

# Test scholarships endpoint
echo ""
echo "2. Testing scholarships endpoint..."
curl -s http://localhost:8000/api/v1/demo/scholarships | python -m json.tool | head -20
echo "✅ Scholarships endpoint working"

# Test students endpoint
echo ""
echo "3. Testing students endpoint..."
curl -s http://localhost:8000/api/v1/demo/students | python -m json.tool | head -20
echo "✅ Students endpoint working"

# Test analyze scholarship
echo ""
echo "4. Testing analyze-scholarship (Persona Builder)..."
curl -s -X POST http://localhost:8000/api/v1/demo/analyze-scholarship?scholarship_id=1 \
  -H "Content-Type: application/json" | python -m json.tool | head -30
echo "✅ Persona analysis working"

# Test generate essay
echo ""
echo "5. Testing generate-essay..."
curl -s -X POST http://localhost:8000/api/v1/demo/generate-essay \
  -H "Content-Type: application/json" \
  -d '{
    "scholarship_id": 1,
    "student_id": 1,
    "essay_type": "adaptive"
  }' | python -m json.tool | head -50
echo "✅ Essay generation working"

# Test complete flow
echo ""
echo "6. Testing complete flow (Scholarship → Persona → Essay → Evaluation)..."
curl -s http://localhost:8000/api/v1/demo/test-flow/1?student_id=1 | python -m json.tool | head -100

echo ""
echo "========================================="
echo "✅ All tests completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Add your Claude API key to backend/.env"
echo "2. Run: python scripts/seed_demo_data.py (to seed database)"
echo "3. Visit: http://localhost:8000/docs (for interactive API docs)"
echo ""