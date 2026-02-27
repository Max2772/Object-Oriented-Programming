from abc import ABC, abstractmethod


class DiscountCard(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass


class GoldCard(DiscountCard):
    def apply_discount(self, total: float) -> float:
        return total * 0.85  # 15% discount


class SilverCard(DiscountCard):
    def apply_discount(self, total: float) -> float:
        return total * 0.9  # 10% discount


class NewbieCard(DiscountCard):
    def apply_discount(self, total: float) -> float:
        return total  # 0% discount


def get_discount_card(card_type: str) -> DiscountCard:
    return {
        "Gold": GoldCard(),
        "Silver": SilverCard(),
        "Newbie": NewbieCard(),
    }.get(card_type, NewbieCard())