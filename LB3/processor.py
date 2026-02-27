from models import Order
from infrastructure import Database, Mailer
from discount import get_discount_card


class OrderProcessor:
    def __init__(self, database: Database, notifiers: list[Mailer]):
        self.database = database
        self.notifiers = notifiers

    def process(self, order: Order) -> None:

        # 1. Валидация
        if not order.items:
            raise ValueError("Order must have at least one item")
        if not order.destination.city:
            raise ValueError("destination city is required")

        # 2. Расчёт суммы
        total = sum(item.price for item in order.items)

        # 3. Скидки и налоги
        match order.type:
            case "Standard":
                total *= 1.2
            case "Premium":
                total = total * 0.9 * 1.2
            case "Budget":
                if len(order.items) > 3:
                    print("Budget orders cannot have more than 3 items. Skipping.")
                    return None
            case "International":
                total *= 1.5
                if order.destination.city == "Nowhere":
                    raise ValueError("Cannot ship to Nowhere")
            case _:
                raise ValueError("Unknown order type")

        card = get_discount_card(order.discount_card)
        total = card.apply_discount(total)

        # 4. Сохранение
        self.database.save_order(order, total)

        # 5. Уведомление
        subject = f"Order {order.id} confirmed!"
        body = f"Total: {total:.2f}"
        for notifier in self.notifiers:
            notifier.send(order.client_email, subject, body)

        return None