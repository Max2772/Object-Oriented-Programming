from decimal import Decimal
from typing import List


class Forecast:
    def __init__(self, daily_max_temps: List[Decimal]):
        self.daily_max_temps = daily_max_temps

    def to_dict(self):
        return {
            "daily_max_temps": [float(t) for t in self.daily_max_temps],
        }
