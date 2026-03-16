from typing import List

from LB5.domain.cargo import Cargo
from LB5.domain.transport import Transport


class Shipment:
    def __init__(self, transport: Transport, distance: float):
        self.transport = transport
        self.distance = distance
        self._cargo_list: List[tuple[Cargo, int]] = []

    def add_cargo(self, cargo: Cargo, quantity: int):
        self._cargo_list.append((cargo, quantity))

    def total_cost(self) -> float:
        cargo_cost = sum(
            cargo.delivery_cost(quantity)
            for cargo, quantity in self._cargo_list
        )

        transport_cost = self.transport.delivery_cost(self.distance)

        return cargo_cost + transport_cost

    def delivery_time(self) -> float:
        return self.transport.delivery_time(self.distance)
