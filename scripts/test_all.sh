#!/bin/bash

echo "🧪 Running all tests for HN-TLDR microservices..."

# Test HN API Service
echo ""
echo "📰 Testing HN API Service..."
cd hn-api-service
python -m pytest test_app.py -v
cd ..

# Test Summarization Service
echo ""
echo "🤖 Testing Summarization Service..."
cd summarization-service
python -m pytest test_app.py -v
cd ..

# Test Backend API
echo ""
echo "🔄 Testing Backend API..."
cd backend-api
python -m pytest test_app.py -v
cd ..

# Test Frontend
echo ""
echo "⚛️ Testing Frontend..."
cd frontend
npm test -- --coverage --watchAll=false
cd ..

echo ""
echo "✅ All tests completed!"
