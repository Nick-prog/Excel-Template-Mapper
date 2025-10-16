#!/bin/bash

# Cross-Platform Docker GUI Setup Script
# Automatically installs and configures GUI support for Docker containers

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

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin*)
            OS="macOS"
            ;;
        Linux*)
            OS="Linux"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            OS="Windows"
            ;;
        *)
            OS="Unknown"
            ;;
    esac
    print_status "Detected OS: $OS"
}

# Setup for macOS
setup_macos() {
    print_status "Setting up GUI support for macOS..."
    
    # Check if Homebrew is installed (don't auto-install)
    if ! command -v brew &> /dev/null; then
        print_warning "Homebrew not found."
        print_status "To install Homebrew (optional):"
        print_status "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        print_status ""
        print_status "Or install XQuartz manually from: https://www.xquartz.org/"
        return 1
    fi
    
    # Check for XQuartz in multiple locations
    if [ -d "/Applications/Utilities/XQuartz.app" ] || [ -d "/Applications/XQuartz.app" ] || [ -d "/opt/X11" ] || command -v xquartz &> /dev/null; then
        print_success "XQuartz is already installed"
    else
        print_status "XQuartz not found. Would you like to install it? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            print_status "Installing XQuartz..."
            brew install --cask xquartz
            print_success "XQuartz installed successfully"
            print_warning "Please log out and back in for XQuartz to work properly"
        else
            print_warning "XQuartz not installed. You can install it manually from: https://www.xquartz.org/"
        fi
    fi
    
    # Check Docker Desktop (don't auto-install)
    if ! command -v docker &> /dev/null; then
        print_warning "Docker Desktop not found."
        print_status "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        return 1
    else
        print_success "Docker is already installed"
    fi
    
    print_success "macOS setup complete!"
    print_status "To run GUI applications:"
    print_status "1. Start XQuartz: open -a XQuartz"
    print_status "2. Run: make docker-run-venv"
}

# Setup for Linux
setup_linux() {
    print_status "Setting up GUI support for Linux..."
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        PKG_MANAGER="apt-get"
        INSTALL_CMD="sudo apt-get install -y"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        INSTALL_CMD="sudo yum install -y"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        INSTALL_CMD="sudo dnf install -y"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
        INSTALL_CMD="sudo pacman -S --noconfirm"
    else
        print_error "Unsupported package manager. Please install Docker manually."
        return 1
    fi
    
    print_status "Using package manager: $PKG_MANAGER"
    
    # Check X11 utilities (don't auto-install)
    if ! command -v xhost &> /dev/null; then
        print_warning "X11 utilities not found."
        print_status "To install X11 utilities:"
        case $PKG_MANAGER in
            "apt-get")
                print_status "sudo apt-get install -y x11-xserver-utils"
                ;;
            "yum"|"dnf")
                print_status "sudo $PKG_MANAGER install -y xorg-x11-server-utils"
                ;;
            "pacman")
                print_status "sudo pacman -S xorg-xhost"
                ;;
        esac
        return 1
    else
        print_success "X11 utilities are already installed"
    fi
    
    # Check Docker (don't auto-install)
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found."
        print_status "Please install Docker from: https://docs.docker.com/engine/install/"
        return 1
    else
        print_success "Docker is already installed"
        
        # Check if user is in docker group
        if ! groups $USER | grep -q docker; then
            print_warning "User $USER is not in docker group."
            print_status "To add yourself to docker group:"
            print_status "sudo usermod -aG docker $USER"
            print_status "Then log out and back in."
        fi
    fi
    
    print_success "Linux setup check complete!"
    print_status "To run GUI applications: make docker-run"
}

# Setup for Windows
setup_windows() {
    print_status "Setting up GUI support for Windows..."
    
    # Check if we're in WSL
    if grep -qi wsl /proc/version 2>/dev/null; then
        print_status "Running in WSL - setting up WSL2 GUI support..."
        setup_wsl
    else
        print_status "Running in native Windows..."
        setup_native_windows
    fi
}

setup_wsl() {
    print_status "Setting up WSL2 with GUI support..."
    
    # Check X11 utilities (don't auto-install)
    if command -v apt-get &> /dev/null; then
        if ! dpkg -l | grep -q x11-apps; then
            print_warning "X11 apps not found."
            print_status "To install: sudo apt-get install -y x11-apps"
            return 1
        fi
    fi
    
    print_success "WSL2 setup check complete!"
    print_status "For GUI support in WSL2, you can:"
    print_status "1. Use WSLg (Windows 11 22H2+) - no additional setup needed"
    print_status "2. Install VcXsrv on Windows host and run: make docker-setup-windows"
}

setup_native_windows() {
    print_status "Setting up native Windows Docker GUI support..."
    
    # Check if Chocolatey is available (don't auto-install)
    if command -v choco &> /dev/null; then
        print_status "Chocolatey found. To install VcXsrv:"
        print_status "choco install vcxsrv -y"
    else
        print_status "Chocolatey not found."
        print_status "Please install VcXsrv manually:"
        print_status "1. Download from: https://sourceforge.net/projects/vcxsrv/"
        print_status "2. Install and run with these settings:"
        print_status "   - Multiple windows: ✓"
        print_status "   - Start no client: ✓"
        print_status "   - Clipboard: ✓"  
        print_status "   - Disable access control: ✓"
    fi
    
    # Check if Docker Desktop is installed
    if ! command -v docker &> /dev/null; then
        print_warning "Docker Desktop not found."
        print_status "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        return 1
    else
        print_success "Docker Desktop is installed"
    fi
    
    print_success "Windows setup check complete!"
}

# Test Docker GUI setup
test_setup() {
    print_status "Testing Docker GUI setup..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        return 1
    fi
    
    print_success "Docker is running correctly"
    
    # Test GUI support based on OS
    case $OS in
        "macOS")
            # Check for XQuartz in multiple locations
            if [ -d "/Applications/Utilities/XQuartz.app" ] || [ -d "/Applications/XQuartz.app" ] || [ -d "/opt/X11" ] || command -v xquartz &> /dev/null; then
                print_success "XQuartz is available"
            else
                print_warning "XQuartz not found - GUI applications may not work"
                print_status "Try installing with: brew install --cask xquartz"
                return 1
            fi
            ;;
        "Linux")
            if ! command -v xhost &> /dev/null; then
                print_warning "xhost command not found - GUI applications may not work"
                return 1
            fi
            print_success "X11 utilities are available"
            ;;
        "Windows")
            print_status "Windows GUI support requires manual VcXsrv/X410 setup"
            ;;
    esac
    
    print_success "Docker GUI setup test completed!"
}

# Main execution
main() {
    echo "🐳 Excel Template Mapper - Cross-Platform Docker GUI Setup"
    echo "========================================================="
    
    detect_os
    
    case $1 in
        "test")
            test_setup
            ;;
        "install")
            case $OS in
                "macOS")
                    setup_macos
                    ;;
                "Linux")
                    setup_linux
                    ;;
                "Windows")
                    setup_windows
                    ;;
                *)
                    print_error "Unsupported operating system: $OS"
                    exit 1
                    ;;
            esac
            ;;
        *)
            echo "Usage: $0 [install|test]"
            echo ""
            echo "Commands:"
            echo "  install  - Install required dependencies for Docker GUI support"
            echo "  test     - Test current Docker GUI setup"
            echo ""
            echo "After installation, you can run:"
            echo "  make docker-run    - Run the application in Docker with GUI support"
            ;;
    esac
}

main "$@"