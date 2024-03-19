from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.model_layers.abstract_layer import AbstractLayer


class Sigmoid(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return []
