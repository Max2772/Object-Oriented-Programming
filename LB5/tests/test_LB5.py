import io
import zipfile
from pathlib import Path

import pytest

from LB5.application.logistic_system import LogisticSystem
from LB5.exporters.csv_exporter import CSVExporter
from LB5.exporters.decorators import CompressedExporter, EncryptedExporter
from LB5.exporters.json_exporter import JSONExporter
from LB5.factory.csv_factory import CSVLogisticFactory
from LB5.factory.json_factory import JSONLogisticFactory
from LB5.factory.xml_factory import XMLLogisticFactory
from LB5.processing.filtering import FieldFilter
from LB5.processing.sorting import MultiFieldSort
from LB5.types.dto.delivery_result import DeliveryResult

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture(params=[
    ("json_factory", "logistic.json"),
    ("csv_factory", "logistic.csv"),
    ("xml_factory", "logistic.xml")
])
def factory(request):
    name, filename = request.param
    path = str(DATA_DIR / filename)

    match name:
        case "json_factory":
            return JSONLogisticFactory(path)
        case "csv_factory":
            return CSVLogisticFactory(path)
        case "xml_factory":
            return XMLLogisticFactory(path)


def test_factory_loads(factory):
    cargo = factory.get_cargo("Электроника")
    assert cargo.unit_mass == 1.5
    assert cargo.price_per_kg == 50

    transport = factory.get_transport("Самолет (Воздух)")
    assert transport.cost_per_km == 150.0
    assert transport.speed_kmh == 850


def test_get_delivery_options_all(factory):
    system = LogisticSystem(factory)
    orders = {
        "Электроника": 10,
        "Одежда": 50
    }
    results = system.get_delivery_options(orders, 1200)
    assert len(results) == 5
    names = {r.transport_name for r in results}
    assert names == {
        "Грузовик (Земля)",
        "Поезд (Земля)",
        "Танкер (Вода)",
        "Самолет (Воздух)",
        "Вертолет (Воздух)"
    }


def test_filter_and_sort():
    results = [
        DeliveryResult("A", 100, 5, 100, {}),
        DeliveryResult("B", 200, 3, 100, {}),
        DeliveryResult("C", 150, 4, 100, {})
    ]

    f = FieldFilter('total_cost', '>', 120)
    filtered = f.apply(results)
    assert len(filtered) == 2
    assert {r.transport_name for r in filtered} == {"B", "C"}

    s = MultiFieldSort([('delivery_time', False)])
    sorted_res = s.apply(filtered)
    assert [r.delivery_time for r in sorted_res] == [3, 4]


def test_exporters():
    results = [DeliveryResult("Test", 123.45, 6.78, 500, {})]

    # JSON экспорт
    json_exporter = JSONExporter()
    data = json_exporter.export(results)
    assert b'Test' in data

    # CSV экспорт
    csv_exporter = CSVExporter()
    data_csv = csv_exporter.export(results)
    assert b'Test' in data_csv

    # Сжатие
    compressed_exporter = CompressedExporter(
        json_exporter,
        internal_filename='test.json'
    )
    zip_data = compressed_exporter.export(results)
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        assert 'test.json' in zf.namelist()

    # Шифрование
    encrypted_exp = EncryptedExporter(
        json_exporter,
        key="secret",
        internal_filename='test.json'
    )
    encrypted_data = encrypted_exp.export(results)
    assert encrypted_data != data

    # Расшифрование
    decrypted = encrypted_exp.decrypt(encrypted_data)
    assert decrypted == data

    # Комбинация: Cжать, Зашифровать
    compressed_exp = CompressedExporter(
        json_exporter,
        internal_filename='combined.json'
    )
    comp_then_enc = EncryptedExporter(
        compressed_exp,
        key="secret",
        internal_filename='combined.zip'
    )
    combined = comp_then_enc.export(results)

    with pytest.raises(zipfile.BadZipFile):
        zipfile.ZipFile(io.BytesIO(combined))

    # Расшифровать, Распаковать
    decrypted_zip = comp_then_enc.decrypt(combined)
    with zipfile.ZipFile(io.BytesIO(decrypted_zip)) as zf:
        print(zf.namelist())
        assert 'combined.json' in zf.namelist()
        with zf.open('combined.json') as f:
            content = f.read()
            assert content == data
