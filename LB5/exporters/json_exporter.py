import json
from typing import List

from LB5.exporters.abstract_exporter import Exporter
from LB5.types.dto.delivery_result import DeliveryResult


class JSONExporter(Exporter):
    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        data = []
        for r in results:
            data.append({
                'transport_name': r.transport_name,
                'total_cost': r.total_cost,
                'delivery_time': r.delivery_time,
                'distance': r.distance,
                'cargo_items': r.cargo_items
            })

        data = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')

        if file_path:
            self.save(data, file_path)

        return data
