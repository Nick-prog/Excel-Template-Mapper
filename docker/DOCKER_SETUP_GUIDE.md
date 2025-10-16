# Docker Build Troubleshooting & Setup Guide

> **📁 Note:** As of the latest update, all Docker files have been moved to the `docker/` folder for better organization. All references in this guide should be updated to use `docker/Dockerfile`, `docker/Dockerfile.gui`, etc.

## Project Overview
Template Mapper is a PySide6 GUI application for mapping templates. This document details the complete process of setting up Docker support and the challenges encountered.

## Initial Problem
User requested help building Docker image and container, but encountered launch failures.

---

## Step-by-Step Troubleshooting Process

### 1. Initial Docker Task Execution
**Commands Attempted:**
```bash
# VS Code Task: docker-build: docker-build
# VS Code Task: docker-run: docker-run: debug
```

**Goal:** Use the pre-configured VS Code tasks to build and run the Docker container.

**Result:** Tasks reported success, but container failed to launch.

**Issue Identified:** Tasks showed "succeeded" but didn't provide detailed error output.

---

### 2. Docker Daemon Check
**Command:**
```bash
docker ps -a
```

**Goal:** Check the status of Docker containers to understand why the launch failed.

**Result:** 
```
Cannot connect to the Docker daemon at unix:///Users/nick/.docker/run/docker.sock. Is the docker daemon running?
```

**Issue Identified:** Docker Desktop was not running on the system.

---

### 3. Starting Docker Desktop
**Command:**
```bash
open -a Docker
```

**Goal:** Launch Docker Desktop application to start the Docker daemon.

**Result:** Docker Desktop started successfully.

**Wait Period:** Added 10-second delay for Docker to fully initialize.

---

### 4. Docker Version Verification
**Command:**
```bash
sleep 10 && docker --version
```

**Goal:** Confirm Docker is running and accessible.

**Result:** `Docker version 28.3.2, build 578ccf6`

**Status:** ✅ Docker daemon now running successfully.

---

### 5. Manual Docker Build Attempt
**Command:**
```bash
docker build -t templatemapper:latest .
```

**Goal:** Build the Docker image manually to see detailed error messages.

**Result:** Build failed with pip requirements error:
```
ERROR: Invalid requirement: 'Package            Version': Expected end or semicolon (after name and no valid version specifier)
```

**Issue Identified:** The `requirements.txt` file was in the wrong format (pip list output instead of pip freeze format).

---

### 6. Requirements.txt Format Analysis
**Original Content (BROKEN):**
```
Package            Version
------------------ -------
et_xmlfile         2.0.0
gitdb              4.0.12
GitPython          3.1.41
openpyxl           3.1.5
pip                25.2
PySide6            6.9.3
PySide6_Addons     6.9.3
PySide6_Essentials 6.9.3
setuptools         75.6.0
shiboken6          6.9.3
smmap              5.0.2
```

**Problem:** This is `pip list` output format, not valid for `pip install -r`.

**Solution:** Convert to proper pip requirements format.

---

### 7. Requirements.txt Fix #1
**Command:** Fixed requirements.txt to proper format:
```
et_xmlfile==2.0.0
gitdb==4.0.12
GitPython==3.1.41
openpyxl==3.1.5
PySide6==6.9.3
PySide6_Addons==6.9.3
PySide6_Essentials==6.9.3
shiboken6==6.9.3
smmap==5.0.2
```

**Goal:** Use proper pip requirements format for Docker build.

**Result:** Build failed with Python version compatibility error:
```
ERROR: Could not find a version that satisfies the requirement PySide6==6.9.3
```

**Issue Identified:** Python version mismatch between local environment and Docker image.

---

### 8. Python Version Analysis
**Local Python Check:**
```bash
python3 --version
# Result: Python 3.13.5
```

**Docker Image Python:** `python:3-slim` uses Python 3.12

**Problem:** PySide6 6.9.3 requires Python >=3.9,<3.14, but the specific version had compatibility issues with Python 3.12 in the Docker environment.

---

### 9. Docker Base Image Fix
**Changed Dockerfile:**
```dockerfile
# FROM python:3-slim          # Python 3.12 (problematic)
FROM python:3.11-slim          # Python 3.11 (compatible)
```

**Goal:** Use Python 3.11 which has better PySide6 compatibility.

**Rationale:** Python 3.11 is widely supported and has stable PySide6 package availability.

---

### 10. Requirements.txt Version Fix
**Updated to Python 3.11 compatible versions:**
```
et_xmlfile==2.0.0
gitdb==4.0.12
GitPython==3.1.41
openpyxl==3.1.5
PySide6==6.6.3
PySide6_Addons==6.6.3
PySide6_Essentials==6.6.3
shiboken6==6.6.3
smmap==5.0.2
```

**Goal:** Use PySide6 versions known to work with Python 3.11.

**Result:** ✅ Docker build succeeded!

---

### 11. Container Runtime Test
**Command:**
```bash
docker run --rm templatemapper:latest
```

**Goal:** Test if the application runs in the container.

**Result:** Runtime error:
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

**Issue Identified:** GUI applications require graphics libraries not available in slim Docker images.

---

### 12. GUI Application Challenges
**Problem:** PySide6 is a GUI framework that requires:
- Graphics libraries (OpenGL, X11)
- Display server connection
- Window manager integration

**Docker Limitation:** Standard Docker containers are headless and don't have display capabilities.

---

### 13. Solutions Provided

#### Solution A: Local Execution (Recommended)
**Created:** `run_local.sh` script
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 app_psg.py
```

**Advantages:**
- No display complications
- Full native GUI support
- Easier debugging
- Better performance

#### Solution B: Docker GUI Support
**Created:** `Dockerfile.gui` with graphics libraries:
```dockerfile
FROM python:3.11-slim

# Install system dependencies for GUI applications
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*
```

**Note:** Still requires X11 forwarding setup for macOS.

---

## Key Lessons Learned

### 1. Requirements.txt Format
- Always use `pip freeze > requirements.txt` not `pip list`
- Format must be `package==version` per line

### 2. Python Version Compatibility
- Docker base images may use different Python versions than local
- PySide6 has specific Python version requirements
- Check compatibility before selecting base images

### 3. GUI Applications in Docker
- GUI apps need graphics libraries and display access
- Standard Docker containers are headless
- Consider if containerization is necessary for GUI apps

### 4. Docker Desktop on macOS
- Must be running before any Docker commands
- Takes time to initialize after starting
- Check daemon status with `docker ps` before proceeding

---

## Final Working Setup

### Files Created/Modified:
1. `Dockerfile` - Fixed with Python 3.11 base
2. `requirements.txt` - Corrected format and versions
3. `Dockerfile.gui` - GUI-enabled version with graphics libraries
4. `run_local.sh` - Local execution script
5. This documentation file

### Recommended Usage:
- **Development:** Use `./run_local.sh` 
- **Production:** Consider if GUI app needs containerization
- **Docker Testing:** Use `Dockerfile.gui` with X11 forwarding if needed

### Docker Image Status:
- ✅ Image builds successfully: `templatemapper:latest`
- ✅ All Python dependencies install correctly
- ⚠️ GUI requires additional display configuration for container execution