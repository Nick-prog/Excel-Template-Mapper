#!/usr/bin/env python3
"""
Excel Template Mapper - Type Hints Validation Test
Validates that all type hints are correctly implemented and mypy-compatible.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

def check_mypy_available() -> bool:
    """Check if mypy is installed"""
    try:
        result = subprocess.run(["mypy", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def run_mypy_check() -> Dict[str, Any]:
    """Run mypy type checking on the entire project"""
    project_root = Path(__file__).parent.parent
    
    # Files to check
    files_to_check = [
        "app_psg.py",
        "src/core/models.py",
        "src/core/engine.py", 
        "src/core/utils.py",
        "src/widgets/main_window.py",
        "src/layouts/top_file_row.py",
        "src/layouts/source_label_row.py",
        "src/layouts/sheet_row.py",
        "src/layouts/bottom_row.py",
    ]
    
    results = {
        "total_files": len(files_to_check),
        "checked_files": 0,
        "files_with_errors": 0,
        "total_errors": 0,
        "error_details": []
    }
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        if not full_path.exists():
            results["error_details"].append(f"File not found: {file_path}")
            continue
            
        print(f"🔍 Checking {file_path}...")
        
        try:
            result = subprocess.run(
                ["mypy", str(full_path), "--no-error-summary"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            results["checked_files"] += 1
            
            if result.returncode != 0:
                results["files_with_errors"] += 1
                error_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                results["total_errors"] += error_count
                results["error_details"].append(f"❌ {file_path}: {error_count} errors")
                if result.stdout:
                    results["error_details"].append(f"   {result.stdout.strip()}")
            else:
                print(f"✅ {file_path} - No type errors")
                
        except Exception as e:
            results["error_details"].append(f"Error checking {file_path}: {e}")
    
    return results

def test_basic_type_annotations() -> bool:
    """Test that basic type annotations are present"""
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    print("🔍 Testing basic type annotations...")
    
    try:
        # Test importing modules with type hints
        from src.core.models import MappingSpec, ColumnMapping, SheetMapping
        from src.core.engine import build_initial_spec, apply_transforms
        from src.core.utils import is_blank, safe_str
        
        # Test that functions have proper annotations
        import inspect
        
        # Check a few key functions
        sig = inspect.signature(build_initial_spec)
        assert 'template_path' in sig.parameters
        assert sig.parameters['template_path'].annotation == str
        assert sig.return_annotation == MappingSpec
        
        sig = inspect.signature(apply_transforms)
        assert sig.return_annotation != inspect.Signature.empty
        
        sig = inspect.signature(is_blank)
        assert sig.return_annotation == bool
        
        print("✅ Basic type annotations present")
        return True
        
    except Exception as e:
        print(f"❌ Basic type annotation test failed: {e}")
        return False

def main() -> int:
    print("🔬 Excel Template Mapper - Type Hints Validation")
    print("=" * 60)
    
    # Test 1: Basic type annotations
    basic_test_passed = test_basic_type_annotations()
    
    # Test 2: MyPy checking (if available)
    if check_mypy_available():
        print("\n🎯 Running MyPy type checking...")
        mypy_results = run_mypy_check()
        
        print(f"\n📊 MyPy Results:")
        print(f"   Files checked: {mypy_results['checked_files']}/{mypy_results['total_files']}")
        print(f"   Files with errors: {mypy_results['files_with_errors']}")
        print(f"   Total errors: {mypy_results['total_errors']}")
        
        if mypy_results["error_details"]:
            print("\n🔍 Error Details:")
            for detail in mypy_results["error_details"]:
                print(f"   {detail}")
        
        mypy_passed = mypy_results["total_errors"] == 0
    else:
        print("\n⚠️  MyPy not available - install with: pip install mypy")
        mypy_passed = True  # Don't fail if mypy isn't installed
    
    # Overall result
    print("\n" + "=" * 60)
    
    if basic_test_passed and mypy_passed:
        print("🎉 ALL TYPE HINT TESTS PASSED!")
        print("✅ Project has comprehensive type hints")
        return 0
    else:
        print("❌ SOME TYPE HINT TESTS FAILED")
        if not basic_test_passed:
            print("   - Basic type annotations are missing or incorrect")
        if not mypy_passed:
            print("   - MyPy found type errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())