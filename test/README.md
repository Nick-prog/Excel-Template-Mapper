# Test Suite Documentation

This directory contains comprehensive testing infrastructure for the Excel Template Mapper project.

## Available Test Scripts

### Core Test Scripts

#### `test_imports.py`
**Purpose**: Validates all Python imports and basic functionality
- ✅ Tests all package imports (src.core, src.widgets, src.layouts)
- ✅ Validates GUI framework availability (PySide6)
- ✅ Checks core dependencies (openpyxl, json, pathlib)
- ✅ Tests model creation with proper parameters
- ✅ Validates version consistency
- ✅ Tests entry point functionality

**Usage**: `python3 test/test_imports.py` or `make test-imports`

#### `test_type_hints.py`
**Purpose**: Validates comprehensive type annotations throughout the codebase
- 🔍 Tests that all functions have proper type annotations
- 📝 Validates return type annotations
- 🎯 Checks parameter type hints
- 🔬 Optional MyPy integration for static type checking
- ✅ Ensures type safety and code quality

**Usage**: `python3 test/test_type_hints.py` or `make test-types`

#### `test_packaging.py`
**Purpose**: Validates package build and distribution process
- 🔧 Tests pyproject.toml syntax
- 📦 Validates requirements.txt dependencies
- 🎯 Tests entry point validity
- 🔨 Tests wheel and source distribution builds
- 🚀 Tests PyInstaller executable creation
- 🛠️ Checks build tool availability

**Usage**: `python3 test/test_packaging.py` or `make test-packaging`

#### `test_docker.py`
**Purpose**: Validates Docker configuration and build process
- 📁 Checks Docker file structure
- 🐳 Validates Docker Compose syntax
- 🔨 Tests Docker image build process
- 🧪 Validates container configuration

**Usage**: `python3 test/test_docker.py` or `make test-docker`

### Test Runners

#### `run_all_tests.py`
**Purpose**: Comprehensive test runner for all test suites
- 🚀 Runs all test scripts in sequence
- 📊 Provides detailed reporting with pass/fail statistics
- ⏰ Includes timing information
- 🎯 Gives overall project readiness assessment

**Usage**: `python3 test/run_all_tests.py` or `make test`

#### `pre_commit.py`
**Purpose**: Quick validation before git commits
- ⚡ Fast import testing
- 🔍 Version format validation
- 🐛 Python syntax error checking
- 🚨 Provides go/no-go for commits

**Usage**: `python3 test/pre_commit.py` or `make pre-commit`

### Legacy Development Scripts

#### `validate_project.py`
**Purpose**: Project structure and consistency validation
- 📁 Validates package structure
- 🔗 Checks import relationships
- ⚙️ Verifies configuration files

#### `setup_dev.py`
**Purpose**: Development environment setup
- 🛠️ Installs development dependencies
- ⚙️ Configures development tools
- 📝 Sets up project for development

#### `update_requirements.py`
**Purpose**: Requirements management
- 📋 Updates requirements.txt from current environment
- 🔄 Manages dependency versions
- 🧹 Cleans up unused dependencies

## Quick Reference

### Most Common Commands

```bash
# Quick validation before commit
make pre-commit

# Run all tests comprehensively
make test

# Test just imports and functionality
make test-imports

# Test type hints and annotations
make test-types

# Test packaging and build process
make test-packaging

# Test Docker configuration
make test-docker
```

### Test Results Interpretation

- ✅ **All tests passed**: Project is ready for GitHub push
- ⚠️ **Some tests failed**: Review individual test outputs and fix issues
- ❌ **Critical failures**: Import errors, syntax errors, or missing dependencies

### Troubleshooting

#### Import Errors
- Ensure you're in the project root directory
- Check that `src/` package structure is intact
- Verify all `__init__.py` files are present

#### Docker Test Failures
- Ensure Docker is installed and running
- Check Docker daemon status: `docker info`
- Verify Docker Compose is available: `docker-compose --version`

#### Packaging Test Failures
- Install build tools: `pip install build PyInstaller`
- Check Python version compatibility (3.9-3.13 supported)
- Verify pyproject.toml syntax

## Integration with Development Workflow

### Pre-commit Hook (Recommended)
```bash
# Quick check before any commit
make pre-commit
```

### Full Validation Pipeline
```bash
# Complete project validation
make test
```

### CI/CD Integration
These tests are designed to work with the GitHub Actions workflow in `.github/workflows/build-release.yml`.

## Adding New Tests

To add new test scripts:

1. Create script in `test/` directory following naming pattern `test_*.py`
2. Make script executable: `chmod +x test/test_*.py`
3. Add to `run_all_tests.py` test suites list
4. Add make target to `Makefile`
5. Update this README

## Dependencies

Test scripts have minimal dependencies:
- Python 3.9+ (matches project requirements)
- Standard library modules (subprocess, pathlib, etc.)
- Project dependencies (for functionality testing)

Optional dependencies for specific tests:
- Docker (for `test_docker.py`)
- Build tools (`build`, `PyInstaller` for `test_packaging.py`)