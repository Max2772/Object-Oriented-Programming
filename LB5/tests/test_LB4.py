from pathlib import Path

import pytest

from LB5.application.logistic_system import LogisticSystem
from LB5.domain.cargo import Cargo
from LB5.domain.transport import Transport
from LB5.factory.csv_factory import CSVLogisticFactory


@pytest.fixture
def csv_factory():
    csv_path = str(Path(__file__).resolve().parent.parent / "data" / "logistic.csv")
    yield CSVLogisticFactory(csv_path)


def test_factory_loads_cargo_and_transport(csv_factory):
    cargo = csv_factory.get_cargo("Электроника")
    assert isinstance(cargo, Cargo)
    assert cargo.unit_mass == 1.5
    assert cargo.price_per_kg == 50

    transport = csv_factory.get_transport("Самолет (Воздух)")
    assert isinstance(transport, Transport)
    assert transport.cost_per_km == 150.0
    assert transport.speed_kmh == 850


def test_shipment_cost_and_time(csv_factory):
    transport = csv_factory.get_transport("Грузовик (Земля)")
    distance = 500
    shipment = csv_factory.create_shipment(transport, distance)

    cargo_electronics = csv_factory.get_cargo("Электроника")
    cargo_clothes = csv_factory.get_cargo("Одежда")
    shipment.add_cargo(cargo_electronics, 10)
    shipment.add_cargo(cargo_clothes, 50)

    expected_total = 1550 + 7500
    assert shipment.total_cost() == pytest.approx(expected_total)
    assert shipment.delivery_time() == pytest.approx(6.25)


def test_system_calculate_delivery(capsys, csv_factory):
    system = LogisticSystem(csv_factory)

    cargo_batch = {"Электроника": 10, "Одежда": 50}
    system.calculate_delivery(cargo_batch, "Самолет (Воздух)", 1200)
    output = capsys.readouterr().out

    assert "Transport: Самолет (Воздух)" in output
    assert "Distance: 1200 km" in output
    assert "Total cost: 181550.00" in output
    assert "Estimated time: 1.41 hours" in output


def test_factory_raises_on_missing_cargo(csv_factory):
    with pytest.raises(ValueError, match="Cargo 'Несуществующий' not found"):
        csv_factory.get_cargo("Несуществующий")


def test_factory_raises_on_missing_transport(csv_factory):
    with pytest.raises(ValueError, match="Transport 'Несуществующий' not found"):
        csv_factory.get_transport("Несуществующий")


def test_shipment_add_cargo(csv_factory):
    transport = csv_factory.get_transport("Поезд (Земля)")
    shipment = csv_factory.create_shipment(transport, 200)
    cargo = csv_factory.get_cargo("Оборудование")
    shipment.add_cargo(cargo, 2)
    assert shipment.total_cost() == 4600
