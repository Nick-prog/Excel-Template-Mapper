#!/usr/bin/env python3
"""
Project validation and update script for Excel Template Mapper.
Checks for inconsistencies and can automatically fix them.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional

def get_version_from_file(file_path: Path) -> Optional[str]:
    """Extract version from a Python file."""
    if not file_path.exists():
        return None
    
    content = file_path.read_text(encoding='utf-8')
    
    # Look for __version__ = "x.x.x"
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    
    # Look for version = "x.x.x" 
    version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    
    return None

def check_version_consistency() -> Dict[str, str]:
    """Check version consistency across files."""
    root = Path(__file__).parent.parent
    
    version_sources = {
        'src/_version.py': root / 'src' / '_version.py',
        'pyproject.toml': root / 'pyproject.toml',
        'setup.py': root / 'setup.py',
    }
    
    versions = {}
    for name, path in version_sources.items():
        version = get_version_from_file(path)
        if version:
            versions[name] = version
    
    return versions

def check_package_structure() -> List[str]:
    """Check if package structure is correct."""
    root = Path(__file__).parent.parent
    issues = []
    
    # Check if src structure exists
    src_dir = root / 'src'
    if not src_dir.exists():
        issues.append("src/ directory missing")
        return issues
    
    required_dirs = [
        src_dir / 'core',
        src_dir / 'widgets', 
        src_dir / 'layouts'
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            issues.append(f"Missing directory: {dir_path.relative_to(root)}")
        elif not (dir_path / '__init__.py').exists():
            issues.append(f"Missing __init__.py in: {dir_path.relative_to(root)}")
    
    # Check if main files exist
    required_files = [
        root / 'app_psg.py',
        root / 'pyproject.toml',
        root / 'requirements.txt',
        src_dir / '_version.py',
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            issues.append(f"Missing file: {file_path.relative_to(root)}")
    
    return issues

def check_entry_points() -> List[str]:
    """Check if entry points are correctly configured."""
    root = Path(__file__).parent.parent
    issues = []
    
    # Check if app_psg.py has main function
    app_file = root / 'app_psg.py'
    if app_file.exists():
        content = app_file.read_text(encoding='utf-8')
        if 'def main(' not in content:
            issues.append("app_psg.py missing main() function")
    
    return issues

def main():
    """Run all validation checks."""
    print("🔍 Excel Template Mapper - Project Validation")
    print("=" * 50)
    
    # Check version consistency
    print("\n📋 Version Consistency Check:")
    versions = check_version_consistency()
    if versions:
        unique_versions = set(versions.values())
        if len(unique_versions) == 1:
            print(f"✅ All versions consistent: {list(unique_versions)[0]}")
        else:
            print("❌ Version inconsistencies found:")
            for source, version in versions.items():
                print(f"   {source}: {version}")
    else:
        print("❌ No version information found")
    
    # Check package structure  
    print("\n📁 Package Structure Check:")
    structure_issues = check_package_structure()
    if not structure_issues:
        print("✅ Package structure looks good")
    else:
        print("❌ Package structure issues:")
        for issue in structure_issues:
            print(f"   - {issue}")
    
    # Check entry points
    print("\n🎯 Entry Points Check:")
    entry_issues = check_entry_points()
    if not entry_issues:
        print("✅ Entry points configured correctly")
    else:
        print("❌ Entry point issues:")
        for issue in entry_issues:
            print(f"   - {issue}")
    
    # Summary
    total_issues = len(structure_issues) + len(entry_issues)
    if len(set(versions.values())) > 1:
        total_issues += 1
    
    print(f"\n📊 Summary: {total_issues} issues found")
    
    if total_issues == 0:
        print("🎉 Project validation passed!")
        return 0
    else:
        print("⚠️  Project has issues that should be addressed")
        return 1

if __name__ == "__main__":
    sys.exit(main())