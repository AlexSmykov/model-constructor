from abc import ABC, abstractmethod
from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter


class AbstractLayer(ABC):
    @property
    @abstractmethod
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        raise NotImplementedError
