#!/usr/bin/env python3
"""
Excel Template Mapper - Comprehensive Test Runner
Runs all test suites and provides a complete validation report.
"""

import subprocess
import sys
from pathlib import Path
import time

def run_test_script(script_name, description):
    """Run a test script and return results"""
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print(f"❌ {description} - Script not found: {script_name}")
        return False, 0, 0
    
    try:
        print(f"\n🚀 Running {description}...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        # Parse results from output (looking for test summary)
        output_lines = result.stdout.split('\n')
        passed = 0
        total = 0
        
        for line in output_lines:
            if 'Passed:' in line:
                try:
                    passed = int(line.split('Passed:')[1].strip())
                except:
                    pass
            if 'Total tests:' in line:
                try:
                    total = int(line.split('Total tests:')[1].strip())
                except:
                    pass
        
        success = result.returncode == 0
        return success, passed, total
        
    except Exception as e:
        print(f"❌ {description} - Error running test: {e}")
        return False, 0, 0

def main():
    print("🧪 Excel Template Mapper - Comprehensive Test Suite")
    print("=" * 60)
    print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define test suites
    test_suites = [
        ("test_imports.py", "Import & Functionality Tests"),
        ("test_type_hints.py", "Type Hints Validation"),
        ("test_packaging.py", "Package Build Tests"),
        ("test_docker.py", "Docker Tests"),
    ]
    
    # Run all test suites
    all_results = []
    total_passed = 0
    total_tests = 0
    
    for script, description in test_suites:
        success, passed, tests = run_test_script(script, description)
        all_results.append((description, success, passed, tests))
        total_passed += passed
        total_tests += tests
    
    # Generate comprehensive report
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 60)
    
    for description, success, passed, tests in all_results:
        status = "✅ PASS" if success else "❌ FAIL"
        if tests > 0:
            percentage = (passed / tests) * 100
            print(f"{status} {description}: {passed}/{tests} ({percentage:.1f}%)")
        else:
            print(f"{status} {description}: No test count available")
    
    print("-" * 60)
    
    if total_tests > 0:
        overall_percentage = (total_passed / total_tests) * 100
        print(f"📈 OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage:.1f}%)")
    
    # Determine overall status
    all_passed = all(result[1] for result in all_results)
    
    print("-" * 60)
    
    if all_passed:
        print("🎉 ALL TEST SUITES PASSED!")
        print("✅ Project is ready for GitHub push")
        print()
        print("🚀 Recommended next steps:")
        print("   1. git add .")
        print("   2. git commit -m 'Complete project reorganization and modernization'")
        print("   3. git push")
        return_code = 0
    else:
        print("⚠️  SOME TESTS FAILED!")
        print("❌ Please fix issues before pushing to GitHub")
        print()
        print("🔧 Troubleshooting tips:")
        print("   1. Check individual test outputs above")
        print("   2. Install missing dependencies")
        print("   3. Verify Docker is running (for Docker tests)")
        print("   4. Ensure all imports are working")
        return_code = 1
    
    print(f"\n🕐 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return return_code

if __name__ == "__main__":
    sys.exit(main())