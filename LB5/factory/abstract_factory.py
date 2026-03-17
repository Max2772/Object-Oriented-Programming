from abc import ABC, abstractmethod
from typing import List

from LB5.domain.cargo import Cargo
from LB5.domain.shipment import Shipment
from LB5.domain.transport import Transport


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

    @abstractmethod
    def get_all_transports(self) -> List[Transport]:
        pass