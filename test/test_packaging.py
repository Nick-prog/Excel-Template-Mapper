#!/usr/bin/env python3
"""
Excel Template Mapper - Package Build Tests
Validates project can be built and packaged correctly.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

def run_command(cmd, description, capture_output=True):
    """Run a command and return success status"""
    try:
        print(f"📦 {description}...")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=capture_output, 
            text=True, 
            cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed:")
            if capture_output and result.stderr:
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def test_requirements_install():
    """Test that requirements can be installed"""
    with tempfile.TemporaryDirectory() as temp_dir:
        return run_command(
            f"python3 -m pip install --dry-run -r requirements.txt",
            "Requirements dependency check"
        )

def test_pyproject_toml():
    """Test pyproject.toml syntax"""
    try:
        import tomllib
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        with open(pyproject_path, 'rb') as f:
            tomllib.load(f)
        
        print("✅ pyproject.toml - Valid syntax")
        return True
    except Exception as e:
        print(f"❌ pyproject.toml - Invalid: {e}")
        return False

def test_build_wheel():
    """Test building wheel package"""
    return run_command(
        "python3 -m build --wheel --outdir /tmp/test_build",
        "Build wheel package"
    )

def test_build_sdist():
    """Test building source distribution"""
    return run_command(
        "python3 -m build --sdist --outdir /tmp/test_build",
        "Build source distribution"
    )

def test_pyinstaller():
    """Test PyInstaller can create executable"""
    return run_command(
        "python3 -m PyInstaller --onefile --windowed --distpath /tmp/test_dist app_psg.py",
        "PyInstaller executable build"
    )

def test_entry_points():
    """Test entry points are valid"""
    try:
        # Test that the main function can be imported and called
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app_psg import main
        
        # Check if function is callable
        if callable(main):
            print("✅ Entry point - Valid and callable")
            return True
        else:
            print("❌ Entry point - Not callable")
            return False
    except Exception as e:
        print(f"❌ Entry point - Import failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test build files"""
    cleanup_dirs = ["/tmp/test_build", "/tmp/test_dist"]
    for dir_path in cleanup_dirs:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path)

def main():
    print("📦 Excel Template Mapper - Package Build Tests")
    print("=" * 55)
    
    # Ensure build tools are available
    build_tools = [
        ("python3 -m pip show build", "Build tool availability"),
        ("python3 -m pip show PyInstaller", "PyInstaller availability"),
    ]
    
    print("🔧 Checking Build Tools:")
    for cmd, desc in build_tools:
        run_command(cmd, desc)
    
    print("\n📋 Running Package Tests:")
    
    # Run tests
    tests = [
        test_pyproject_toml(),
        test_requirements_install(),
        test_entry_points(),
        test_build_wheel(),
        test_build_sdist(),
        test_pyinstaller(),
    ]
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    total_tests = len(tests)
    passed_tests = sum(tests)
    
    print(f"\n📊 Test Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 All package tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())