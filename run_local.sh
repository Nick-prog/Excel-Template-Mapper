#!/bin/bash

# Template Mapper - Local Run Script
# This script runs the Template Mapper GUI application locally (outside of Docker)

echo "🚀 Starting Template Mapper Application..."
echo "📁 Working directory: $(pwd)"

# Change to the project directory (in case script is run from elsewhere)
cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

echo "🐍 Python version: $(python3 --version)"

# Check if required dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import PySide6" 2>/dev/null; then
    echo "❌ Error: PySide6 is not installed. Please install dependencies first:"
    echo "   pip3 install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies check passed"

# Run the application
echo "🎯 Launching Template Mapper GUI..."
python3 app_psg.py

echo "👋 Template Mapper application closed"