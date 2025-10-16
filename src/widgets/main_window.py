import json
from typing import Dict, Any, List, Optional, Union
from PySide6 import QtCore, QtGui, QtWidgets
from ..core.models import MappingSpec, ColumnMapping, TRANSFORM_CHOICES, TYPE_CHOICES
from ..core.engine import build_initial_spec, generate_preview_data, apply_template
from ..core.utils import read_workbook_headers, safe_str
from .mapping_table import MappingTable
from .preview_dialog import PreviewDialog

class MainWindow(QtWidgets.QMainWindow):
    def on_table_selection(self, row: int) -> None:
        sm = self.current_sheet()
        if not sm:
            return
        if row < 0 or row >= len(sm.columns):
            return
        col: ColumnMapping = sm.columns[row]
        self.selected_column = col  # Ensure advanced formatting targets the correct column
        self.detail_target.setText(col.target)
        self.detail_type.setCurrentText(col.data_type or "general")
        self.detail_format.setText(col.number_format or "")
        self.detail_tfbtn.set_values(col.transforms or [])
        self.detail_default.setText(col.default or "")
        self.detail_advanced.setPlainText(getattr(col, "advanced_format", ""))

    def on_toggle_details(self, checked: bool) -> None:
        self.details_widget.setVisible(checked)
        self.details_toggle.setText("Hide Details" if checked else "Show Details")
        if checked:
            icon: QtGui.QIcon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowUp)
        else:
            icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack)
        self.details_toggle.setIcon(icon)

    def on_load_files(self) -> None:
        template_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Template Workbook", filter="Excel (*.xlsx)")
        if not template_path:
            return
        source_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Source Workbook", filter="Excel (*.xlsx)")
        if not source_path:
            return
        try:
            template_headers: Dict[str, List[str]] = read_workbook_headers(template_path)
            source_headers: Dict[str, List[str]] = read_workbook_headers(source_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Load Files", f"Failed to read headers:\n{e}")
            return
        try:
            self.spec = build_initial_spec(template_path, source_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Load Files", f"Failed to build mapping spec:\n{e}")
            return
        self.template_headers = template_headers
        self.source_headers = source_headers
        self.template_label.setText(f"Template: {template_path}")
        self.source_label.setText(f"Source: {source_path}")
        if self.spec and hasattr(self.spec, 'sheets'):
            self.target_combo.clear()
            self.target_combo.addItems([s.target_sheet for s in self.spec.sheets])
            self.refresh_sheet_ui()
            QtWidgets.QMessageBox.information(self, "Load Files", "Files loaded and mapping initialized.")

    def on_target_sheet_change(self, idx: int) -> None:
        self.refresh_sheet_ui()

    def on_source_sheet_change(self, idx: int) -> None:
        pass

    def on_automap(self) -> None:
        import difflib
        sm = self.current_sheet()
        if not sm or not sm.source_sheet:
            return
        source_headers: List[str] = self.source_headers.get(sm.source_sheet, [])
        norm_sources: List[str] = [src.lower().replace(" ", "").replace("_", "") for src in source_headers]
        for col in sm.columns:
            norm_target: str = col.target.lower().replace(" ", "").replace("_", "")
            # Exact match
            if norm_target in norm_sources:
                idx: int = norm_sources.index(norm_target)
                col.source = source_headers[idx]
            else:
                # Fuzzy match on normalized names
                close: List[str] = difflib.get_close_matches(norm_target, norm_sources, n=1, cutoff=0.6)
                if close:
                    idx = norm_sources.index(close[0])
                    col.source = source_headers[idx]
                else:
                    col.source = None
        self.refresh_table()

    def current_sheet(self) -> Optional[Any]:
        if not self.spec or self.target_combo.count() == 0:
            return None
        idx: int = max(0, self.target_combo.currentIndex())
        return self.spec.sheets[idx]

    def apply_from_table(self) -> None:
        sm = self.current_sheet()
        if not sm:
            return
        sm.drop_if_all_blank = self.drop_blank_chk.isChecked()
        self.table.apply_sources_to_spec(sm)
        rows = self.table.selectionModel().selectedRows()
        if rows:
            self.on_apply_details()

    def refresh_sheet_ui(self) -> None:
        sm = self.current_sheet()
        if not sm:
            return
        self.source_sheet_combo.blockSignals(True)
        self.source_sheet_combo.clear()
        self.source_sheet_combo.addItems(list(self.source_headers.keys()))
        if sm.source_sheet:
            ix: int = self.source_sheet_combo.findText(sm.source_sheet)
            if ix >= 0:
                self.source_sheet_combo.setCurrentIndex(ix)
        self.source_sheet_combo.blockSignals(False)
        self.drop_blank_chk.setChecked(bool(sm.drop_if_all_blank))
        self.refresh_table()

    def refresh_table(self) -> None:
        sm = self.current_sheet()
        if not sm:
            return
        src: List[str] = self.source_headers.get(sm.source_sheet, []) if sm.source_sheet else []
        self.table.build_rows(sm, src)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Excel Template Maker (Qt/PySide6)")
        self.resize(880, 680)
        self.spec: Optional[MappingSpec] = None
        self.template_headers: Dict[str, List[str]] = {}
        self.source_headers: Dict[str, List[str]] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        from ..layouts.top_file_row import create_top_file_row
        from ..layouts.source_label_row import create_source_label_row
        from ..layouts.sheet_row import create_sheet_row
        from ..layouts.details_toggle import create_details_toggle
        from ..layouts.details_widget import create_details_widget
        from ..layouts.bottom_row import create_bottom_row

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        vbox = QtWidgets.QVBoxLayout(central)

        file_row, self.template_label, btn_load = create_top_file_row(self, self.on_load_files)
        vbox.addLayout(file_row)
        source_row, self.source_label = create_source_label_row(self)
        vbox.addLayout(source_row)
        sheet_row, self.target_combo, self.source_sheet_combo, btn_automap = create_sheet_row(
            self,
            self.on_target_sheet_change,
            self.on_source_sheet_change,
            self.on_automap
        )
        vbox.addLayout(sheet_row)
        self.table = MappingTable(self)
        vbox.addWidget(self.table, stretch=1)
        self.table.selectionChangedSignal.connect(self.on_table_selection)
        self.details_toggle = create_details_toggle(self, self.on_toggle_details)
        vbox.addWidget(self.details_toggle)
        (self.details_widget, self.detail_target, self.detail_type, self.detail_format,
         self.detail_tfbtn, self.detail_default, self.detail_advanced, self.detail_apply) = create_details_widget(self, self.on_apply_details)
        vbox.addWidget(self.details_widget)
        bottom_row, self.drop_blank_chk, btn_export, btn_import, btn_preview, btn_save = create_bottom_row(
            self,
            self.on_export,
            self.on_import,
            self.on_preview,
            self.on_save
        )
        vbox.addLayout(bottom_row)

    def on_export(self) -> None:
        if not self.spec:
            return
        self.apply_from_table()
        only_current, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Export Option",
            "Export only current mapped sheet?",
            ["No (all sheets)", "Yes (current sheet only)"],
            0,
            False
        )
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Mapping JSON", filter="JSON (*.json)")
        if not path:
            return
        try:
            spec_to_export: MappingSpec = self.spec
            if only_current == "Yes (current sheet only)":
                idx: int = self.target_combo.currentIndex()
                from copy import deepcopy
                spec_to_export = deepcopy(self.spec)
                spec_to_export.sheets = [spec_to_export.sheets[idx]]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(spec_to_export.to_dict(), f, indent=2)
            QtWidgets.QMessageBox.information(self, "Export", f"Saved to:\n{path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Export", f"Failed to save mapping:\n{e}")

    def on_import(self) -> None:
        if not self.spec:
            return
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import Mapping JSON", filter="JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
            new_spec: MappingSpec = MappingSpec.from_dict(data)
            # Ensure template/source paths are present
            if not new_spec.template_path:
                new_spec.template_path = self.spec.template_path
            if not new_spec.source_path:
                new_spec.source_path = self.spec.source_path
            # Ensure sheets is always a list
            if not hasattr(new_spec, 'sheets') or not isinstance(new_spec.sheets, list):
                if hasattr(new_spec, 'sheets') and new_spec.sheets:
                    if isinstance(new_spec.sheets, list):
                        pass  # already a list, do nothing
                    else:
                        new_spec.sheets = [new_spec.sheets]
                else:
                    QtWidgets.QMessageBox.critical(self, "Import", "Imported mapping is missing sheet data.")
                    return
            self.spec = new_spec
            # Refresh all UI elements for new spec
            self.target_combo.clear()
            self.target_combo.addItems([s.target_sheet for s in self.spec.sheets])
            self.refresh_sheet_ui()
            QtWidgets.QMessageBox.information(self, "Import", "Mapping imported.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Import", f"Failed to import mapping:\n{e}")

    def on_preview(self) -> None:
        if not self.spec:
            return
        self.apply_from_table()
        try:
            pv: Dict[str, Dict[str, Any]] = generate_preview_data(self.spec, max_rows_per_sheet=1000)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Preview", f"Failed to generate preview:\n{e}")
            return
        dlg: PreviewDialog = PreviewDialog(self.spec, pv, self)
        dlg.exec()

    def on_save(self) -> None:
        if not self.spec:
            return
        self.apply_from_table()
        only_current, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Download Option",
            "Download only current mapped sheet?",
            ["No (all sheets)", "Yes (current sheet only)"],
            0,
            False
        )
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Output Workbook", filter="Excel (*.xlsx)")
        if not out_path:
            return
        try:
            spec_to_download: MappingSpec = self.spec
            if only_current == "Yes (current sheet only)":
                idx: int = self.target_combo.currentIndex()
                from copy import deepcopy
                spec_to_download = deepcopy(self.spec)
                spec_to_download.sheets = [spec_to_download.sheets[idx]]
            apply_template(spec_to_download, out_path)
            QtWidgets.QMessageBox.information(self, "Download", f"Output saved to:\n{out_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Download", f"Failed to save output:\n{e}")

    def on_apply_details(self) -> None:
        sm = self.current_sheet()
        if not sm:
            return
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QtWidgets.QMessageBox.information(self, "Details", "Select a target row first.")
            return
        row: int = rows[0].row()
        col: ColumnMapping = sm.columns[row]
        col.data_type = self.detail_type.currentData() or "general"
        col.number_format = self.detail_format.text()
        col.transforms = self.detail_tfbtn.values()
        col.default = self.detail_default.text()
        col.advanced_format = self.detail_advanced.toPlainText()
        QtWidgets.QMessageBox.information(self, "Details", f"Applied settings to: {col.target}")