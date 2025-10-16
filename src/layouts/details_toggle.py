from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyle

def create_details_toggle(parent, on_toggle_details):
    details_toggle = QtWidgets.QToolButton(parent)
    details_toggle.setText("Show Details")
    details_toggle.setCheckable(True)
    details_toggle.setChecked(False)
    details_toggle.setIcon(parent.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
    details_toggle.toggled.connect(on_toggle_details)
    return details_toggle
