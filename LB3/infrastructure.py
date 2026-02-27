import datetime
import time


class RandomSQLDatabase:
    """Имитация тяжелой базы данных"""

    def __init__(self, connection_string: str = "random://root:password@localhost:228/shop"):
        self.connection_string = connection_string

    def save_order(self, order, total: float) -> None:
        print(f"Connecting to RandomSQL at {self.connection_string} ...")
        time.sleep(0.5)  # Имитация задержки сети

        record = "[{ts}] ID: {id} | Type: {typ} | Total: {total:.2f}\n".format(
            ts=datetime.datetime.now().isoformat(),
            id=order.id,
            typ=order.type,
            total=total
        )

        with open("orders_db.txt", "a", encoding="utf-8") as f:
            f.write(record)

        print("Order saved successfully.")


class SmtpMailer:
    """Имитация почтового сервиса"""

    def __init__(self, server: str = "smtp.google.com"):
        self.server = server

    def send_html_email(self, to: str, subject: str, body: str) -> None:
        print(f">> Connecting to SMTP server {self.server}...")
        print(f">> Sending EMAIL to {to}\n   Subject: {subject}\n   Body: {body}")
