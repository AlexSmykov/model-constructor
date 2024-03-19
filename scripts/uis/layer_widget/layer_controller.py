from PyQt5.QtWidgets import QWidget

from scripts.model_layers.abstract_layer import AbstractLayer
from scripts.uis.abstract_controller import AbstractController, AbstractWidgetController
from scripts.uis.layer_widget.layer_ui import Ui_layer
from scripts.uis.parameter_widget.parameter_controller import ParameterController
from scripts.utils.flatten_array_of_dicts import flatten_array_of_dicts


class LayerController(AbstractController, AbstractWidgetController):
    widget: QWidget = None
    ui: Ui_layer = None
    parameters: list[ParameterController] = None

    def __init__(self, layer_item: dict[str, str, str, AbstractLayer]):
        self.widget = QWidget()
        self.ui = Ui_layer()
        self.parameters = []

        self.ui.setupUi(self.widget)
        self._set_layer_data(layer_item)
        self._set_connections()

    def _set_connections(self) -> None:
        pass

    def _set_layer_data(self, layer_item: dict[str, str, str, AbstractLayer]):
        self.ui.name.setText(layer_item['text'])
        layer_object: AbstractLayer = layer_item['class']()

        for parameter in layer_object.hyper_parameters:
            parameter_controller = ParameterController(parameter())
            layout_to_add = self.ui.parameters.layout()
            layout_to_add.insertWidget(layout_to_add.count() - 1, parameter_controller.widget)
            self.parameters.append(parameter_controller)

    def get_layer_data(self) -> dict[str: dict[str: float]]:
        return {
            self.ui.name.text(): flatten_array_of_dicts(list(map(lambda item: item.get_value(), self.parameters)))}

    def enable(self):
        map(lambda parameter: parameter.enable(), self.parameters)

    def disable(self):
        map(lambda parameter: parameter.disable(), self.parameters)
