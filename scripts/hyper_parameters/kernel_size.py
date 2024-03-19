from scripts.hyper_parameters.abstract_hyperparameter import AbstractHyperparameter


class KernelSize(AbstractHyperparameter):
    @property
    def name(self) -> str:
        return 'Kernel size'

    @property
    def min_value(self) -> float:
        return 1

    @property
    def max_value(self) -> float:
        return 101

    @property
    def current_value(self) -> float:
        return 1

    @property
    def step_size(self) -> float:
        return 2

    @property
    def precision(self) -> int:
        return 0
