import sys
from typing import NoReturn
from PySide6 import QtWidgets
import json
from src.core.models import MappingSpec
from src.core.engine import generate_preview_data, apply_template
from src.widgets.preview_dialog import PreviewDialog
from src.widgets.main_window import MainWindow

def main() -> int:
    """Main entry point for the Excel Template Mapper application."""
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    win: MainWindow = MainWindow()
    win.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())