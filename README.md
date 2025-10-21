
# Excel-Template-Mapper

> **Note**: This project was developed utilizing GitHub Copilot AI assistance for code generation, optimization, and documentation.

A powerful GUI application for mapping and transforming templates with Excel integration.

## 🚀 Quick Installation

### Option 1: Download Pre-built Executable (Recommended)

**Stable Release:** [Download from GitHub Releases](https://github.com/Nick-prog/Excel-Template-Mapper/releases/latest)

**Latest Development Build:** [Download Latest Build](https://github.com/Nick-prog/Excel-Template-Mapper/releases/tag/latest) (Updated automatically with each commit)

### Option 1.5: Install via Python Package (pip)

**From Latest Release:**
```bash
# Download the .whl file from releases, then:
pip install excel-template-mapper-*.whl

# Or install from source distribution:
pip install excel-template-mapper-*.tar.gz
```

**Note:** Python packages are available alongside executables in both stable and development releases.

#### Quick Install Script:
```bash
# Unix/Linux/macOS
curl -fsSL https://raw.githubusercontent.com/Nick-prog/Excel-Template-Mapper/main/install.sh | bash

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Nick-prog/Excel-Template-Mapper/main/install.bat" -OutFile "install.bat" && .\install.bat
```

#### Manual Download:
1. Go to [Releases](https://github.com/Nick-prog/Excel-Template-Mapper/releases/latest)
2. Download the appropriate file for your system:
   
   **Standalone Executables (No Python required):**
   - **Windows**: `excel-template-mapper-windows-amd64.exe`
   - **macOS (Intel)**: `excel-template-mapper-macos-amd64`
   - **macOS (Apple Silicon)**: `excel-template-mapper-macos-arm64`
   - **Linux**: `excel-template-mapper-linux-amd64`
   
   **Python Packages (For pip install):**
   - **Wheel Package**: `excel-template-mapper-*.whl` (Recommended)
   - **Source Distribution**: `excel-template-mapper-*.tar.gz`

3. **For executables**: Run the downloaded file directly
   **For Python packages**: `pip install downloaded-file.whl`

> **⚠️ Security Note**: Browsers may warn about downloading executables. These are false positives for unsigned files. See [DOWNLOAD_SECURITY.md](DOWNLOAD_SECURITY.md) for details about why this happens and how to safely download.

### Option 2: Build from Source

#### Prerequisites
- Python 3.8 or higher
- Git

#### Step 1: Environment Setup
```bash
# Clone the repository
git clone https://github.com/Nick-prog/Excel-Template-Mapper/.git
cd YOUR_REPO

# Create and activate virtual environment (IMPORTANT!)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows

# Verify virtual environment is active (you should see (venv) in prompt)
which pip  # Should point to ./venv/bin/pip
```

#### Step 2: Install Dependencies
```bash
# Install all dependencies in the virtual environment
pip install -r requirements.txt pyinstaller
```

#### Step 3: Build Executable
```bash
# Build executable (completely non-invasive)
python setup.py

# The executable will be created in dist/ directory
# - Windows: dist/Template-Mapper.exe
# - macOS/Linux: dist/Template-Mapper
```

#### Step 4: Run the Application
```bash
# Run the executable
./dist/Template-Mapper  # macOS/Linux
# dist\Template-Mapper.exe  # Windows

# Or run from source during development
python app_psg.py
```

## ⚠️ Important Notes

- **Virtual Environment**: The project requires a properly activated virtual environment for development
- **Non-Invasive Setup**: `setup.py` only checks dependencies and builds executables - it never installs packages
- **Manual Dependency Management**: You control your Python environment - install dependencies manually
- **Environment Issues**: If you get "pip installing globally" errors, recreate your virtual environment

## 📋 System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 or later
- **Linux**: Most modern distributions (Ubuntu 18.04+, CentOS 7+, etc.)
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 100MB available space

## 🎯 Features

- **Cross-platform GUI application** - Works on Windows, macOS, and Linux
- **Excel template mapping and transformation** - Map source data to target templates
- **Interactive column mapping** - Drag-and-drop or click-to-map interface
- **Live preview functionality** - See results before final transformation
- **Advanced formatting builder** - Custom data transformation rules
- **Multi-sheet support** - Handle complex Excel workbooks
- **Multiple export options** - Save to various formats
- **Non-invasive installation** - Respects your Python environment
- **Standalone executables** - No Python installation required for end users
- **Comprehensive type hints** - Fully typed codebase for better maintainability
- **Docker support** - Containerized deployment with GUI forwarding
- **Modular architecture** - Clean separation of widgets, layouts, and core logic

## 📖 Usage

### Running the Application

After installation, simply run:
- **Windows**: Double-click `Template-Mapper.exe` or run from command line
- **macOS/Linux**: `./Template-Mapper` or double-click the executable

### Development Usage

If you're running from source:
```bash
# Run locally (recommended for development)
./run_local.sh

# Or run with Python directly
python app_psg.py
```

## 🐳 Docker Support

For containerized deployment, all Docker files are organized in the `docker/` folder:

```bash
# Build and run locally
./run_local.sh

# Build and run with Docker GUI support
cd docker && ./run_docker_gui.sh

# Or use Docker Compose from the docker folder
cd docker && docker-compose -f compose.yaml up
```

See `docker/README.md` for detailed Docker configuration and usage instructions.

## 🛠️ Development

### Setup Development Environment

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt pyinstaller

# Run development version
python app_psg.py
```

#### Option B: Using setup.py dev command
```bash
python setup.py dev
```

This will:
- Create a virtual environment
- Set up the development environment structure
- Provide guidance on dependency installation

### Running in Development Mode
```bash
# Run locally (recommended for development)
./run_local.sh

# Or run with Python directly
python app_psg.py
```

### Project Structure
```
Excel-Template-Mapper/
├── app_psg.py              # Main application entry point
├── setup.py                # Non-invasive executable builder
├── requirements.txt        # Python dependencies
├── src/                    # Organized source code
│   ├── core/              # Core business logic
│   │   ├── models.py      # Data models
│   │   ├── engine.py      # Processing engine
│   │   └── utils.py       # Utility functions
│   ├── widgets/           # GUI widgets
│   │   ├── main_window.py
│   │   ├── mapping_table.py
│   │   ├── preview_dialog.py
│   │   └── transform_button.py
│   └── layouts/           # GUI layouts
├── docker/                # Docker configuration
├── test/                  # Test files and validation
├── venv/                  # Virtual environment (after setup)
├── dist/                  # Generated executables
└── .github/workflows/     # CI/CD workflows
```

See `src/README.md` for detailed source code organization.

### Building Executables

To build executables for all platforms:

```bash
# Build for current platform
python setup.py executable

# The executable will be created in the dist/ directory
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python -m pytest` (if tests exist)
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Support

- **Issues**: [GitHub Issues](https://github.com/Nick-prog/Excel-Template-Mapper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nick-prog/Excel-Template-Mapper/discussions)

## 🔧 Troubleshooting

### "pip installing globally even though I'm in a venv"
This happens when your virtual environment was created in a directory with a different name than your current directory.

**Solution**:
```bash
# Remove broken venv
rm -rf venv

# Create new venv in current directory
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows

# Verify it's working
which pip  # Should point to ./venv/bin/pip
echo $VIRTUAL_ENV  # Should show your current directory/venv

# Install dependencies
pip install -r requirements.txt pyinstaller
```

### "setup.py tries to install packages"
The setup.py is designed to be completely non-invasive. If you see installation attempts:
- Use `python setup.py executable` (not `install`)
- Install dependencies manually: `pip install -r requirements.txt`
- The setup.py will only check for dependencies and build executables

### "Virtual environment not activating"
Check your terminal prompt for `(venv)` prefix. If missing:
```bash
# Ensure you're in the right directory
pwd

# Reactivate
source venv/bin/activate
```

## 🔄 Release Notes

### Latest Release
See [Releases](https://github.com/Nick-prog/Excel-Template-Mapper/releases) for detailed changelog.

---

## ⚡ Quick Start

1. **Download** the latest release for your platform
2. **Run** the executable
3. **Start** mapping your templates!

For detailed documentation, see the [Wiki](https://github.com/Nick-prog/Excel-Template-Mapper/wiki).