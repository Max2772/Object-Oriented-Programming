import xml.etree.ElementTree as ET
from typing import List, Dict

from LB5.domain.cargo import Cargo
from LB5.domain.shipment import Shipment
from LB5.domain.transport import Transport
from LB5.factory.abstract_factory import LogisticFactory


class XMLLogisticFactory(LogisticFactory):
    def __init__(self, xml_path: str):
        self._cargo_data: Dict[str, Cargo] = {}
        self._transport_data: Dict[str, Transport] = {}
        self._read_xml_file(xml_path)

    def _read_xml_file(self, xml_path: str):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for cargo_elem in root.findall('cargos/cargo'):
            cargo = Cargo(
                cargo_elem.get('name'),
                float(cargo_elem.get('unit_mass_kg')),
                float(cargo_elem.get('price_per_kg'))
            )
            self._cargo_data[cargo.name] = cargo
        for trans_elem in root.findall('transports/transport'):
            transport = Transport(
                trans_elem.get('name'),
                float(trans_elem.get('cost_per_km')),
                float(trans_elem.get('speed_kmh'))
            )
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

    def get_all_transports(self) -> List[Transport]:
        return list(self._transport_data.values())
