# Docker Configuration

This folder contains all Docker-related files for the Excel Template Mapper project.

## Files

- **Dockerfile** - Main Docker image for the application
- **Dockerfile.gui** - Docker image with GUI support for X11 forwarding
- **compose.yaml** - Production Docker Compose configuration
- **compose.debug.yaml** - Debug Docker Compose configuration with debugpy support
- **run_docker_gui.sh** - Script to run the GUI application with Docker and X11 forwarding
- **DOCKER_SETUP_GUIDE.md** - Comprehensive troubleshooting and setup guide

## Usage

### Building the main image
```bash
# From project root
docker build -f docker/Dockerfile -t templatemapper:latest .

# From docker folder
docker build -f Dockerfile -t templatemapper:latest ..
```

### Building the GUI image
```bash
# From project root
docker build -f docker/Dockerfile.gui -t templatemapper:gui .

# From docker folder  
docker build -f Dockerfile.gui -t templatemapper:gui ..
```

### Using Docker Compose
```bash
# From docker folder
docker-compose -f compose.yaml up

# Debug mode
docker-compose -f compose.debug.yaml up
```

### GUI Application (macOS)
```bash
# From docker folder
./run_docker_gui.sh
```

## Notes

- Uses Python 3.13 to match local development environment
- The build context is set to the parent directory (`..`) to access all project files
- GUI support requires X11 forwarding on macOS (XQuartz)
- Debug configuration includes debugpy for VS Code debugging support
- PySide6 6.10.0+ is required for Python 3.13 compatibility