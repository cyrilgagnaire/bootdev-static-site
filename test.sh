#!/usr/bin/env zsh

# Run unittest discovery for the project without pytest
# Uses the system Python executable detected on macOS Homebrew

PYTHON="/opt/homebrew/bin/python3"

if ! command -v $PYTHON >/dev/null 2>&1; then
  echo "Python executable not found at $PYTHON"
  exit 1
fi

# Run all tests under src/ (files like test_*.py)
$PYTHON -m unittest discover -s src -p "test_*.py" -v
python3 -m unittest discover -s src