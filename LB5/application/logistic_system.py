from typing import Dict, List, Optional

from LB5.types.dto.delivery_result import DeliveryResult
from LB5.domain.transport import Transport
from LB5.factory.abstract_factory import LogisticFactory


class LogisticSystem:
    def __init__(self, factory: LogisticFactory):
        self.factory = factory

    def get_delivery_options(
            self,
            cargo_orders: Dict[str, int],
            distance: float,
            transport_name: Optional[str] = None
    ) -> List[DeliveryResult]:
        if transport_name:
            transport = self.factory.get_transport(transport_name)
            return [self._compute_for_transport(transport, cargo_orders, distance)]
        else:
            transports = self.factory.get_all_transports()
            results = []
            for transport in transports:
                results.append(self._compute_for_transport(transport, cargo_orders, distance))
            return results

    def _compute_for_transport(
            self,
            transport: Transport,
            cargo_orders: Dict[str, int],
           distance: float
    ) -> DeliveryResult:
        shipment = self.factory.create_shipment(transport, distance)
        for cargo_name, quantity in cargo_orders.items():
            cargo = self.factory.get_cargo(cargo_name)
            shipment.add_cargo(cargo, quantity)
        return DeliveryResult(
            transport_name=transport.name,
            total_cost=shipment.total_cost(),
            delivery_time=shipment.delivery_time(),
            distance=distance,
            cargo_items=cargo_orders.copy()
        )