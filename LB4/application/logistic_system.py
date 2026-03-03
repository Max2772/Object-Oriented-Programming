from typing import Dict

from LB4.domain.shipment import Shipment
from LB4.factory.abstract_factory import LogisticFactory


class LogisticSystem:
    def __init__(self, factory: LogisticFactory):
        self.factory = factory

    def calculate_delivery(
            self,
            cargo_orders: Dict[str, int],
            transport_name: str,
            distance: float
    ) -> None:
        transport = self.factory.create_transport(transport_name)
        shipment = Shipment(transport, distance)

        for cargo_name, quantity in cargo_orders.items():
            cargo = self.factory.create_cargo(cargo_name)
            shipment.add_cargo(cargo, quantity)

        print("\n=== DELIVERY REPORT ===")
        print(f"Transport: {transport.name}")
        print(f"Distance: {distance} km")
        print(f"Total cost: {shipment.total_cost():.2f}")
        print(f"Estimated time: {shipment.delivery_time():.2f} hours")
