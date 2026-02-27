from typing import Optional
from infrastructure import RandomSQLDatabase, SmtpMailer
from models import Order


class OrderProcessor:
    def __init__(self):
        self.database = RandomSQLDatabase()
        self.mailer = SmtpMailer()

    def process(self, order: Order) -> Optional[None]:
        print(f"--- Processing Order {order.id} ---")

        # 1. Валидация
        if not order.items or len(order.items) == 0:
            raise ValueError("order must have at least one item")
        if not order.destination.city:
            raise ValueError("destination city is required")

        # 2. Расчёт суммы
        total = 0.0
        for item in order.items:
            total += item.price

        # 3. Скидки и налоги
        match order.type:
            case "Standard":
                total = total * 1.2
            case "Premium":
                total = (total * 0.9) * 1.2
            case "Budget":
                if len(order.items) > 3:
                    print("Budget orders cannot have more than 3 items. Skipping.")
                    return None
            case "International":
                total = total * 1.5
                if order.destination.city == "Nowhere":
                    raise ValueError("cannot ship to Nowhere")
            case _:
                raise ValueError("unknown order type")

        # 4. Сохранение
        self.database.save_order(order, total)

        # 5. Уведомление
        email_body = f"<h1>Your order {order.id} is confirmed!</h1><p>Total: {total:.2f}</p>"
        self.mailer.send_html_email(order.client_email, "Order Confirmation", email_body)

        return None