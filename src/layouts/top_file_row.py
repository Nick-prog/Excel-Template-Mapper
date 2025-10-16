from typing import Callable, Tuple
from PySide6 import QtWidgets

def create_top_file_row(parent: QtWidgets.QWidget, on_load_files: Callable[[], None]) -> Tuple[QtWidgets.QHBoxLayout, QtWidgets.QLabel, QtWidgets.QPushButton]:
    file_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
    template_label: QtWidgets.QLabel = QtWidgets.QLabel("Template: ", parent)
    btn_load: QtWidgets.QPushButton = QtWidgets.QPushButton("Load Files", parent)
    btn_load.clicked.connect(on_load_files)
    file_row.addWidget(template_label)
    file_row.addStretch(1)
    file_row.addWidget(btn_load)
    return file_row, template_label, btn_load
