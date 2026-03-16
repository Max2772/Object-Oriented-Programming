from dataclasses import dataclass


@dataclass
class Cargo:
    name: str
    unit_mass: float
    price_per_kg: float

    def delivery_cost(self, quantity: int) -> float:
        total_mass = self.unit_mass * quantity
        return total_mass * self.price_per_kg
