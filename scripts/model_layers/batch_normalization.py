from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.hyper_parameters.momentum import Momentum
from scripts.hyper_parameters.epsilon import Epsilon
from scripts.model_layers.abstract_layer import AbstractLayer


class BatchNormalization(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return [Momentum, Epsilon]

