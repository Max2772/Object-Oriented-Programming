from infrastructure import RandomSQLDatabase, SmtpMailer, TelegramNotifier, Logger
from models import Order, Item, Address
from processor import OrderProcessor
from staff import HumanManager, RobotPacker, manage_warehouse


def main():
    order = Order(
        id="ORD-256-X",
        type="Premium",
        items=[
            Item(id="1", name="Thermal Clips", price=1500),
            Item(id="2", name="UNATCO Pass Card", price=50),
        ],
        client_email="jeevacation@gmail.com",
        destination=Address(city="Agartha", street="33 Thomas Street", zip="12345"),
        discount_card="Gold"
    )

    database = RandomSQLDatabase()
    notifiers = [
        SmtpMailer(),
        TelegramNotifier(chat_id="manager123"),
        Logger()
    ]

    print("\nTesting Orders:")
    processor = OrderProcessor(database, notifiers)
    processor.process(order)
    processor.process(order)

    print("\nTesting Warehouse:")
    staff = [
        HumanManager(),
        RobotPacker(model="George Droid"),
    ]
    manage_warehouse(staff)


if __name__ == "__main__":
    main()
