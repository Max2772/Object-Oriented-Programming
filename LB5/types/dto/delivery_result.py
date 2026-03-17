from dataclasses import dataclass


@dataclass
class DeliveryResult:
    transport_name: str
    total_cost: float
    delivery_time: float
    distance: float
    cargo_items: dict
