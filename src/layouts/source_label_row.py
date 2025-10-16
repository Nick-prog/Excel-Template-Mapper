from typing import Tuple
from PySide6 import QtWidgets

def create_source_label_row(parent: QtWidgets.QWidget) -> Tuple[QtWidgets.QHBoxLayout, QtWidgets.QLabel]:
    source_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
    source_label: QtWidgets.QLabel = QtWidgets.QLabel("Source: ", parent)
    source_row.addWidget(source_label)
    source_row.addStretch(1)
    return source_row, source_label
