#!/usr/bin/env python3
"""
Excel Template Mapper - Import & Functionality Tests
Validates all imports, dependencies, and basic functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_import(module_name, description):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description}: {e}")
        return False

def test_models():
    """Test model creation"""
    try:
        from src.core.models import MappingSpec, SheetMapping, ColumnMapping
        
        # Test model instantiation with required parameters
        column_mapping = ColumnMapping(target="test_target")
        sheet_mapping = SheetMapping(
            target_sheet="test_sheet",
            target_headers=["header1", "header2"]
        )
        mapping_spec = MappingSpec(template_path="test_template.xlsx")
        
        print("✓ Models created successfully")
        return True
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False

def test_version_consistency():
    """Test that version information is consistent."""
    print("\n📋 Testing Version Consistency:")
    
    try:
        from src._version import __version__
        from src import __version__ as src_version
        
        if __version__ == src_version:
            print(f"✅ Version consistency: {__version__}")
            return True
        else:
            print(f"❌ Version mismatch: _version.py={__version__}, src.__init__.py={src_version}")
            return False
            
    except Exception as e:
        print(f"❌ Version test failed: {e}")
        return False

def test_entry_point():
    """Test that the main entry point works."""
    print("\n🎯 Testing Entry Point:")
    
    try:
        # Import main function
        from app_psg import main
        print("✅ Main function can be imported")
        
        # Test that it's callable (don't actually run it as it would start GUI)
        if callable(main):
            print("✅ Main function is callable")
            return True
        else:
            print("❌ Main function is not callable")
            return False
            
    except Exception as e:
        print(f"❌ Entry point test failed: {e}")
        return False

def main():
    """Run all import and basic functionality tests."""
    print("🧪 Excel Template Mapper - Import & Functionality Tests")
    print("=" * 60)
    
    # Test basic imports
    print("\n📦 Testing Package Imports:")
    
    core_imports = [
        ("src", "Main package"),
        ("src.core", "Core package"),
        ("src.core.models", "Data models"),
        ("src.core.engine", "Processing engine"),
        ("src.core.utils", "Utility functions"),
        ("src.widgets", "GUI widgets package"),
        ("src.widgets.main_window", "Main window"),
        ("src.widgets.preview_dialog", "Preview dialog"),
        ("src.widgets.mapping_table", "Mapping table"),
        ("src.widgets.transform_button", "Transform button"),
        ("src.layouts", "Layout package"),
    ]
    
    import_results = []
    for module, description in core_imports:
        import_results.append(test_import(module, description))
    
    # Test PySide6 imports
    print("\n🖥️  Testing GUI Framework:")
    gui_results = []
    gui_imports = [
        ("PySide6", "Main PySide6 package"),
        ("PySide6.QtWidgets", "Qt Widgets"),
        ("PySide6.QtCore", "Qt Core"),
        ("PySide6.QtGui", "Qt GUI"),
    ]
    
    for module, description in gui_imports:
        gui_results.append(test_import(module, description))
    
    # Test other dependencies
    print("\n📚 Testing Dependencies:")
    dep_results = []
    dep_imports = [
        ("openpyxl", "Excel file handling"),
        ("json", "JSON handling"),
        ("pathlib", "Path handling"),
    ]
    
    for module, description in dep_imports:
        dep_results.append(test_import(module, description))
    
    # Test functionality
    func_results = [
        test_version_consistency(),
        test_entry_point(),
    ]
    
    # Summary
    total_tests = len(import_results) + len(gui_results) + len(dep_results) + len(func_results)
    passed_tests = sum(import_results + gui_results + dep_results + func_results)
    
    print(f"\n📊 Test Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Project is ready.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please fix before pushing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())