from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    id: str
    name: str
    price: float


@dataclass
class Address:
    city: str
    street: str
    zip: str


@dataclass
class Order:
    id: str
    items: List[Item]
    type: str  # "Standard", "Premium", "Budget", "International"
    client_email: str
    destination: Address
    discount_card: str = "Newbie"