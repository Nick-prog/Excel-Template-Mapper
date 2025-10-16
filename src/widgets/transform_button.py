from PySide6 import QtCore, QtGui, QtWidgets
from ..core.models import TRANSFORM_CHOICES

class TransformButton(QtWidgets.QToolButton):
    changed = QtCore.Signal(list)

    def __init__(self, initial: list | None = None, parent=None):
        super().__init__(parent)
        self.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        menu = QtWidgets.QMenu(self)
        self.setMenu(menu)
        self._actions = {}
        self._init_menu(initial or [], menu)
        self._sync_text()

    def _init_menu(self, initial: list, menu):
        for t in TRANSFORM_CHOICES:
            act = QtGui.QAction(t, menu)
            act.setCheckable(True)
            act.setChecked(t in initial)
            act.toggled.connect(self._on_toggled)
            menu.addAction(act)
            self._actions[t] = act

    def _on_toggled(self, _checked: bool):
        self._sync_text()
        self.changed.emit(self.values())

    def values(self) -> list:
        return [k for k, a in self._actions.items() if a.isChecked()]

    def set_values(self, vals: list):
        for k, a in self._actions.items():
            a.setChecked(k in vals)
        self._sync_text()

    def _sync_text(self):
        selected = self.values()
        self.setText(",".join(selected) if selected else "(none)")