from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.hyper_parameters.coefficient import Coefficient
from scripts.model_layers.abstract_layer import AbstractLayer


class Dropout(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return [Coefficient]
