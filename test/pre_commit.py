#!/usr/bin/env python3
"""
Excel Template Mapper - Pre-commit Validation
Runs before git commits to ensure code quality and readiness.
"""

import subprocess
import sys
from pathlib import Path

def run_test_quick():
    """Run quick import tests"""
    test_script = Path(__file__).parent / "test_imports.py"
    result = subprocess.run([sys.executable, str(test_script)], capture_output=True, text=True)
    return result.returncode == 0

def check_version_consistency():
    """Check that version is consistent across files"""
    try:
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # Check _version.py (our single source of truth)
        from src._version import __version__
        
        # Check that version is a valid semantic version
        import re
        version_pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9-]+)?(?:\+[a-zA-Z0-9-]+)?$'
        if re.match(version_pattern, __version__):
            print(f"✅ Version is valid: {__version__}")
            return True
        else:
            print(f"❌ Invalid version format: {__version__}")
            return False
            
    except Exception as e:
        print(f"❌ Version check failed: {e}")
        return False

def check_no_syntax_errors():
    """Check Python files for syntax errors"""
    project_root = Path(__file__).parent.parent
    python_files = []
    
    # Find all Python files
    for pattern in ["*.py", "src/**/*.py", "test/**/*.py", "layouts/**/*.py", "widgets/**/*.py"]:
        python_files.extend(project_root.glob(pattern))
    
    errors_found = False
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                compile(f.read(), str(py_file), 'exec')
        except SyntaxError as e:
            print(f"❌ Syntax error in {py_file}: {e}")
            errors_found = True
        except Exception as e:
            print(f"⚠️  Warning in {py_file}: {e}")
    
    if not errors_found:
        print("✅ No Python syntax errors found")
        return True
    else:
        return False

def main():
    print("🚨 Excel Template Mapper - Pre-commit Validation")
    print("=" * 55)
    
    # Quick validation checks
    checks = [
        ("Import Tests", run_test_quick),
        ("Version Validation", check_version_consistency),
        ("Syntax Check", check_no_syntax_errors),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n🔍 Running {name}...")
        try:
            passed = check_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 55)
    
    if all_passed:
        print("✅ PRE-COMMIT VALIDATION PASSED")
        print("🚀 Safe to commit!")
        return 0
    else:
        print("❌ PRE-COMMIT VALIDATION FAILED")
        print("🛑 Please fix issues before committing")
        print()
        print("💡 Tips:")
        print("   - Run 'make test' for comprehensive testing")
        print("   - Check import errors and syntax issues")
        print("   - Ensure version consistency")
        return 1

if __name__ == "__main__":
    sys.exit(main())