from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

class AdvancedCodeEdit(QtWidgets.QTextEdit):
    def keyPressEvent(self, event):
        # Qt.Key_Tab = 0x01000001
        if event.key() == 0x01000001:
            cursor = self.textCursor()
            cursor.insertText("    ")
            event.accept()
        # Qt.Key_Tab = 0x01000001, Qt.Key_Return = 0x01000004, Qt.Key_Enter = 0x01000005
        elif event.key() in (0x01000004, 0x01000005):
            cursor = self.textCursor()
            indent = self._auto_indent(cursor)
            if indent is None:
                indent = ""
            cursor.insertText("\n" + indent)
            event.accept()
        else:
            super().keyPressEvent(event)

    def _auto_indent(self, cursor):
        block = cursor.block()
        text = block.text()
        indent = ""
        for char in text:
            if char in (" ", "\t"):
                indent += char
            else:
                break
        return indent

class AdvancedFormatBuilderDialog(QtWidgets.QDialog):
    def __init__(self, parent, column_names, source_columns=None, initial_code=""):
        super().__init__(parent)
        self.setWindowTitle("Advanced Format Builder")
        self.resize(600, 500)
        layout = QtWidgets.QVBoxLayout(self)

        # Instructions and tips
        instructions = QtWidgets.QLabel(
            "Build advanced Python logic for this column.\n"
            "You can reference target columns as col['ColumnName'] and source columns as source['SourceName'].\n"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Show available columns
        col_group = QtWidgets.QGroupBox("Available Columns")
        col_layout = QtWidgets.QVBoxLayout(col_group)
        col_layout.addWidget(QtWidgets.QLabel("Target columns: " + ", ".join(column_names)))
        if source_columns:
            col_layout.addWidget(QtWidgets.QLabel("Source columns: " + ", ".join(source_columns)))
        layout.addWidget(col_group)

        # Column dropdown (target)
        col_row = QtWidgets.QHBoxLayout()
        col_label = QtWidgets.QLabel("Insert target column:")
        self.col_combo = QtWidgets.QComboBox()
        self.col_combo.addItems(column_names)
        col_row.addWidget(col_label)
        col_row.addWidget(self.col_combo)
        insert_btn = QtWidgets.QPushButton("Insert")
        insert_btn.clicked.connect(self.insert_column)
        col_row.addWidget(insert_btn)
        layout.addLayout(col_row)

        # Source column dropdown
        if source_columns:
            src_row = QtWidgets.QHBoxLayout()
            src_label = QtWidgets.QLabel("Insert source column:")
            self.src_combo = QtWidgets.QComboBox()
            self.src_combo.addItems(source_columns)
            src_row.addWidget(src_label)
            src_row.addWidget(self.src_combo)
            src_btn = QtWidgets.QPushButton("Insert")
            src_btn.clicked.connect(self.insert_source_column)
            src_row.addWidget(src_btn)
            layout.addLayout(src_row)

        # Snippet dropdown
        snippet_layout = QtWidgets.QHBoxLayout()
        snippet_label = QtWidgets.QLabel("Insert snippet:")
        self.snippet_combo = QtWidgets.QComboBox()
        self.snippet_combo.addItems([
            "If/Else (source)",
            "Reference target column",
            "Reference source column",
            "Return value",
        ])
        snippet_layout.addWidget(snippet_label)
        snippet_layout.addWidget(self.snippet_combo)
        snippet_btn = QtWidgets.QPushButton("Insert")
        snippet_btn.clicked.connect(self.insert_snippet)
        snippet_layout.addWidget(snippet_btn)
        layout.addLayout(snippet_layout)

        # Code editor
        self.code_edit = AdvancedCodeEdit()
        self.code_edit.setPlainText(initial_code)
        layout.addWidget(self.code_edit)

        # Validate button
        validate_btn = QtWidgets.QPushButton("Validate Python Syntax")
        validate_btn.clicked.connect(self.validate_code)
        layout.addWidget(validate_btn)

        # Dialog buttons
        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def insert_column(self):
        col_name = self.col_combo.currentText()
        cursor = self.code_edit.textCursor()
        cursor.insertText(f"col['{col_name}']")

    def insert_source_column(self):
        src_name = self.src_combo.currentText()
        cursor = self.code_edit.textCursor()
        cursor.insertText(f"source['{src_name}']")

    def insert_snippet(self):
        snippet = self.snippet_combo.currentText()
        cursor = self.code_edit.textCursor()
        if snippet == "If/Else (source)":
            code = (
                "def format_column(col, source):\n"
                "    if source['Gender'] == 'Male':\n"
                "        return 'M'\n"
                "    else:\n"
                "        return 'F'\n"
            )
            cursor.insertText(code)
        elif snippet == "Reference target column":
            code = (
                "def format_column(col, source):\n"
                "    return col['OtherColumn']\n"
            )
            cursor.insertText(code)
        elif snippet == "Reference source column":
            code = (
                "def format_column(col, source):\n"
                "    return source['Gender']\n"
            )
            cursor.insertText(code)
        elif snippet == "Return value":
            code = (
                "def format_column(col, source):\n"
                "    return value\n"
            )
            cursor.insertText(code)

    def validate_code(self):
        code = self.code_edit.toPlainText()
        try:
            compile(code, '<string>', 'exec')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Validation", f"Syntax error:\n{e}")
            return
        QtWidgets.QMessageBox.information(self, "Validation", "Python syntax is valid.")

    def get_code(self):
        return self.code_edit.toPlainText()