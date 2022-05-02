from abc import ABC, abstractmethod


class DataMonitor(ABC):
    # TODO: Fill out all methods and properties

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError
