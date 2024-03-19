from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.hyper_parameters.filters import Filters
from scripts.hyper_parameters.kernel_size import KernelSize
from scripts.model_layers.abstract_layer import AbstractLayer


class Convolution(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return [Filters, KernelSize]

