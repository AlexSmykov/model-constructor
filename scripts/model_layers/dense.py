from typing import Type

from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter
from scripts.hyper_parameters.neuron_count import NeuronCount
from scripts.model_layers.abstract_layer import AbstractLayer


class Dense(AbstractLayer):
    @property
    def hyper_parameters(self) -> list[Type[AbstractHyperparameter]]:
        return [NeuronCount]
