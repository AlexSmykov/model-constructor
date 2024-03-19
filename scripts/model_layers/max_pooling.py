from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.hyper_parameters.pool_size import PoolSize
from scripts.model_layers.abstract_layer import AbstractLayer


class MaxPooling(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return [PoolSize]
