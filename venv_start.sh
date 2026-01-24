#!/bin/bash

# venv_start.sh - Easy virtual environment activation script

VENV_DIR=".venv"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$PROJECT_ROOT/$VENV_DIR"
    echo "Virtual environment created at $PROJECT_ROOT/$VENV_DIR"
    
    echo "Activating virtual environment..."
    source "$PROJECT_ROOT/$VENV_DIR/bin/activate"
    
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r "$PROJECT_ROOT/requirements.txt"
    
    echo "Setup complete!"
else
    echo "Activating existing virtual environment..."
    source "$PROJECT_ROOT/$VENV_DIR/bin/activate"
fi

echo "Virtual environment activated. Python location: $(which python)"
echo "To deactivate, run: deactivate"