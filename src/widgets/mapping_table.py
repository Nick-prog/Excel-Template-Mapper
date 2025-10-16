from PySide6 import QtCore, QtWidgets

class MappingTable(QtWidgets.QTableWidget):
    HEADERS = [
        "Target",
        "Source",
    ]

    selectionChangedSignal = QtCore.Signal(int)  # row index

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        header = self.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        rows = self.selectionModel().selectedRows()
        if rows:
            self.selectionChangedSignal.emit(rows[0].row())

    def build_rows(self, sm, source_headers: list):
        self.setRowCount(0)
        for row_idx, col in enumerate(sm.columns):
            self.insertRow(row_idx)
            # Target label
            item = QtWidgets.QTableWidgetItem(col.target)
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
            self.setItem(row_idx, 0, item)
            # Source combo
            src_combo = QtWidgets.QComboBox()
            src_combo.addItem("(none)", None)
            for h in source_headers:
                src_combo.addItem(h, h)
            if col.source:
                ix = src_combo.findData(col.source)
                if ix >= 0:
                    src_combo.setCurrentIndex(ix)
            # Compact width for 13" screens
            src_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            src_combo.setMinimumContentsLength(10)
            self.setCellWidget(row_idx, 1, src_combo)

    def apply_sources_to_spec(self, sm):
        for row_idx, col in enumerate(sm.columns):
            src_combo: QtWidgets.QComboBox = self.cellWidget(row_idx, 1)  # type: ignore
            col.source = src_combo.currentData() or None