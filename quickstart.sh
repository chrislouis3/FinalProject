#!/bin/bash
#
# Quick Start Script for Student Grading System
# Linux/Mac Version
#

echo ""
echo "========================================"
echo "Student Grading System - Quick Start"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate venv
echo "[2/3] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[3/3] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Starting Student Grading System..."
echo "Accessing at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Start application
python run.py
