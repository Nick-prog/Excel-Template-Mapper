from typing import Callable, Tuple
from PySide6 import QtWidgets

def create_sheet_row(
    parent: QtWidgets.QWidget, 
    on_target_sheet_change: Callable[[int], None], 
    on_source_sheet_change: Callable[[int], None], 
    on_automap: Callable[[], None]
) -> Tuple[QtWidgets.QHBoxLayout, QtWidgets.QComboBox, QtWidgets.QComboBox, QtWidgets.QPushButton]:
    sheet_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
    sheet_row.addWidget(QtWidgets.QLabel("Target sheet:", parent))
    target_combo: QtWidgets.QComboBox = QtWidgets.QComboBox(parent)
    target_combo.currentIndexChanged.connect(on_target_sheet_change)
    sheet_row.addWidget(target_combo)
    sheet_row.addSpacing(12)
    sheet_row.addWidget(QtWidgets.QLabel("Source sheet:", parent))
    source_sheet_combo: QtWidgets.QComboBox = QtWidgets.QComboBox(parent)
    source_sheet_combo.currentIndexChanged.connect(on_source_sheet_change)
    sheet_row.addWidget(source_sheet_combo)
    btn_automap: QtWidgets.QPushButton = QtWidgets.QPushButton("Auto-map columns", parent)
    btn_automap.clicked.connect(on_automap)
    sheet_row.addWidget(btn_automap)
    return sheet_row, target_combo, source_sheet_combo, btn_automap
