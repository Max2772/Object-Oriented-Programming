from decimal import Decimal

class Weather:
    def __init__(self, temperature: Decimal):
        self.temperature = temperature
    
    def to_dict(self):
        return {
            "temperature": float(self.temperature)
        }
