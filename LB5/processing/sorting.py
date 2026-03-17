from abc import ABC, abstractmethod
from typing import List, Tuple

from LB5.types.dto.delivery_result import DeliveryResult


class Sort(ABC):
    @abstractmethod
    def apply(self, results: List[DeliveryResult]) -> List[DeliveryResult]:
        pass


class MultiFieldSort(Sort):
    def __init__(self, fields: List[Tuple[str, bool]]):
        self.fields = fields

    def apply(self, results: List[DeliveryResult]) -> List[DeliveryResult]:
        for field, reverse in reversed(self.fields):
            results.sort(key=lambda x: getattr(x, field), reverse=reverse)
        return results
