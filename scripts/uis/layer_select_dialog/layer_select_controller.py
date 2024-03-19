from PyQt5.QtWidgets import QDialog

from scripts.enums.layers_enum import ELayers
from scripts.uis.abstract_controller import AbstractController
from scripts.uis.layer_select_dialog.layer_select_ui import Ui_select_layer


class LayerSelectController(AbstractController):
    dialog = None
    ui = None

    def __init__(self):
        self.dialog = QDialog()
        self.ui = Ui_select_layer()

        self.ui.setupUi(self.dialog)
        self._set_connections()

        self.ui.layer_select.clear()
        for key, value in ELayers.items():
            self.ui.layer_select.addItem(value['text'], key)

    def _set_connections(self) -> None:
        self.ui.select_layer_button.clicked.connect(self.dialog.close)
