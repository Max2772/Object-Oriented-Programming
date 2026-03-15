import csv
from typing import Dict

from LB4.domain.cargo import Cargo
from LB4.domain.shipment import Shipment
from LB4.domain.transport import Transport
from LB4.factory.abstract_factory import LogisticFactory


class CSVLogisticFactory(LogisticFactory):
    def __init__(self, csv_path: str):
        self._cargo_data: Dict[str, Cargo] = {}
        self._transport_data: Dict[str, Transport] = {}
        self._read_csv_file(csv_path)

    def _read_csv_file(self, csv_path: str):
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                if row["Тип записи"] == "cargo":
                    cargo = Cargo(
                        name=row["Наименование"],
                        unit_mass=float(row["Масса_ед_кг"]),
                        price_per_kg=float(row["Стоимость_перевозки_за_кг"]),
                    )
                    self._cargo_data[cargo.name] = cargo
                elif row["Тип записи"] == "transport":
                    transport = Transport(
                        name=row["Наименование"],
                        cost_per_km=float(row["Расход_на_км"]),
                        speed_kmh=float(row["Скорость_км_ч"]),
                    )
                    self._transport_data[transport.name] = transport

    def get_cargo(self, name: str) -> Cargo:
        try:
            return self._cargo_data[name]
        except KeyError:
            raise ValueError(f"Cargo '{name}' not found in factory")

    def get_transport(self, name: str) -> Transport:
        try:
            return self._transport_data[name]
        except KeyError:
            raise ValueError(f"Transport '{name}' not found in factory")


    def create_shipment(self, transport: Transport, distance: float) -> Shipment:
        return Shipment(transport, distance)
