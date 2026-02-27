import time
import datetime
from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def save_order(self, order, total: float) -> None:
        pass


class RandomSQLDatabase(Database):
    """Имитация тяжелой базы"""
    def __init__(self, connection_string="random://root:password@localhost:228/shop"):
        self.connection_string = connection_string
        self.cache = set()

    def save_order(self, order, total: float) -> None:
        if order.id in self.cache:
            print("Заказ уже есть в кэше")
            return

        print(f"Connecting to RandomSQL at {self.connection_string} ...")
        time.sleep(0.5)

        record = f"[{datetime.datetime.now().isoformat()}] ID: {order.id} | Type: {order.type} | Total: {total:.2f}\n"
        with open("orders_db.txt", "a", encoding="utf-8") as f:
            f.write(record)

        self.cache.add(order.id)
        print("Order saved successfully.")


class Mailer(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        pass


class SmtpMailer(Mailer):
    def __init__(self, server="smtp.google.com"):
        self.server = server

    def send(self, to: str, subject: str, body: str) -> None:
        print(f">> Sending EMAIL to {to} | Subject: {subject} | Body: {body}")


class TelegramNotifier(Mailer):
    def __init__(self, chat_id: str):
        self.chat_id = chat_id

    def send(self, to: str, subject: str, body: str) -> None:
        print(f">> Sending Telegram to {self.chat_id} | Message: {subject} - {body}")


class Logger(Mailer):
    def __init__(self, logfile="events.log"):
        self.logfile = logfile

    def send(self, to: str, subject: str, body: str) -> None:
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {subject}: {body}\n")
        print(f">> Logged event: {subject}")