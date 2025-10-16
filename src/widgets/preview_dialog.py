from PySide6 import QtWidgets
from typing import Dict, Any
from ..core.models import MappingSpec

class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, spec: MappingSpec, preview: Dict[str, Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.resize(1000, 700)
        vbox = QtWidgets.QVBoxLayout(self)
        tabs = QtWidgets.QTabWidget(self)
        vbox.addWidget(tabs)
        for sm in spec.sheets:
            sheet_name = sm.target_sheet
            data = preview.get(sheet_name, {"headers": sm.target_headers, "rows": [], "truncated": False})
            tab = QtWidgets.QWidget()
            t_layout = QtWidgets.QVBoxLayout(tab)
            table = QtWidgets.QTableWidget()
            table.setColumnCount(len(data["headers"]))
            table.setHorizontalHeaderLabels(data["headers"])
            table.setRowCount(0)
            for r, row in enumerate(data["rows"]):
                table.insertRow(r)
                for c, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem("" if val is None else str(val))
                    table.setItem(r, c, item)
            if data.get("truncated"):
                lbl = QtWidgets.QLabel("Preview truncated")
                lbl.setStyleSheet("color:#a00")
                t_layout.addWidget(lbl)
            t_layout.addWidget(table)
            tabs.addTab(tab, sheet_name)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(self.reject)
        vbox.addWidget(btns)
