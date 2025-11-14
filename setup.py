"""
Setup script for first-time installation.
This script helps set up the test environment quickly.
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"{description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def check_venv():
    """Check if we're in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )


def main():
    """Main setup function."""
    print_header("DITTO MUSIC TEST SUITE - SETUP")
    
    # Check if in virtual environment
    if not check_venv():
        print("WARNING: Not running in a virtual environment!")
        print("It's recommended to create and activate a virtual environment first:")
        print("  python -m venv venv")
        print("  .\\venv\\Scripts\\Activate.ps1  (Windows PowerShell)")
        print("  source venv/bin/activate      (Linux/Mac)")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return 1
    else:
        print("Virtual environment detected")
    
    print_header("INSTALLING DEPENDENCIES")
    
    # Install Python packages
    if not run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    ):
        return 1
    
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    ):
        return 1
    
    print_header("INSTALLING PLAYWRIGHT BROWSERS")
    
    # Install Playwright browsers
    if not run_command(
        f"{sys.executable} -m playwright install",
        "Installing Playwright browsers"
    ):
        return 1
    
    print_header("CREATING DIRECTORIES")
    
    # Create necessary directories
    dirs = ["test-results/screenshots", "test-results/traces", "test-results/videos"]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("Created test results directories")
    
    print_header("SETUP COMPLETE!")
    
    print("Your test environment is ready!")
    print()
    print("Next steps:")
    print("  1. Run tests: pytest -q")
    print("  2. Run with browser visible: pytest --headed -v")
    print("  3. Run demo: python run_demo.py")
    print()
    print("For more commands, see COMMANDS.md")
    print("For detailed documentation, see README.md")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
