#!/usr/bin/env python3
"""
Development environment setup script for Excel Template Mapper.
Creates virtual environment, installs dependencies, and sets up development tools.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def create_venv(venv_path):
    """Create a virtual environment."""
    print(f"Creating virtual environment at {venv_path}")
    venv.create(venv_path, with_pip=True)

def get_venv_python(venv_path):
    """Get the Python executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return venv_path / 'Scripts' / 'python.exe'
    else:  # Unix/Linux/macOS
        return venv_path / 'bin' / 'python'

def main():
    """Set up the development environment."""
    print("🚀 Excel Template Mapper - Development Setup")
    print("=" * 50)
    
    root_dir = Path(__file__).parent.parent
    venv_path = root_dir / 'venv'
    python_exe = get_venv_python(venv_path)
    
    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        create_venv(venv_path)
    else:
        print(f"\n✅ Virtual environment already exists at {venv_path}")
    
    # Upgrade pip
    print("\n⬆️  Upgrading pip...")
    run_command([str(python_exe), '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    # Install the package in development mode
    print("\n📥 Installing package in development mode...")
    run_command([str(python_exe), '-m', 'pip', 'install', '-e', '.'], cwd=root_dir)
    
    # Install development dependencies
    print("\n🛠️  Installing development dependencies...")
    run_command([str(python_exe), '-m', 'pip', 'install', '-e', '.[dev,test]'], cwd=root_dir)
    
    # Validate the setup
    print("\n✅ Validating setup...")
    validation_script = root_dir / 'scripts' / 'validate_project.py'
    if validation_script.exists():
        run_command([str(python_exe), str(validation_script)], check=False)
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print(f"1. Activate the virtual environment:")
    if os.name == 'nt':
        print(f"   {venv_path}\\Scripts\\activate")
    else:
        print(f"   source {venv_path}/bin/activate")
    print("2. Run the application:")
    print("   python app_psg.py")
    print("3. Or use the Makefile:")
    print("   make run")

if __name__ == "__main__":
    main()