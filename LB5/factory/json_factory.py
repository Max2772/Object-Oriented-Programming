import json

from LB5.domain.cargo import Cargo
from LB5.domain.shipment import Shipment
from LB5.domain.transport import Transport
from LB5.factory.abstract_factory import LogisticFactory


class JSONLogisticFactory(LogisticFactory):
    def __init__(self, json_path: str):
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        self._cargo_data = {}
        self._transport_data = {}
        for item in data.get('cargo', []):
            cargo = Cargo(item['name'], item['unit_mass_kg'], item['price_per_kg'])
            self._cargo_data[cargo.name] = cargo
        for item in data.get('transport', []):
            transport = Transport(item['name'], item['cost_per_km'], item['speed_kmh'])
            self._transport_data[transport.name] = transport

    def get_cargo(self, name: str) -> Cargo:
        if name not in self._cargo_data:
            raise ValueError(f"Cargo '{name}' not found")
        return self._cargo_data[name]

    def get_transport(self, name: str) -> Transport:
        if name not in self._transport_data:
            raise ValueError(f"Transport '{name}' not found")
        return self._transport_data[name]

    def create_shipment(self, transport: Transport, distance: float) -> Shipment:
        return Shipment(transport, distance)
