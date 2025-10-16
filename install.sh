#!/bin/bash

# Excel Template Mapper - Installation Script
# Works for both virtual environment and system installation

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect if we're in a virtual environment
detect_environment() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        ENV_TYPE="virtualenv"
        PYTHON_CMD="python"
        PIP_CMD="pip"
        ENV_PATH="$VIRTUAL_ENV"
    elif [[ -f "./venv/bin/activate" ]]; then
        ENV_TYPE="local_venv"
        PYTHON_CMD="./venv/bin/python"
        PIP_CMD="./venv/bin/pip"
        ENV_PATH="./venv"
    elif command -v python3 &> /dev/null; then
        ENV_TYPE="system"
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
        ENV_PATH=""
    else
        print_error "No Python installation found"
        exit 1
    fi
    
    print_status "Detected environment: $ENV_TYPE"
    if [[ -n "$ENV_PATH" ]]; then
        print_status "Environment path: $ENV_PATH"
    fi
}

# Install requirements
install_requirements() {
    print_status "Installing Python requirements..."
    
    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    case $ENV_TYPE in
        "virtualenv"|"local_venv")
            print_status "Installing in virtual environment..."
            $PIP_CMD install -r requirements.txt
            ;;
        "system")
            print_warning "Installing system-wide (you may need sudo)"
            if command -v sudo &> /dev/null; then
                sudo $PIP_CMD install -r requirements.txt
            else
                $PIP_CMD install -r requirements.txt
            fi
            ;;
    esac
    
    print_success "Requirements installed successfully"
}

# Install development dependencies
install_dev_requirements() {
    print_status "Installing development requirements..."
    
    # Check if setup.py or pyproject.toml exists for editable install
    if [[ -f "setup.py" ]] || [[ -f "pyproject.toml" ]]; then
        case $ENV_TYPE in
            "virtualenv"|"local_venv")
                print_status "Installing package in development mode..."
                $PIP_CMD install -e ".[dev,test]" 2>/dev/null || $PIP_CMD install -e .
                ;;
            "system")
                print_warning "Installing package system-wide in development mode..."
                if command -v sudo &> /dev/null; then
                    sudo $PIP_CMD install -e ".[dev,test]" 2>/dev/null || sudo $PIP_CMD install -e .
                else
                    $PIP_CMD install -e ".[dev,test]" 2>/dev/null || $PIP_CMD install -e .
                fi
                ;;
        esac
    else
        print_warning "No setup.py or pyproject.toml found, skipping development install"
    fi
    
    print_success "Development requirements installed"
}

# Create virtual environment if needed
create_venv() {
    if [[ ! -d "./venv" ]]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
        print_status "To activate: source venv/bin/activate"
    else
        print_status "Virtual environment already exists"
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python imports
    if $PYTHON_CMD -c "import PySide6; import openpyxl; print('All imports successful')" 2>/dev/null; then
        print_success "All required packages are importable"
    else
        print_error "Some packages failed to import"
        return 1
    fi
    
    # Test application startup (dry run)
    if [[ -f "app_psg.py" ]]; then
        if $PYTHON_CMD -c "
import sys
sys.argv = ['app_psg.py', '--help']
try:
    exec(open('app_psg.py').read())
    print('Application dry run successful')
except SystemExit as e:
    if e.code in [0, None]:
        print('Application dry run successful')
    else:
        raise
except Exception as e:
    print(f'Application test failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
            print_success "Application startup test passed"
        else
            print_warning "Application startup test failed (may be normal for GUI apps)"
        fi
    fi
}

# Main installation function
main() {
    echo "🐍 Excel Template Mapper - Installation Script"
    echo "=============================================="
    
    case $1 in
        "venv")
            create_venv
            print_status "Please activate the virtual environment and run:"
            print_status "source venv/bin/activate && ./install.sh requirements"
            ;;
        "requirements")
            detect_environment
            install_requirements
            test_installation
            ;;
        "dev")
            detect_environment
            install_requirements
            install_dev_requirements
            test_installation
            ;;
        "test")
            detect_environment
            test_installation
            ;;
        *)
            echo "Usage: $0 [venv|requirements|dev|test]"
            echo ""
            echo "Commands:"
            echo "  venv         - Create virtual environment"
            echo "  requirements - Install requirements in current environment"
            echo "  dev          - Install development dependencies"
            echo "  test         - Test current installation"
            echo ""
            echo "Recommended workflow:"
            echo "  1. ./install.sh venv"
            echo "  2. source venv/bin/activate"
            echo "  3. ./install.sh dev"
            ;;
    esac
}

main "$@"