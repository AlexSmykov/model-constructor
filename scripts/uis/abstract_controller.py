from abc import ABC, abstractmethod


class AbstractController(ABC):
    @abstractmethod
    def _set_connections(self) -> None:
        raise NotImplementedError


class AbstractWidgetController(ABC):
    @abstractmethod
    def enable(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disable(self) -> None:
        raise NotImplementedError
