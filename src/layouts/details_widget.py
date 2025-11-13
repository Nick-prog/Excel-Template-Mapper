from PySide6 import QtWidgets, QtCore
from ..core.models import TYPE_CHOICES
from ..widgets.transform_button import TransformButton

def create_details_widget(parent, on_apply_details):
    """Create an enhanced details widget with tabs for different operation types."""
    details_widget = QtWidgets.QGroupBox("Selected Column Details", parent)
    details_widget.setVisible(False)
    main_layout = QtWidgets.QVBoxLayout(details_widget)
    
    # Basic info section
    basic_group = QtWidgets.QGroupBox("Basic Information")
    basic_layout = QtWidgets.QFormLayout(basic_group)
    
    detail_target = QtWidgets.QLabel("-", parent)
    basic_layout.addRow("Target Column:", detail_target)
    
    detail_source = QtWidgets.QLabel("-", parent)
    basic_layout.addRow("Source Column:", detail_source)
    
    detail_default = QtWidgets.QLineEdit(parent)
    detail_default.setPlaceholderText("Value if source is empty")
    basic_layout.addRow("Default Value:", detail_default)
    
    main_layout.addWidget(basic_group)
    
    # Create tabs for different operation types
    tabs = QtWidgets.QTabWidget(parent)
    
    # Tab 1: Data Type & Formatting
    type_format_widget = _create_type_format_tab(parent)
    detail_type = type_format_widget['type']
    detail_format = type_format_widget['format']
    detail_format_preset = type_format_widget['preset']
    tabs.addTab(type_format_widget['widget'], "Type & Format")
    
    # Tab 2: Find & Replace
    find_replace_widget = _create_find_replace_tab(parent)
    detail_find_replace = find_replace_widget['table']
    tabs.addTab(find_replace_widget['widget'], "Find & Replace")
    
    # Tab 3: Transforms
    transforms_widget = _create_transforms_tab(parent)
    detail_tfbtn = transforms_widget['button']
    tabs.addTab(transforms_widget['widget'], "Transforms")
    
    # Tab 4: Advanced Formatting
    advanced_widget = _create_advanced_tab(parent)
    detail_advanced = advanced_widget['editor']
    tabs.addTab(advanced_widget['widget'], "Advanced")
    
    main_layout.addWidget(tabs)
    
    # Apply button
    detail_apply = QtWidgets.QPushButton("Apply to Selected Column", parent)
    detail_apply.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
    detail_apply.clicked.connect(on_apply_details)
    main_layout.addWidget(detail_apply)
    
    return (
        details_widget, detail_target, detail_type, detail_format, detail_tfbtn,
        detail_default, detail_advanced, detail_apply, detail_source, detail_format_preset, detail_find_replace
    )


def _create_type_format_tab(parent):
    """Create Data Type & Format tab."""
    widget = QtWidgets.QWidget(parent)
    main_layout = QtWidgets.QVBoxLayout(widget)
    
    layout = QtWidgets.QFormLayout()
    
    # Data Type selector
    type_label = QtWidgets.QLabel(
        "<b>Data Type</b><br/>"
        "<small>Determines how Excel interprets the data</small>"
    )
    type_label.setWordWrap(True)
    detail_type = QtWidgets.QComboBox(parent)
    for t in TYPE_CHOICES:
        detail_type.addItem(t.title(), t)
    layout.addRow(type_label, detail_type)
    
    # Format type selector
    format_type_label = QtWidgets.QLabel(
        "<b>Format Template</b><br/>"
        "<small>Choose a preset or enter custom Excel format code</small>"
    )
    format_type_label.setWordWrap(True)
    detail_format_preset = QtWidgets.QComboBox(parent)
    detail_format_preset.addItems([
        "None (Default)",
        "Number - 2 decimals",
        "Number - 4 decimals",
        "Percentage",
        "Currency ($)",
        "Currency (EUR €)",
        "Date (MM/DD/YYYY)",
        "Date (YYYY-MM-DD)",
        "DateTime (MM/DD/YYYY HH:MM)",
        "Time (HH:MM:SS)",
        "Phone (USA)",
        "SSN (USA)",
        "Custom...",
    ])
    
    def on_preset_changed(idx):
        """Update custom format field based on preset selection."""
        presets = {
            "None (Default)": "",
            "Number - 2 decimals": "0.00",
            "Number - 4 decimals": "0.0000",
            "Percentage": "0%",
            "Currency ($)": "$#,##0.00",
            "Currency (EUR €)": "[$EUR -407] #,##0.00;[RED]-[$EUR -407] #,##0.00",
            "Date (MM/DD/YYYY)": "mm/dd/yyyy",
            "Date (YYYY-MM-DD)": "yyyy-mm-dd",
            "DateTime (MM/DD/YYYY HH:MM)": "mm/dd/yyyy hh:mm",
            "Time (HH:MM:SS)": "hh:mm:ss",
            "Phone (USA)": "[<=9999999]###-####;(###) ###-####",
            "SSN (USA)": "000-00-0000",
            "Custom...": "",
        }
        selected = detail_format_preset.currentText()
        detail_format.setText(presets.get(selected, ""))
        detail_format.setReadOnly(selected != "Custom...")
    
    detail_format_preset.currentIndexChanged.connect(on_preset_changed)
    layout.addRow(format_type_label, detail_format_preset)
    
    # Custom format field
    custom_label = QtWidgets.QLabel(
        "<b>Custom Excel Format Code</b><br/>"
        "<small>Excel number format codes (e.g., #,##0.00 for currency)</small>"
    )
    custom_label.setWordWrap(True)
    detail_format = QtWidgets.QLineEdit(parent)
    detail_format.setPlaceholderText("Excel format code (e.g., #,##0.00)")
    layout.addRow(custom_label, detail_format)
    
    # Help text
    help_text = QtWidgets.QLabel(
        "<b>Excel Format Code Examples:</b><br/>"
        "• <code>0.00</code> - Two decimal places<br/>"
        "• <code>#,##0</code> - Thousands separator<br/>"
        "• <code>0%</code> - Percentage<br/>"
        "• <code>$#,##0.00</code> - Currency<br/>"
        "• <code>mm/dd/yyyy</code> - Date format<br/>"
        "• <code>[<=9999999]###-####;(###) ###-####</code> - Phone number"
    )
    help_text.setWordWrap(True)
    help_text.setStyleSheet("color: #666; font-size: 10px;")
    layout.addRow(help_text)
    
    main_layout.addLayout(layout)
    main_layout.addStretch()
    
    return {
        'widget': widget,
        'type': detail_type,
        'format': detail_format,
        'preset': detail_format_preset
    }


def _create_find_replace_tab(parent):
    """Create Find & Replace tab."""
    widget = QtWidgets.QWidget(parent)
    layout = QtWidgets.QVBoxLayout(widget)
    
    instructions = QtWidgets.QLabel(
        "<b>Find and Replace Rules</b><br/>"
        "<small>Define multiple find/replace patterns to be applied to this column</small>"
    )
    instructions.setWordWrap(True)
    layout.addWidget(instructions)
    
    # Table for find/replace pairs
    table = QtWidgets.QTableWidget(parent)
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Find", "Replace With", "Remove"])
    table.horizontalHeader().setStretchLastSection(False)
    table.setColumnWidth(0, 200)
    table.setColumnWidth(1, 200)
    table.setColumnWidth(2, 80)
    table.setMinimumHeight(150)
    layout.addWidget(table)
    
    # Buttons to manage rows
    button_layout = QtWidgets.QHBoxLayout()
    
    add_btn = QtWidgets.QPushButton("Add Rule")
    def add_row():
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
        remove_btn = QtWidgets.QPushButton("Delete")
        # Create closure to capture row number
        def delete_row(checked=False, row_num=row):
            table.removeRow(row_num)
        remove_btn.clicked.connect(delete_row)
        table.setCellWidget(row, 2, remove_btn)
    add_btn.clicked.connect(add_row)
    button_layout.addWidget(add_btn)
    
    help_label = QtWidgets.QLabel(
        "<small><b>Tip:</b> Use regex patterns for complex matching (e.g., ^\\d{3}$ for 3 digits)</small>"
    )
    help_label.setWordWrap(True)
    button_layout.addWidget(help_label)
    button_layout.addStretch()
    layout.addLayout(button_layout)
    
    layout.addStretch()
    
    return {
        'widget': widget,
        'table': table
    }


def _create_transforms_tab(parent):
    """Create Transforms tab."""
    widget = QtWidgets.QWidget(parent)
    layout = QtWidgets.QVBoxLayout(widget)
    
    instructions = QtWidgets.QLabel(
        "<b>Transform Operations</b><br/>"
        "<small>Apply built-in transformations to this column</small>"
    )
    instructions.setWordWrap(True)
    layout.addWidget(instructions)
    
    detail_tfbtn = TransformButton([], parent)
    layout.addWidget(detail_tfbtn)
    
    # Available transforms info
    available_transforms = QtWidgets.QLabel(
        "<b>Available Transforms:</b><br/>"
        "• <code>trim</code> - Remove leading/trailing whitespace<br/>"
        "• <code>upper</code> - Convert to UPPERCASE<br/>"
        "• <code>lower</code> - Convert to lowercase<br/>"
        "• <code>title</code> - Convert To Title Case<br/>"
        "• <code>to_string</code> - Convert to text format<br/>"
        "• <code>to_int</code> - Convert to integer<br/>"
        "• <code>to_float</code> - Convert to decimal number<br/>"
        "• <code>date_to_iso</code> - Convert to ISO date format (YYYY-MM-DD)<br/>"
        "• <code>digits_only</code> - Extract only numeric digits"
    )
    available_transforms.setWordWrap(True)
    available_transforms.setStyleSheet("color: #666; font-size: 10px;")
    layout.addWidget(available_transforms)
    
    layout.addStretch()
    
    return {
        'widget': widget,
        'button': detail_tfbtn
    }


def _create_advanced_tab(parent):
    """Create Advanced Formatting tab with improved structure."""
    widget = QtWidgets.QWidget(parent)
    layout = QtWidgets.QVBoxLayout(widget)
    
    instructions = QtWidgets.QLabel(
        "<b>Advanced Formatting</b><br/>"
        "<small>Write custom Python logic or Excel formulas for complex transformations</small>"
    )
    instructions.setWordWrap(True)
    layout.addWidget(instructions)
    
    # Format type selector
    format_type_layout = QtWidgets.QHBoxLayout()
    format_type_label = QtWidgets.QLabel("Format Type:")
    format_type = QtWidgets.QComboBox(parent)
    format_type.addItems(["Python Function", "Excel Formula", "Find & Replace Pattern"])
    format_type_layout.addWidget(format_type_label)
    format_type_layout.addWidget(format_type)
    layout.addLayout(format_type_layout)
    
    # Code editor
    from .advanced_format_builder import AdvancedCodeEdit
    detail_advanced = AdvancedCodeEdit(parent)
    detail_advanced.setPlaceholderText("Write your logic here...")
    detail_advanced.setMinimumHeight(200)
    layout.addWidget(detail_advanced)
    
    # Code templates
    template_layout = QtWidgets.QHBoxLayout()
    template_label = QtWidgets.QLabel("Code Templates:")
    template_combo = QtWidgets.QComboBox(parent)
    
    # Enhanced templates
    templates = {
        "Python: If/Else Logic": """def format_column(col, source):
    \"\"\"Apply conditional logic based on column values.\"\"\"
    if source['SourceColumn'] == 'SomeValue':
        return 'MappedValue'
    elif source['SourceColumn'] == 'AnotherValue':
        return 'DifferentValue'
    else:
        return col['TargetColumn']""",
        
        "Python: Text Operations": """def format_column(col, source):
    \"\"\"Manipulate text: concatenate, extract, or transform.\"\"\"
    value = source['SourceColumn'].strip()  # Remove whitespace
    # Convert to title case
    return value.title() if value else ''""",
        
        "Python: Number Operations": """def format_column(col, source):
    \"\"\"Perform calculations and number formatting.\"\"\"
    try:
        value = float(source['SourceColumn'])
        # Round to 2 decimal places
        return round(value, 2)
    except (ValueError, TypeError):
        return 0""",
        
        "Python: String Replacement": """import re
def format_column(col, source):
    \"\"\"Use regex for complex replacements.\"\"\"
    value = source['SourceColumn']
    # Replace all non-alphanumeric characters with underscore
    return re.sub(r'[^a-zA-Z0-9]', '_', value)""",
        
        "Python: Date Parsing": """from datetime import datetime
def format_column(col, source):
    \"\"\"Parse and reformat dates.\"\"\"
    try:
        date_obj = datetime.strptime(source['SourceColumn'], '%m/%d/%Y')
        return date_obj.strftime('%Y-%m-%d')  # ISO format
    except ValueError:
        return ''""",
        
        "Python: Conditional Mapping": """def format_column(col, source):
    \"\"\"Map values to categories.\"\"\"
    value = source['SourceColumn']
    mapping = {
        'V1': 'Category A',
        'V2': 'Category B',
        'V3': 'Category C',
    }
    return mapping.get(value, 'Unknown')""",
        
        "Python: Null/Empty Handling": """def format_column(col, source):
    \"\"\"Handle missing or empty values.\"\"\"
    value = source['SourceColumn']
    if not value or value.strip() == '':
        return col['TargetColumn']  # Use default or other column
    return value.strip()""",
        
        "Excel: Basic Formula": """=IF(ISNUMBER(A1), A1*2, "Invalid")""",
        
        "Excel: Concatenation": """=CONCATENATE(A1, " - ", B1)""",
        
        "Excel: VLOOKUP": """=IFERROR(VLOOKUP(A1, LookupTable, 2, FALSE), "Not Found")""",
        
        "Regex: Phone Number": """r'(\\d{3})-(\\d{3})-(\\d{4})' -> r'(\\1) \\2-\\3'""",
        
        "Regex: Email Extraction": """r'(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})'""",
    }
    
    template_combo.addItems(list(templates.keys()))
    
    def insert_template():
        selected = template_combo.currentText()
        detail_advanced.setPlainText(templates[selected])
    
    template_btn = QtWidgets.QPushButton("Insert Template")
    template_btn.clicked.connect(insert_template)
    template_layout.addWidget(template_label)
    template_layout.addWidget(template_combo)
    template_layout.addWidget(template_btn)
    template_layout.addStretch()
    layout.addLayout(template_layout)
    
    # Validate button
    validate_btn = QtWidgets.QPushButton("Validate Syntax")
    validate_btn.clicked.connect(lambda: _validate_advanced_code(parent, detail_advanced, format_type))
    layout.addWidget(validate_btn)
    
    # Help section
    help_text = QtWidgets.QLabel(
        "<b>Tips:</b><br/>"
        "• <b>Python:</b> Access source: <code>source['ColumnName']</code>, target: <code>col['ColumnName']</code><br/>"
        "• <b>Excel:</b> Use standard Excel formula syntax (A1, SUM, IF, etc.)<br/>"
        "• <b>Regex:</b> Use Python regex syntax with groups: <code>pattern</code> -> <code>replacement</code><br/>"
        "• Always return a value or the column will be empty"
    )
    help_text.setWordWrap(True)
    help_text.setStyleSheet("color: #666; font-size: 10px; background-color: #f0f0f0; padding: 8px;")
    layout.addWidget(help_text)
    
    return {
        'widget': widget,
        'editor': detail_advanced
    }


def _validate_advanced_code(parent, editor, format_type):
    """Validate the code based on format type."""
    code = editor.toPlainText()
    format_selection = format_type.currentText() if hasattr(format_type, 'currentText') else "Python Function"
    
    try:
        if "Python" in format_selection:
            compile(code, '<string>', 'exec')
            QtWidgets.QMessageBox.information(parent, "Validation", "Python syntax is valid ✓")
        elif "Excel" in format_selection:
            # Basic Excel formula validation
            if code.startswith('='):
                QtWidgets.QMessageBox.information(parent, "Validation", "Excel formula format looks valid ✓")
            else:
                QtWidgets.QMessageBox.warning(parent, "Validation", "Excel formulas should start with '='")
        elif "Regex" in format_selection:
            import re
            if '->' in code:
                pattern, replacement = code.split('->')
                re.compile(pattern.strip())
                QtWidgets.QMessageBox.information(parent, "Validation", "Regex pattern is valid ✓")
            else:
                QtWidgets.QMessageBox.warning(parent, "Validation", "Regex should be in format: pattern -> replacement")
    except SyntaxError as e:
        QtWidgets.QMessageBox.critical(parent, "Validation Error", f"Syntax error:\n{e}")
    except Exception as e:
        QtWidgets.QMessageBox.warning(parent, "Validation", f"Warning:\n{e}")
