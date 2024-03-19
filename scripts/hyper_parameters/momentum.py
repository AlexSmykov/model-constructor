from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter


class Momentum(AbstractHyperparameter):
    @property
    def name(self) -> str:
        return 'Momentum'

    @property
    def min_value(self) -> float:
        return 0

    @property
    def max_value(self) -> float:
        return 1

    @property
    def current_value(self) -> float:
        return 0.95

    @property
    def step_size(self) -> float:
        return 0.001

    @property
    def precision(self) -> int:
        return 3
