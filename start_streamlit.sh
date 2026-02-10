#!/bin/bash

# Start Streamlit chatbot
echo "Starting Stock Market AI Chatbot (Streamlit)..."
echo "The app will open in your browser at: http://localhost:8501"
echo ""

cd "$(dirname "$0")"
streamlit run src/app.py
