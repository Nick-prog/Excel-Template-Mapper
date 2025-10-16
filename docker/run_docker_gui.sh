#!/bin/bash

# Template Mapper - Docker GUI Run Script
# This script runs the Template Mapper GUI application using Docker with X11 forwarding

echo "🐳 Starting Template Mapper Application in Docker..."
echo "📁 Working directory: $(pwd)"

# Change to the project directory
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "🔧 Setting up X11 forwarding for GUI..."

# Install XQuartz if not already installed (required for X11 forwarding on macOS)
if ! command -v xquartz &> /dev/null && ! ls /Applications/Utilities/XQuartz.app &> /dev/null; then
    echo "❌ Error: XQuartz is required for GUI applications in Docker on macOS."
    echo "   Please install XQuartz from: https://www.xquartz.org/"
    echo "   Or run: brew install --cask xquartz"
    exit 1
fi

# Start XQuartz if not running
if ! pgrep -x "XQuartz" > /dev/null; then
    echo "🚀 Starting XQuartz..."
    open -a XQuartz
    sleep 3
fi

# Allow X11 forwarding from localhost
xhost +localhost &> /dev/null

# Get the IP address for Docker
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

echo "🐍 Building Docker image with GUI support..."
docker build -f Dockerfile.gui -t templatemapper:gui ..

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker build failed"
    exit 1
fi

echo "🎯 Launching Template Mapper GUI in Docker..."
docker run --rm -it \
    -e DISPLAY=$IP:0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    templatemapper:gui

echo "👋 Template Mapper Docker container stopped"