#!/bin/bash
# Run script for the enhanced Gemini agent

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY environment variable is not set"
    echo ""
    echo "Please set it with:"
    echo "  export GEMINI_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    exit 1
fi

# Activate virtual environment and run agent
echo "🚀 Starting Gemini Agent..."
source venv/bin/activate
python3 agent.py
