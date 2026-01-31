#!/bin/bash
# Setup script for E-Paper Dashboard

set -e

echo "Setting up E-Paper Dashboard v2..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.12"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env created - please edit it with your configuration"
else
    echo "✓ .env already exists"
fi

# Check if git submodule exists
if [ ! -d "lib/e-Paper/.git" ]; then
    echo ""
    echo "⚠️  Waveshare e-Paper library not found!"
    echo "Run: git submodule add https://github.com/waveshare/e-Paper lib/e-Paper"
    echo "Or:  git submodule update --init --recursive"
else
    echo "✓ Waveshare library submodule found"
fi

echo ""
echo "=========================================="
echo "Setup complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. Run: source .venv/bin/activate"
echo "3. Run: python src/main.py"
echo ""
