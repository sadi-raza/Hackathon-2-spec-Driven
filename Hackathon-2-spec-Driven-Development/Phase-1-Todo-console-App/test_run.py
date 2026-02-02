#!/usr/bin/env python3
"""
Test script to run the todo application and immediately exit to verify it works.
"""

import sys
import os

# Add the project root to the Python path so absolute imports work
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Mock input to simulate exiting the application immediately
import builtins
original_input = builtins.input

def mock_input(prompt):
    print(prompt, end='')  # Show the prompt
    return "7"  # Return "7" to exit the application

# Replace input function temporarily
builtins.input = mock_input

try:
    from src.main import main
    print("Starting the Enhanced Todo Application...")
    print("(The application will exit immediately after starting)")
    main()
    print("\nApplication exited successfully.")
except Exception as e:
    print(f"\nApplication encountered an error: {e}")
    sys.exit(1)
finally:
    # Restore original input function
    builtins.input = original_input