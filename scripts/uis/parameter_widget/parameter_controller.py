from PyQt5.QtWidgets import QWidget

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.uis.abstract_controller import AbstractController, AbstractWidgetController
from scripts.uis.parameter_widget.parameter_ui import Ui_model_parameter


class ParameterController(AbstractController, AbstractWidgetController):
    widget = None
    ui = None

    def __init__(self, parameter: AbstractHyperparameter):
        self.widget = QWidget()
        self.ui = Ui_model_parameter()

        self.ui.setupUi(self.widget)
        self._set_parameter_data(parameter)
        self._set_connections()

    def _set_connections(self) -> None:
        pass

    def _set_parameter_data(self, parameter: AbstractHyperparameter):
        self.ui.name.setText(parameter.name)

        self.ui.value_input.setDecimals(parameter.precision)
        self.ui.value_input.setValue(parameter.current_value)
        self.ui.value_input.setMaximum(parameter.max_value)
        self.ui.value_input.setMinimum(parameter.min_value)
        self.ui.value_input.setSingleStep(parameter.step_size)

    def get_value(self) -> dict[str: float]:
        return {self.ui.name.text(): self.ui.value_input.value()}

    def enable(self) -> None:
        self.ui.value_input.setEnabled(True)

    def disable(self) -> None:
        self.ui.value_input.setEnabled(False)
