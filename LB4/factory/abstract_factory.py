from abc import ABC, abstractmethod

from LB4.domain.cargo import Cargo
from LB4.domain.shipment import Shipment
from LB4.domain.transport import Transport


class LogisticFactory(ABC):
    @abstractmethod
    def get_cargo(self, name: str) -> Cargo:
        pass

    @abstractmethod
    def get_transport(self, name: str) -> Transport:
        pass

    @abstractmethod
    def create_shipment(self, transport: Transport, distance: float) -> Shipment:
        pass