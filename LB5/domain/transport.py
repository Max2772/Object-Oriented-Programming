from dataclasses import dataclass


@dataclass
class Transport:
    name: str
    cost_per_km: float
    speed_kmh: float

    def delivery_cost(self, distance: float) -> float:
        return distance * self.cost_per_km

    def delivery_time(self, distance: float) -> float:
        return round(distance / self.speed_kmh, 2)
