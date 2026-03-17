import csv
import io
from typing import List

from LB5.exporters.abstract_exporter import Exporter
from LB5.types.dto.delivery_result import DeliveryResult


class CSVExporter(Exporter):
    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')

        writer.writerow(['Транспорт', 'Общая стоимость', 'Время доставки', 'Расстояние'])
        for res in results:
            writer.writerow([res.transport_name, res.total_cost, res.delivery_time, res.distance])

        data = output.getvalue().encode('utf-8')

        if file_path:
            self.save(data, file_path)

        return data

