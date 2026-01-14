#!/usr/bin/env python3
"""
Enhanced Todo Console Application - Main Entry Point

This module implements the command-line interface for the enhanced todo application.
It includes priority management, tagging, search, filter, and sort capabilities.
"""
from src.cli.ui import TodoCLI


def main():
    """
    Main application entry point for the enhanced Todo Application.
    """
    print("Welcome to the Enhanced Todo Application!")
    print("This application includes priority management, tagging, search, filter, and sort capabilities.")

    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()