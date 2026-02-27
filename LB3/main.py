from models import Item, Address, Order
from processor import OrderProcessor
from staff import HumanManager, RobotPacker, manage_warehouse
import logging
import sys

def main():
    # 1. Создание заказа
    order = Order(
        id="ORD-256-X",
        type="Premium",
        items=[
            Item(id="1", name="Thermal Clips", price=1500.0),
            Item(id="2", name="UNATCO Pass Card", price=50.0),
        ],
        client_email="jeevacation@gmail.com",
        destination=Address(city="Agartha", street="33 Thomas Street", zip="[REDACTED]")
    )

    # 2. Инициализация процессора
    processor = OrderProcessor()

    # 3. Обработка заказа
    try:
        processor.process(order)
    except Exception as e:
        logging.exception("Failed to process order")
        sys.exit(1)

    # 4. Работа с обслуживанием
    print("\nTesting Warehouse Stuff:")
    workers = [
        HumanManager(),
        RobotPacker(model="George Droid"),
    ]

    manage_warehouse(workers)


if __name__ == "__main__":
    main()