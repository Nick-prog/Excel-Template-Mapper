from typing import Callable, Tuple
from PySide6 import QtWidgets

def create_bottom_row(
    parent: QtWidgets.QWidget, 
    on_export: Callable[[], None], 
    on_import: Callable[[], None], 
    on_preview: Callable[[], None], 
    on_save: Callable[[], None]
) -> Tuple[QtWidgets.QHBoxLayout, QtWidgets.QCheckBox, QtWidgets.QPushButton, QtWidgets.QPushButton, QtWidgets.QPushButton, QtWidgets.QPushButton]:
    bottom_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
    drop_blank_chk: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Drop rows where all mapped target columns are blank", parent)
    bottom_row.addWidget(drop_blank_chk)
    bottom_row.addStretch(1)
    btn_export: QtWidgets.QPushButton = QtWidgets.QPushButton("Export Mapping", parent)
    btn_export.clicked.connect(on_export)
    btn_import: QtWidgets.QPushButton = QtWidgets.QPushButton("Import Mapping", parent)
    btn_import.clicked.connect(on_import)
    btn_preview: QtWidgets.QPushButton = QtWidgets.QPushButton("Preview", parent)
    btn_preview.clicked.connect(on_preview)
    btn_save: QtWidgets.QPushButton = QtWidgets.QPushButton("Download", parent)
    btn_save.clicked.connect(on_save)
    bottom_row.addWidget(btn_export)
    bottom_row.addWidget(btn_import)
    bottom_row.addWidget(btn_preview)
    bottom_row.addWidget(btn_save)
    return bottom_row, drop_blank_chk, btn_export, btn_import, btn_preview, btn_save
