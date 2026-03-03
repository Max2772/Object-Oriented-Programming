from LB4.application.logistic_system import LogisticSystem
from LB4.factory.csv_factory import CSVLogisticFactory


if __name__ == "__main__":
    factory = CSVLogisticFactory("data/logistic.csv")
    system = LogisticSystem(factory)

    cargo_batch = {
        "Электроника": 10,
        "Одежда": 50,
    }

    system.calculate_delivery(
        cargo_orders=cargo_batch,
        transport_name="Самолет (Воздух)",
        distance=1200
    )