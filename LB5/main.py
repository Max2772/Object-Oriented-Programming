import json
from pathlib import Path

from LB5.application.logistic_system import LogisticSystem
from LB5.exporters.csv_exporter import CSVExporter
from LB5.exporters.decorators import CompressedExporter, EncryptedExporter
from LB5.exporters.json_exporter import JSONExporter
from LB5.factory.csv_factory import CSVLogisticFactory
from LB5.factory.json_factory import JSONLogisticFactory
from LB5.factory.xml_factory import XMLLogisticFactory
from LB5.processing.filtering import FieldFilter
from LB5.processing.sorting import MultiFieldSort

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent / "data"

    csv_path = str(data_path / "logistic.csv")
    json_path = str(data_path / "logistic.json")
    xml_path = str(data_path / "logistic.xml")

    csv_factory = CSVLogisticFactory(csv_path)
    json_factory = JSONLogisticFactory(json_path)
    xml_factory = XMLLogisticFactory(xml_path)

    if (
            csv_factory.get_all_transports()
            == json_factory.get_all_transports()
            == xml_factory.get_all_transports()
    ):
        print("Данные из CSV/JSON/XML совпали\n")

    system = LogisticSystem(csv_factory)

    distance = 1200
    cargo_batch = {
        "Электроника": 10,
        "Одежда": 50
    }

    # Указываем транспорт
    transport_name = "Грузовик (Земля)"
    results = system.get_delivery_options(cargo_batch, distance, transport_name)
    print(f"Результат по варианту доставки - {transport_name}:")
    for r in results:
        print(f"\t{r.transport_name}: {r.total_cost:.2f} руб., {r.delivery_time:.2f} ч.\n")


    # Не указываем транспорт
    results = system.get_delivery_options(cargo_batch, distance)
    print("Все варианты доставки:")
    for r in results:
        print(f"\t{r.transport_name}: {r.total_cost:.2f} руб., {r.delivery_time:.2f} ч.")

    # Фильтрация
    cost_filter = FieldFilter('total_cost', '<', 200000)
    filtered = cost_filter.apply(results)
    print("\nПосле фильтрации (total_cost < 200000):")
    for r in filtered:
        print(f"\t{r.transport_name}: {r.total_cost:.2f} руб., {r.delivery_time:.2f} ч.")

    # Сортировка
    sorter = MultiFieldSort([('delivery_time', False), ('total_cost', True)])
    sorted_results = sorter.apply(filtered)
    print("\nПосле сортировки (время по возрастанию, стоимость по убыванию):")
    for r in sorted_results:
        print(f"\t{r.transport_name}: {r.delivery_time:.2f} ч., {r.total_cost:.2f} руб.")

    # Экспорт в JSON/CSV/XML
    json_exporter = JSONExporter()
    csv_exporter = CSVExporter()

    json_file_name = 'json_results.json'
    csv_file_name = 'csv_results.csv'

    json_exported = json_exporter.export(sorted_results, json_file_name)
    csv_exported = csv_exporter.export(sorted_results, csv_file_name)

    # Сжатие для JSON/CSV
    compressed_json_file_name = 'json_results.zip'
    compressed_csv_file_name = 'csv_results.zip'

    compressed_json_exporter = CompressedExporter(
        json_exporter,
        internal_filename=json_file_name
    )
    compressed_json_exporter.export(sorted_results, compressed_json_file_name)

    compressed_csv_expoter = CompressedExporter(
        csv_exporter,
        internal_filename=csv_file_name
    )
    compressed_csv_expoter.export(sorted_results, compressed_csv_file_name)

    # Шифрование JSON/CSV
    encrypted_json_file_name = 'json_results.enc'
    encrypted_csv_file_name = 'csv_results.enc'

    encrypted_json_exporter = EncryptedExporter(
        json_exporter,
        key="mypassword",
        internal_filename=json_file_name
    )
    encrypted_json = encrypted_json_exporter.export(
        sorted_results,
        encrypted_json_file_name
    )

    encrypted_csv_exporter = EncryptedExporter(
        csv_exporter,
        key="mypassword",
        internal_filename=csv_file_name
    )
    encrypted_csv = encrypted_csv_exporter.export(
        sorted_results,
        encrypted_csv_file_name
    )

    # Расшифрование JSON/CSV
    if(
            encrypted_json_exporter.decrypt(encrypted_json) == json_exported
            and
            encrypted_csv_exporter.decrypt(encrypted_csv) == csv_exported
    ):
        print("Расшифрованные данные из JSON/CSV совпали\n")

        print(f"\nРасшифрованное содержимое {encrypted_json_file_name}:")
        raw = encrypted_json_exporter.decrypt(encrypted_json)
        data = json.loads(raw)
        print(json.dumps(data, indent=4, ensure_ascii=False))

        print(f"\nРасшифрованное содержимое {encrypted_csv_file_name}:")
        raw = encrypted_csv_exporter.decrypt(encrypted_csv)
        for line in raw.decode("utf-8").splitlines():
            print(line)
