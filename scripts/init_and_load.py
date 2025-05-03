import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Run a shell command and print its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result.returncode == 0

def install_requirements():
    """Install required Python packages."""
    print("Installing required packages...")
    requirements_cmd = "pip install -r requirements.txt"
    if not run_command(requirements_cmd):
        print("Error installing requirements")
        return False
    return True

def main():
    print("Starting database initialization and data loading...")
    
    # Step 0: Install requirements
    if not install_requirements():
        return
    
    # Step 1: Initialize the database
    print("\n1. Initializing database...")
    init_cmd = "python scripts/init_db.py"
    if not run_command(init_cmd):
        print("Error initializing database")
        return
    
    # Step 2: Load the data
    print("\n2. Loading data...")
    load_cmd = "python scripts/load_data.py"
    if not run_command(load_cmd):
        print("Error loading data")
        return
    
    print("\nDatabase initialization and data loading completed successfully!")

if __name__ == "__main__":
    main() 