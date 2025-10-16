from PySide6 import QtWidgets
from ..core.models import TYPE_CHOICES
from ..widgets.transform_button import TransformButton

def create_details_widget(parent, on_apply_details):
    details_widget = QtWidgets.QGroupBox("Selected Column Details", parent)
    details_widget.setVisible(False)
    dform = QtWidgets.QFormLayout(details_widget)
    detail_target = QtWidgets.QLabel("-", parent)
    dform.addRow("Target:", detail_target)
    detail_type = QtWidgets.QComboBox(parent)
    for t in TYPE_CHOICES:
        detail_type.addItem(t, t)
    dform.addRow("Type:", detail_type)
    detail_format = QtWidgets.QLineEdit(parent)
    dform.addRow("Format:", detail_format)
    detail_tfbtn = TransformButton([], parent)
    dform.addRow("Transforms:", detail_tfbtn)
    detail_default = QtWidgets.QLineEdit(parent)
    dform.addRow("Default:", detail_default)
    # Advanced formatting logic
    detail_advanced = QtWidgets.QTextEdit(parent)
    detail_advanced.setPlaceholderText("Advanced Python logic (e.g., if/else, reference other columns)")
    detail_advanced.setMinimumHeight(60)
    # Add builder button
    builder_btn = QtWidgets.QPushButton("Open Format Builder", parent)
    def open_builder():
        from .advanced_format_builder import AdvancedFormatBuilderDialog
        # Get all column names for dropdown
        # Only include the currently targeted column for advanced formatting
        col_names = []
        source_col_names = []
        if hasattr(parent, 'current_sheet') and parent.current_sheet():
            # Assume parent has a method or property for the selected column
            selected_col = getattr(parent, 'selected_column', None)
            if selected_col:
                col_names = [selected_col.target]
                if selected_col.source:
                    source_col_names = [selected_col.source]
            else:
                # Fallback: if no selected_column, use the first column
                if parent.current_sheet().columns:
                    col_names = [parent.current_sheet().columns[0].target]
                    if parent.current_sheet().columns[0].source:
                        source_col_names = [parent.current_sheet().columns[0].source]
        dialog = AdvancedFormatBuilderDialog(parent, col_names, source_col_names, detail_advanced.toPlainText())
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            detail_advanced.setPlainText(dialog.get_code())
    builder_btn.clicked.connect(open_builder)
    adv_layout = QtWidgets.QHBoxLayout()
    adv_layout.addWidget(detail_advanced)
    adv_layout.addWidget(builder_btn)
    dform.addRow("Advanced Formatting:", adv_layout)
    detail_apply = QtWidgets.QPushButton("Apply to Selected", parent)
    detail_apply.clicked.connect(on_apply_details)
    dform.addRow(detail_apply)
    return details_widget, detail_target, detail_type, detail_format, detail_tfbtn, detail_default, detail_advanced, detail_apply
