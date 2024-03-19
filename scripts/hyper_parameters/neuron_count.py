from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter


class NeuronCount(AbstractHyperparameter):
    @property
    def name(self) -> str:
        return 'Neuron count'

    @property
    def min_value(self) -> float:
        return 1

    @property
    def max_value(self) -> float:
        return 10000

    @property
    def current_value(self) -> float:
        return 10

    @property
    def step_size(self) -> float:
        return 1

    @property
    def precision(self) -> int:
        return 0
