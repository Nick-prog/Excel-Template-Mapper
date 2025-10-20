#!/usr/bin/env python3
"""
Template Mapper - Setup Script
Cross-platform installer and executable builder for Template Mapper application.
"""

import sys
import os
import platform
import subprocess
import shutil
from pathlib import Path

# Conditional import of setuptools components (only needed for install command)
SETUPTOOLS_AVAILABLE = False
try:
    from setuptools import setup, find_packages
    from setuptools.command.build_py import build_py
    from setuptools.command.install import install
    SETUPTOOLS_AVAILABLE = True
except ImportError:
    # setuptools not available - only executable creation will work
    setup = find_packages = build_py = install = None

# Application metadata
APP_NAME = "Template Mapper"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A GUI application for mapping and transforming templates"
APP_AUTHOR = "Template Mapper Team"
APP_EMAIL = "support@templatemapper.com"
MAIN_SCRIPT = "app_psg.py"

# Get the directory containing this script
ROOT_DIR = Path(__file__).parent.absolute()
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"

def get_requirements():
    """Read requirements from requirements.txt"""
    if REQUIREMENTS_FILE.exists():
        with open(REQUIREMENTS_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def check_python_version():
    """Check if Python version is compatible"""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"ERROR: Python {min_version[0]}.{min_version[1]}+ is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        sys.exit(1)
    
    print(f"SUCCESS: Python version check passed: {sys.version.split()[0]}")

def install_requirements():
    """Check required packages (without installing globally)"""
    requirements = get_requirements()
    if not requirements:
        print("INFO:  No requirements.txt found, skipping dependency check")
        return True
    
    print("Checking dependencies...")
    missing_packages = []
    
    # Package name mapping (pip name -> import name)
    package_mapping = {
        'GitPython': 'git',
        'PySide6_Addons': 'PySide6',  # Part of PySide6
        'PySide6_Essentials': 'PySide6',  # Part of PySide6
        'et_xmlfile': 'et_xmlfile',
        'openpyxl': 'openpyxl',
        'PySide6': 'PySide6',
        'shiboken6': 'shiboken6',
        'gitdb': 'gitdb',
        'smmap': 'smmap'
    }
    
    for req in requirements:
        # Parse package name (handle version specifiers)
        package_name = req.split('>=')[0].split('==')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0]
        
        # Get import name
        import_name = package_mapping.get(package_name, package_name.replace('-', '_'))
        
        try:
            __import__(import_name)
            print(f"FOUND: {req}")
        except ImportError:
            # For PySide6 addons/essentials, check if base PySide6 is available
            if package_name in ['PySide6_Addons', 'PySide6_Essentials']:
                try:
                    __import__('PySide6')
                    print(f"FOUND: {req} (via PySide6)")
                    continue
                except ImportError:
                    pass
            missing_packages.append(req)
            print(f"MISSING: {req}")
    
    if missing_packages:
        print(f"\nMISSING {len(missing_packages)} required package(s):")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\nPlease install dependencies first:")
        print("   Option 1: pip install -r requirements.txt")
        print("   Option 2: python setup.py install")
        print("   Option 3: Use a virtual environment with dependencies")
        return False
    
    print("SUCCESS: All dependencies are available!")
    return True

def create_executable():
    """Create executable using PyInstaller - minimal build with only essential files"""
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("SUCCESS: PyInstaller found")
    except ImportError:
        print("ERROR: PyInstaller not found")
        print("Please install PyInstaller first:")
        print("   pip install pyinstaller")
        return False
    
    print("Creating minimal executable with only essential files...")
    
    # Determine platform-specific settings
    system = platform.system().lower()
    
    # Base PyInstaller command with minimal inclusions
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--name={APP_NAME.replace(' ', '-')}",
        "--clean",
        "--noconfirm",  # Overwrite without asking
        
        # Only include essential modules - exclude unnecessary packages
        "--exclude-module=matplotlib",
        "--exclude-module=numpy.distutils",
        "--exclude-module=scipy",
        "--exclude-module=PIL.ImageTk",
        "--exclude-module=tkinter",
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=doctest",
        "--exclude-module=pdb",
        "--exclude-module=pydoc",
        "--exclude-module=email.mime",
        "--exclude-module=email.message",
        
        # Include essential modules that might be missed
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets", 
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=openpyxl",
        "--hidden-import=openpyxl.workbook",
        "--hidden-import=openpyxl.worksheet",
        "--hidden-import=openpyxl.xml",
        "--hidden-import=openpyxl.xml.functions",
        "--hidden-import=xml.etree.ElementTree",
        "--hidden-import=xml.etree",
        "--hidden-import=xml",
        
        # Add source directory to path
        "--add-data=src:src",
    ]
    
    # Platform-specific optimizations (only if files exist)
    if system == "windows":
        icon_path = ROOT_DIR / "icon.ico"
        if icon_path.exists():
            cmd.append(f"--icon={icon_path}")
    elif system == "darwin":  # macOS
        icon_path = ROOT_DIR / "icon.icns"
        if icon_path.exists():
            cmd.append(f"--icon={icon_path}")
        cmd.append("--osx-bundle-identifier=com.templatemapper.app")
    elif system == "linux":
        icon_path = ROOT_DIR / "icon.png"
        if icon_path.exists():
            cmd.append(f"--icon={icon_path}")
    
    # Add the main script
    cmd.append(MAIN_SCRIPT)
    
    try:
        subprocess.check_call(cmd, cwd=ROOT_DIR)
        print(f"SUCCESS: Executable created successfully!")
        
        # Clean up build artifacts - keep only the final executable
        cleanup_build_artifacts()
        
        # Find the executable
        dist_dir = ROOT_DIR / "dist"
        if system == "windows":
            exe_name = f"{APP_NAME.replace(' ', '-')}.exe"
        else:
            exe_name = APP_NAME.replace(' ', '-')
        
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            # Fix macOS executable permissions and security
            if system == "darwin":  # macOS
                print("Fixing macOS permissions and security...")
                try:
                    # Make executable
                    import stat
                    exe_path.chmod(exe_path.stat().st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP)
                    
                    # Remove quarantine attribute (macOS security feature)
                    subprocess.run(["xattr", "-d", "com.apple.quarantine", str(exe_path)], 
                                 capture_output=True, check=False)
                    
                    print("   SUCCESS: Executable permissions set")
                    print("   SUCCESS: Quarantine attribute removed")
                    print("   You can now double-click the executable to run it")
                except Exception as e:
                    print(f"   WARNING: Permission fix warning: {e}")
            
            print(f"Executable location: {exe_path}")
            print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Test if executable can run (basic check)
            if system == "darwin":
                print("Testing executable...")
                try:
                    # Just check if it's a valid executable (don't actually run GUI)
                    result = subprocess.run([str(exe_path), "--help"], 
                                          capture_output=True, timeout=5, check=False)
                    if result.returncode != 0:
                        print("   WARNING: Executable may have issues - try running manually")
                    else:
                        print("   SUCCESS: Executable appears to be working")
                except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                    print(f"   WARNING: Could not test executable: {e}")
                    
        else:
            print(f"WARNING: Executable not found at expected location: {exe_path}")
            # List what's actually in dist
            if dist_dir.exists():
                print(f"Contents of {dist_dir}:")
                for item in dist_dir.iterdir():
                    print(f"   {item.name}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create executable: {e}")
        return False

def cleanup_build_artifacts():
    """Remove unnecessary build artifacts, keep only the final executable"""
    print("Cleaning up build artifacts...")
    
    # Remove build directory
    build_dir = ROOT_DIR / "build"
    if build_dir.exists():
        import shutil
        shutil.rmtree(build_dir)
        print("   SUCCESS: Removed build/ directory")
    
    # Remove .spec file
    spec_files = list(ROOT_DIR.glob("*.spec"))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"   SUCCESS: Removed {spec_file.name}")
    
    # Remove __pycache__ directories
    for pycache_dir in ROOT_DIR.rglob("__pycache__"):
        if pycache_dir.is_dir():
            import shutil
            shutil.rmtree(pycache_dir)
    
    print("   SUCCESS: Build cleanup completed")

def setup_development_environment():
    """Setup development environment"""
    print("Setting up development environment...")
    
    # Create virtual environment if it doesn't exist
    venv_dir = ROOT_DIR / "venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    
    # Determine activation script path
    system = platform.system().lower()
    if system == "windows":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        pip_path = venv_dir / "bin" / "pip"
    
    print(f"SUCCESS: Virtual environment ready at: {venv_dir}")
    print(f"TIP: Activate with: {activate_script}")
    
    return True

# Define custom classes only if setuptools is available
if SETUPTOOLS_AVAILABLE:
    class CustomBuildPy(build_py):
        """Custom build command"""
        def run(self):
            check_python_version()
            super().run()

    class CustomInstall(install):
        """Custom install command that actually installs dependencies"""
        def run(self):
            check_python_version()
            
            # For explicit install command, actually install packages
            requirements = get_requirements()
            if requirements:
                print("PACKAGE: Installing dependencies...")
                for req in requirements:
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", req])
                        print(f"SUCCESS: Installed: {req}")
                    except subprocess.CalledProcessError as e:
                        print(f"ERROR: Failed to install {req}: {e}")
                        sys.exit(1)
            
            super().run()
else:
    # Dummy classes when setuptools is not available
    CustomBuildPy = CustomInstall = None

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description=f"{APP_NAME} Setup - Non-invasive executable builder")
    parser.add_argument("command", nargs="?", choices=["executable", "dev"], 
                       default="executable", help="Setup command to run (no package installation)")
    parser.add_argument("--force", action="store_true", help="Force rebuild")
    
    # If called without arguments, default to building executable
    if len(sys.argv) == 1:
        sys.argv.append("executable")
    
    # Handle custom commands (block any installation attempts)
    if len(sys.argv) > 1 and sys.argv[1] in ["executable", "dev", "install", "build"]:
        command = sys.argv[1]
        
        print(f"{APP_NAME} Setup")
        print(f"Platform: {platform.system()} {platform.machine()}")
        print(f"Python: {sys.version.split()[0]}")
        print("-" * 50)
        
        check_python_version()
        
        if command == "executable":
            if not install_requirements():
                sys.exit(1)
            if not create_executable():
                sys.exit(1)
        elif command == "dev":
            setup_development_environment()
            if not install_requirements():
                sys.exit(1)
        elif command in ["install", "build"]:
            # Completely disable installation - redirect to manual installation
            print("BLOCKED: Package installation disabled to protect your environment!")
            print("TIP: To install dependencies manually, use:")
            print("   pip install -r requirements.txt")
            print("   pip install pyinstaller")
            print("\nTIP: Or use a virtual environment:")
            print("   python -m venv venv")
            print("   source venv/bin/activate  # Linux/macOS")
            print("   # venv\\Scripts\\activate     # Windows")
            print("   pip install -r requirements.txt pyinstaller")
            print("\nTARGET: Then run: python setup.py executable")
            print("TARGET: This setup.py is ONLY for building executables - no package management!")
            sys.exit(0)
        
        if command in ["executable", "dev"]:
            print("-" * 50)
            print("SUCCESS: Setup completed successfully!")
            return
    
    # Completely disable setuptools installation - setup.py is now ONLY for executable creation
    print("BLOCKED: Direct setuptools installation disabled!")
    print("TIP: This setup.py only creates executables - no package installation.")
    print("TIP: Use 'python setup.py executable' to build standalone executable.")
    print("TIP: Use 'pip install -r requirements.txt' to install dependencies manually.")
    sys.exit(0)

if __name__ == "__main__":
    main()