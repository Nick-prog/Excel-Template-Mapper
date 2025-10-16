#!/usr/bin/env python3
"""
Excel Template Mapper - Docker Build Tests
Validates Docker configuration and build process.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    try:
        print(f"🔨 {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed:")
            print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def test_docker_files():
    """Test Docker file structure"""
    project_root = Path(__file__).parent.parent
    docker_files = [
        "docker/Dockerfile",
        "docker/Dockerfile.gui", 
        "docker/compose.yaml",
        "docker/compose.debug.yaml",
        "docker/run_docker_gui.sh",
    ]
    
    print("📁 Testing Docker Files:")
    all_exist = True
    for file_path in docker_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def test_docker_build():
    """Test Docker build process"""
    return run_command(
        "docker build -f docker/Dockerfile -t templatemapper:test .",
        "Docker build"
    )

def test_docker_compose_syntax():
    """Test Docker Compose file syntax"""
    return run_command(
        "docker-compose -f docker/compose.yaml config",
        "Docker Compose syntax validation"
    )

def main():
    print("🐳 Excel Template Mapper - Docker Tests")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_docker_files(),
        test_docker_compose_syntax(),
        test_docker_build(),
    ]
    
    # Summary
    total_tests = len(tests)
    passed_tests = sum(tests)
    
    print(f"\n📊 Test Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 All Docker tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())