from abc import ABC, abstractmethod


class WarehouseWorker(ABC):
    @abstractmethod
    def process_order(self) -> None:
        pass

    @abstractmethod
    def attend_meeting(self) -> None:
        pass

    @abstractmethod
    def get_rest(self) -> None:
        pass

    @abstractmethod
    def swinging_the_lead(self) -> None:
        pass


class HumanManager(WarehouseWorker):
    def process_order(self) -> None:
        print("Manager is processing logic...")

    def attend_meeting(self) -> None:
        print("Manager is boring at the meeting...")

    def get_rest(self) -> None:
        print("Manager is taking a break...")

    def swinging_the_lead(self) -> None:
        print("Manager is watching reels...")


class RobotPacker(WarehouseWorker):
    def __init__(self, model: str):
        self.model = model

    def process_order(self) -> None:
        print(f"Robot {self.model} is packing boxes...")

    def attend_meeting(self) -> None:
        print("ERROR: Robot cannot attend meetings")

    def get_rest(self) -> None:
        print("Robot was taken for maintenance")

    def swinging_the_lead(self) -> None:
        raise RuntimeError("CRITICAL ERROR: Robot cannot waste our money (we hope so)")


def manage_warehouse(workers):
    print("\n--- Warehouse Shift Started ---")
    for worker in workers:
        try:
            worker.process_order()
            worker.attend_meeting()
            worker.get_rest()
            worker.swinging_the_lead()
        except RuntimeError as e:
            print(f"Worker error caught: {e}")