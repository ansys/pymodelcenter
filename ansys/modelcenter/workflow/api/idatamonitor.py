from abc import ABC, abstractmethod


class IDataMonitor(ABC):
    # TODO: Fill out all methods and properties

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError
