from abc import ABC, abstractmethod


class AbstractHyperparameter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def precision(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def min_value(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def max_value(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def current_value(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def step_size(self) -> float:
        raise NotImplementedError
