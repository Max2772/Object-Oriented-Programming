from abc import ABC, abstractmethod
from typing import List

from LB5.types.dto.delivery_result import DeliveryResult


class Filter(ABC):
    @abstractmethod
    def apply(self, results: List[DeliveryResult]) -> List[DeliveryResult]:
        pass


class FieldFilter(Filter):
    def __init__(self, field: str, op: str, value):
        self.field = field
        self.op = op
        self.value = value

    def apply(self, results: List[DeliveryResult]) -> List[DeliveryResult]:
        filtered = []
        for r in results:
            attr = getattr(r, self.field)
            if self.op == '==' and attr == self.value:
                filtered.append(r)
            elif self.op == '<' and attr < self.value:
                filtered.append(r)
            elif self.op == '>' and attr > self.value:
                filtered.append(r)
            elif self.op == '<=' and attr <= self.value:
                filtered.append(r)
            elif self.op == '>=' and attr >= self.value:
                filtered.append(r)
        return filtered
