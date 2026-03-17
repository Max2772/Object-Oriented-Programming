from abc import ABC, abstractmethod
from typing import List

from LB5.types.dto.delivery_result import DeliveryResult


class Exporter(ABC):
    @abstractmethod
    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        pass

    def save(self, data: bytes, file_path: str):
        with open(file_path, "wb") as f:
            f.write(data)
        print(f"Экспорт в файл {file_path}")
