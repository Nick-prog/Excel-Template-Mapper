# Source Code Structure

This folder contains the organized source code for the Excel Template Mapper application.

## Structure

```
src/
├── __init__.py              # Package initialization
├── core/                    # Core business logic and models
│   ├── __init__.py
│   ├── models.py           # Data models and type definitions
│   ├── engine.py           # Core processing engine
│   └── utils.py            # Utility functions and helpers
├── widgets/                 # GUI widget components
│   ├── __init__.py
│   ├── main_window.py      # Main application window
│   ├── mapping_table.py    # Data mapping table widget
│   ├── preview_dialog.py   # Preview dialog window
│   └── transform_button.py # Transform selection widget
└── layouts/                 # UI layout definitions
    ├── __init__.py
    ├── advanced_format_builder.py  # Advanced formatting dialog
    ├── bottom_row.py               # Bottom action row layout
    ├── details_toggle.py           # Details toggle layout
    ├── details_widget.py           # Column details widget layout
    ├── sheet_row.py                # Sheet selection row layout
    ├── source_label_row.py         # Source file label layout
    └── top_file_row.py             # Top file selection layout
```

## Module Organization

### `core/` - Business Logic
- **models.py**: Contains all data classes and type definitions
  - `MappingSpec`, `SheetMapping`, `ColumnMapping`
  - Transform and type choice constants
- **engine.py**: Core processing functionality
  - Template building and validation
  - Data transformation and preview generation
  - Excel file processing
- **utils.py**: Helper functions
  - File I/O utilities
  - Data validation and formatting
  - Header mapping suggestions

### `widgets/` - GUI Components
Self-contained PySide6 widget classes for the user interface.

### `layouts/` - UI Layout Functions
Functions that create and configure specific UI layout sections.

## Import Guidelines

### Recommended Import Patterns

**From outside the src package (e.g., app_psg.py):**
```python
# Option 1: Direct module imports (most explicit)
from src.core.models import MappingSpec
from src.widgets.main_window import MainWindow

# Option 2: Package-level imports (cleaner)
from src.core import MappingSpec, generate_preview_data
from src.widgets import MainWindow, PreviewDialog

# Option 3: Top-level imports (most convenient)
from src import MappingSpec, MainWindow, generate_preview_data
```

**Within the src package:**
```python
# Within core package, use relative imports
from .models import MappingSpec
from .utils import safe_str

# Across packages within src, use absolute imports
from src.core.models import MappingSpec
from src.widgets.main_window import MainWindow
```

### Package Exports

Each `__init__.py` file exposes the most commonly used classes and functions:

- **`src/__init__.py`**: All main classes and functions
- **`src/core/__init__.py`**: Core models, engine functions, and utilities  
- **`src/widgets/__init__.py`**: All GUI widget classes
- **`src/layouts/__init__.py`**: All layout creation functions and dialog classes

- Use absolute imports from the root package: `from src.core.models import MappingSpec`
- Within the core package, use relative imports: `from .models import MappingSpec`
- Each folder is a proper Python package with `__init__.py` files