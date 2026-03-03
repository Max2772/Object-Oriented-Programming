from abc import ABC, abstractmethod

from LB4.domain.cargo import Cargo
from LB4.domain.transport import Transport


class LogisticFactory(ABC):
    @abstractmethod
    def create_cargo(self, name: str) -> Cargo:
        pass

    @abstractmethod
    def create_transport(self, name: str) -> Transport:
        pass
