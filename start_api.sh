#!/bin/bash

# Start API server on port 8000
echo "Starting Stock Market AI Chatbot API on port 8000..."
echo "API Docs will be available at: http://localhost:8000/docs"
echo ""

uvicorn api:app --host 0.0.0.0 --port 8000 --reload
