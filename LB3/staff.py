from abc import ABC, abstractmethod


class Worker(ABC):
    @abstractmethod
    def process_order(self) -> None:
        pass


class MeetingParticipant(ABC):
    @abstractmethod
    def attend_meeting(self):
        pass


class Restable(ABC):
    @abstractmethod
    def get_rest(self):
        pass


class LazyParticipant(ABC):
    @abstractmethod
    def swinging_the_lead(self):
        pass


class HumanManager(Worker, MeetingParticipant, Restable, LazyParticipant):
    def process_order(self) -> None:
        print("Manager is processing logic...")

    def attend_meeting(self) -> None:
        print("Manager is boring at the meeting...")

    def get_rest(self) -> None:
        print("Manager is taking a break...")

    def swinging_the_lead(self) -> None:
        print("Manager is watching reels...")


class RobotPacker(Worker):
    def __init__(self, model: str):
        self.model = model

    def process_order(self) -> None:
        print(f"Robot {self.model} is packing boxes...")

    # def attend_meeting(self) -> None:
    #     print("ERROR: Robot cannot attend meetings")
    #
    # def get_rest(self) -> None:
    #     print("Robot was taken for maintenance")
    #
    # def swinging_the_lead(self) -> None:
    #     raise RuntimeError("CRITICAL ERROR: Robot cannot waste our money (we hope so)")


def manage_orders(workers):
    for worker in workers:
        worker.process_order()


def manage_meetings(humans):
    for human in humans:
        human.attend_meeting()


def manage_rest(humans):
    for human in humans:
        human.get_rest()


def manage_lazy(humans):
    for human in humans:
        human.swinging_the_lead()


def manage_warehouse(workers, humans):
    print("\n--- Warehouse Shift Started ---")
    manage_orders(workers)
    manage_meetings(humans)
    manage_rest(humans)
    manage_lazy(humans)