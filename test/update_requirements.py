#!/usr/bin/env python3
"""
Dynamic requirements generator for Excel Template Mapper.
Generates requirements.txt from current environment or pyproject.toml.
"""

import subprocess
import sys
from pathlib import Path

def get_installed_versions():
    """Get currently installed package versions."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], 
                              capture_output=True, text=True, check=True)
        return {line.split('==')[0]: line.split('==')[1] 
                for line in result.stdout.strip().split('\n') 
                if '==' in line and not line.startswith('-e')}
    except subprocess.CalledProcessError:
        return {}

def update_requirements():
    """Update requirements.txt with current versions of core dependencies."""
    
    # Core dependencies that should be pinned
    core_deps = [
        'et_xmlfile',
        'GitPython', 
        'openpyxl',
        'PySide6',
        'PySide6_Addons',
        'PySide6_Essentials', 
        'shiboken6',
    ]
    
    installed = get_installed_versions()
    requirements = []
    
    for dep in core_deps:
        if dep in installed:
            requirements.append(f"{dep}=={installed[dep]}")
        else:
            print(f"Warning: {dep} not found in current environment")
    
    # Add any additional dependencies that were installed
    additional_deps = ['gitdb', 'smmap']  # Common sub-dependencies
    for dep in additional_deps:
        if dep in installed:
            requirements.append(f"{dep}=={installed[dep]}")
    
    # Sort requirements
    requirements.sort()
    
    # Write to file
    req_file = Path(__file__).parent / "requirements.txt"
    with open(req_file, 'w') as f:
        f.write('\n'.join(requirements) + '\n')
    
    print(f"✅ Updated requirements.txt with {len(requirements)} packages")
    for req in requirements:
        print(f"  - {req}")

if __name__ == "__main__":
    update_requirements()