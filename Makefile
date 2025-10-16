# Makefile for Excel Template Mapper
# Provides convenient commands for development and maintenance

.PHONY: help install install-venv install-dev test clean build validate update-deps run docker-setup docker-test docker-build docker-build-venv docker-run docker-run-venv

# Default target
help:
	@echo "Excel Template Mapper - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install-venv - Create virtual environment"
	@echo "  install      - Install the package and dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the application"
	@echo "  test         - Run comprehensive test suite"
	@echo "  test-imports - Test imports and functionality only"
	@echo "  test-types   - Test type hints and annotations"
	@echo "  test-packaging - Test package build process"
	@echo "  test-docker  - Test Docker configuration"
	@echo "  pre-commit   - Quick validation before committing"
	@echo "  clean        - Clean build artifacts"
	@echo ""
	@echo "Maintenance:"
	@echo "  validate     - Validate project structure and consistency"
	@echo "  update-deps  - Update requirements.txt from current environment"
	@echo "  format       - Format code with black"
	@echo "  lint         - Run linting checks"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  build            - Build distribution packages"
	@echo "  docker-setup     - Set up Docker GUI support for your OS (non-invasive)"
	@echo "  docker-test      - Test Docker GUI configuration"
	@echo "  docker-build     - Build Docker images (installs packages in container)"
	@echo "  docker-build-venv - Build Docker images using your virtual environment"
	@echo "  docker-run       - Run application in Docker (auto-detects OS)"
	@echo "  docker-run-venv  - Run application using your venv (no root installs)"
	@echo "  docker-setup-windows - Set up Windows X11 server"

# Python executable (use venv if available)
PYTHON := $(shell if [ -f "./venv/bin/python" ]; then echo "./venv/bin/python"; else echo "python3"; fi)
PIP := $(shell if [ -f "./venv/bin/pip" ]; then echo "./venv/bin/pip"; else echo "pip3"; fi)

# Installation
install:
	@echo "🐍 Installing Excel Template Mapper..."
	./install.sh requirements

install-dev:
	@echo "🔧 Installing Excel Template Mapper with development dependencies..."
	./install.sh dev

install-venv:
	@echo "🌐 Creating virtual environment..."
	./install.sh venv
	@echo "✅ Virtual environment created!"
	@echo "To activate: source venv/bin/activate"
	@echo "Then run: make install-dev"

# Running
run:
	$(PYTHON) app_psg.py

# Testing and validation
test:
	$(PYTHON) test/run_all_tests.py

test-imports:
	$(PYTHON) test/test_imports.py

test-types:
	$(PYTHON) test/test_type_hints.py

test-packaging:
	$(PYTHON) test/test_packaging.py

test-docker:
	$(PYTHON) test/test_docker.py

pre-commit:
	$(PYTHON) test/pre_commit.py

validate:
	$(PYTHON) test/validate_project.py

# Maintenance
update-deps:
	$(PYTHON) test/update_requirements.py

format:
	$(PYTHON) -m black src/ app_psg.py test/

lint:
	$(PYTHON) -m flake8 src/ app_psg.py
	$(PYTHON) -m mypy src/

# Build
clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

# Docker setup and testing
docker-setup:
	@echo "🐳 Setting up Docker GUI support..."
	@./docker/setup_gui.sh install

docker-test:
	@echo "🧪 Testing Docker GUI setup..."
	@./docker/setup_gui.sh test

# Docker
docker-build:
	docker build -f docker/Dockerfile -t excel-template-mapper:latest .
	docker build -f docker/Dockerfile.gui -t excel-template-mapper:gui .

# Build using existing virtual environment (no root package installation)
docker-build-venv:
	@echo "🔧 Building Docker image using your existing virtual environment..."
	@if [ ! -d "./venv" ]; then \
		echo "❌ Virtual environment not found. Please create one first:"; \
		echo "   python3 -m venv venv"; \
		echo "   source venv/bin/activate"; \
		echo "   pip install -r requirements.txt"; \
		exit 1; \
	fi
	docker build -f docker/Dockerfile.gui.venv -t excel-template-mapper:gui-venv .
	@echo "✅ Docker image built using your venv packages!"

docker-run:
	$(MAKE) docker-run-$(shell uname -s | tr '[:upper:]' '[:lower:]')

# Run using virtual environment image (no root packages)
docker-run-venv:
	@echo "🚀 Running Docker with your virtual environment..."
	@if ! docker images | grep -q "excel-template-mapper:gui-venv"; then \
		echo "❌ venv image not found. Building it first..."; \
		$(MAKE) docker-build-venv; \
	fi
	$(MAKE) docker-run-venv-$(shell uname -s | tr '[:upper:]' '[:lower:]')

docker-run-darwin:
	@echo "🍎 Running on macOS - Setting up XQuartz..."
	@if ! ls /Applications/Utilities/XQuartz.app >/dev/null 2>&1 && ! ls /Applications/XQuartz.app >/dev/null 2>&1 && ! ls /opt/X11 >/dev/null 2>&1; then \
		echo "❌ XQuartz not found. Installing via Homebrew..."; \
		if command -v brew >/dev/null 2>&1; then \
			brew install --cask xquartz; \
			echo "⚠️  Please log out and back in for XQuartz to work properly"; \
		else \
			echo "❌ Homebrew not found. Please install XQuartz manually from https://www.xquartz.org/"; \
			exit 1; \
		fi; \
	fi
	@echo "🚀 Starting XQuartz..."
	@open -a XQuartz 2>/dev/null || open -a /opt/X11/bin/X11.app 2>/dev/null || true
	@sleep 3
	@xhost +localhost >/dev/null 2>&1 || /opt/X11/bin/xhost +localhost >/dev/null 2>&1 || true
	@export DISPLAY=$$(ifconfig en0 | grep inet | awk '$$1=="inet" {print $$2}'):0; \
	docker run --rm -it \
		-e DISPLAY=$$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
		excel-template-mapper:gui

docker-run-venv-darwin:
	@echo "🍎 Running on macOS with venv - Setting up XQuartz..."
	@if ! ls /Applications/Utilities/XQuartz.app >/dev/null 2>&1 && ! ls /Applications/XQuartz.app >/dev/null 2>&1 && ! ls /opt/X11 >/dev/null 2>&1; then \
		echo "❌ XQuartz not found. Please install it manually from https://www.xquartz.org/"; \
		echo "   Or run: brew install --cask xquartz"; \
		exit 1; \
	fi
	@echo "🚀 Starting XQuartz..."
	@open -a XQuartz 2>/dev/null || open -a /opt/X11/bin/X11.app 2>/dev/null || true
	@sleep 3
	@xhost +localhost >/dev/null 2>&1 || /opt/X11/bin/xhost +localhost >/dev/null 2>&1 || true
	@export DISPLAY=$$(ifconfig en0 | grep inet | awk '$$1=="inet" {print $$2}'):0; \
	docker run --rm -it \
		-e DISPLAY=$$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
		excel-template-mapper:gui-venv

docker-run-linux:
	@echo "🐧 Running on Linux - Using native X11..."
	@xhost +local:docker >/dev/null 2>&1 || true
	docker run --rm -it \
		-e DISPLAY=$$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
		--network host \
		excel-template-mapper:gui

docker-run-venv-linux:
	@echo "🐧 Running on Linux with venv - Using native X11..."
	@xhost +local:docker >/dev/null 2>&1 || true
	docker run --rm -it \
		-e DISPLAY=$$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
		--network host \
		excel-template-mapper:gui-venv

docker-run-mingw64_nt-10.0:
docker-run-msys_nt-10.0:
docker-run-cygwin_nt-10.0:
	@$(MAKE) docker-run-windows

docker-run-windows:
	@echo "🪟 Running on Windows - Using VcXsrv/X410..."
	@echo "📋 Please ensure you have an X11 server running:"
	@echo "   - VcXsrv: https://sourceforge.net/projects/vcxsrv/"
	@echo "   - X410: https://x410.dev/"
	@echo "   - Or WSL2 with GUI support"
	@echo ""
	@if command -v powershell.exe >/dev/null 2>&1; then \
		export HOST_IP=$$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'vEthernet (WSL)').IPAddress" 2>/dev/null | tr -d '\r' | head -1); \
		if [ -z "$$HOST_IP" ]; then \
			export HOST_IP=$$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$$_.PrefixOrigin -eq 'Dhcp'}).IPAddress" 2>/dev/null | tr -d '\r' | head -1); \
		fi; \
		if [ -z "$$HOST_IP" ]; then \
			export HOST_IP="host.docker.internal"; \
		fi; \
	else \
		export HOST_IP="host.docker.internal"; \
	fi; \
	echo "🔗 Using display: $$HOST_IP:0"; \
	docker run --rm -it \
		-e DISPLAY=$$HOST_IP:0 \
		--add-host=host.docker.internal:host-gateway \
		excel-template-mapper:gui

docker-run-venv-windows:
docker-run-venv-mingw64_nt-10.0:
docker-run-venv-msys_nt-10.0:
docker-run-venv-cygwin_nt-10.0:
	@echo "🪟 Running on Windows with venv - Using VcXsrv/X410..."
	@echo "📋 Please ensure you have an X11 server running:"
	@echo "   - VcXsrv: https://sourceforge.net/projects/vcxsrv/"
	@echo "   - X410: https://x410.dev/"
	@echo "   - Or WSL2 with GUI support"
	@echo ""
	@if command -v powershell.exe >/dev/null 2>&1; then \
		export HOST_IP=$$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'vEthernet (WSL)').IPAddress" 2>/dev/null | tr -d '\r' | head -1); \
		if [ -z "$$HOST_IP" ]; then \
			export HOST_IP=$$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$$_.PrefixOrigin -eq 'Dhcp'}).IPAddress" 2>/dev/null | tr -d '\r' | head -1); \
		fi; \
		if [ -z "$$HOST_IP" ]; then \
			export HOST_IP="host.docker.internal"; \
		fi; \
	else \
		export HOST_IP="host.docker.internal"; \
	fi; \
	echo "🔗 Using display: $$HOST_IP:0"; \
	docker run --rm -it \
		-e DISPLAY=$$HOST_IP:0 \
		--add-host=host.docker.internal:host-gateway \
		excel-template-mapper:gui-venv

docker-setup-windows:
	@echo "🪟 Setting up Windows X11 server..."
	@echo "1️⃣ Installing VcXsrv via Chocolatey (if available)..."
	@if command -v choco >/dev/null 2>&1; then \
		choco install vcxsrv -y; \
	else \
		echo "   Chocolatey not found. Please install manually:"; \
		echo "   https://sourceforge.net/projects/vcxsrv/"; \
	fi
	@echo "2️⃣ To start VcXsrv, run: 'vcxsrv.exe' with these settings:"
	@echo "   - Multiple windows: ✓"
	@echo "   - Start no client: ✓" 
	@echo "   - Clipboard: ✓"
	@echo "   - Disable access control: ✓"