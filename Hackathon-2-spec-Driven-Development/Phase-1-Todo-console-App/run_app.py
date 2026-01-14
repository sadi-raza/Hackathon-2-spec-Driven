#!/usr/bin/env python3
"""
Script to run the todo application by adding src to Python path.
"""

import sys
import os

# Add the project root to the Python path so absolute imports work
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now we can import and run the main module
from src.main import main

if __name__ == "__main__":
    main()