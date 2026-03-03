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


def manage_warehouse(staff: list):
    print("\n--- Warehouse Shift Started ---")
    for member in staff:
        if isinstance(member, Worker):
            member.process_order()

        if isinstance(member, MeetingParticipant):
            member.attend_meeting()

        if isinstance(member, Restable):
            member.get_rest()

        if isinstance(member, LazyParticipant):
            member.swinging_the_lead()