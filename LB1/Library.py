from datetime import date, timedelta
from typing import Optional


class Author:
    def __init__(self, author_id: str, name: str, birth_date: date, nationality: str):
        self.__author_id = author_id
        self.__name = name
        self.__birth_date = birth_date
        self.__nationality = nationality

    @property
    def author_id(self) -> str:
        return self.__author_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Автор: {self.__name} ({self.__birth_date.year} г., {self.__nationality})"


class Publisher:
    def __init__(self, publisher_id: str, name: str, location: str):
        self.__publisher_id = publisher_id
        self.__name = name
        self.__location = location

    @property
    def publisher_id(self) -> str:
        return self.__publisher_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Издательство: {self.__name}, {self.__location}"


class Genre:
    def __init__(self, genre_id: str, name: str):
        self.__genre_id = genre_id
        self.__name = name

    @property
    def genre_id(self) -> str:
        return self.__genre_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Жанр: {self.__name}"


class Book:
    def __init__(self, book_id: str, title: str, isbn: str, publication_year: int):
        self.__book_id = book_id
        self.__title = title
        self.__isbn = isbn
        self.__publication_year = publication_year

    @property
    def book_id(self) -> str:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    def get_info(self) -> str:
        return f"Книга: «{self.__title}» (ISBN: {self.__isbn}, {self.__publication_year} г.)"


class BookCopy:
    def __init__(self, copy_id: str, status: str = "available"):
        self.__copy_id = copy_id
        self.__status = status

    @property
    def copy_id(self) -> str:
        return self.__copy_id

    @property
    def status(self) -> str:
        return self.__status

    def borrow(self) -> bool:
        if self.__status == "available":
            self.__status = "borrowed"
            return True
        return False

    def return_copy(self) -> None:
        self.__status = "available"


class LibraryMember:
    def __init__(self, member_id: str, name: str, address: str, phone: str, email: str):
        self.__member_id = member_id
        self.__name = name
        self.__address = address
        self.__phone = phone
        self.__email = email

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Читатель: {self.__name}, {self.__phone}"


class Librarian:
    def __init__(self, librarian_id: str, name: str, phone: str):
        self.__librarian_id = librarian_id
        self.__name = name
        self.__phone = phone

    @property
    def librarian_id(self) -> str:
        return self.__librarian_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Библиотекарь: {self.__name}, {self.__phone}"


class Library:
    def __init__(self, library_id: str, name: str, address: str):
        self.__library_id = library_id
        self.__name = name
        self.__address = address

    @property
    def library_id(self) -> str:
        return self.__library_id

    @property
    def name(self) -> str:
        return self.__name

    def get_info(self) -> str:
        return f"Библиотека: {self.__name}, {self.__address}"


class Loan:
    def __init__(self, loan_id: str, loan_date: date, due_date: date):
        self.__loan_id = loan_id
        self.__loan_date = loan_date
        self.__due_date = due_date
        self.__returned_date: Optional[date] = None

    @property
    def loan_id(self) -> str:
        return self.__loan_id

    def return_loan(self) -> None:
        self.__returned_date = date.today()

    def is_overdue(self) -> bool:
        return self.__returned_date is None and date.today() > self.__due_date

    def get_info(self) -> str:
        status = "возвращен" if self.__returned_date else "на руках"
        return f"Заём №{self.__loan_id} — статус: {status}"


class Reservation:
    def __init__(self, reservation_id: str, reservation_date: date, cancelled: bool = False):
        self.__reservation_id = reservation_id
        self.__reservation_date = reservation_date
        self.__cancelled = cancelled

    def cancel(self) -> None:
        self.__cancelled = True
        print(f"Резервирование №{self.__reservation_id} отменено.")


class Fine:
    def __init__(self, fine_id: str, amount: float):
        self.__fine_id = fine_id
        self.__amount = amount
        self.__paid = False

    def pay(self) -> None:
        self.__paid = True
        print(f"Штраф №{self.__fine_id} на сумму {self.__amount} BYN оплачен.")


if __name__ == "__main__":
    print("Демонстрация независимых классов:\n")

    author = Author("A001", "Лев Толстой", date(1828, 9, 9), "Россия")
    book = Book("B001", "Война и мир", "978-5-04-123456-7", 1869)
    book_copy = BookCopy("C001")
    member = LibraryMember("M001", "Анна Смирнова", "Гикало 9", "+375-29-123-45-67", "anna@example.com")
    librarian = Librarian("L001", "Мария Иванова", "+375-29-345-67-89")
    library = Library("LIB01", "Нацыянальная бібліятэка Беларусі", "пр. Независимости 116")

    print("Создание объектов:")
    print(" -", author.get_info())
    print(" -", book.get_info())
    print(" -", member.get_info())
    print(" -", librarian.get_info())

    print("\nДемонстрационный сценарий:")
    print("Библиотекарь выдаёт книгу читателю...")

    loan = Loan("L001", date.today(), date.today() + timedelta(days=14))
    print(loan.get_info())

    if book_copy.borrow():
        print("Экземпляр книги выдан.")

    print("\nЧерез 20 дней...")
    print("Книга просрочена.")

    loan.return_loan()
    book_copy.return_copy()
    print(loan.get_info())

    fine = Fine("F001", 25.0)
    fine.pay()

    print("\nЧитатель резервирует другую книгу:")
    reservation = Reservation("R001", date.today())
    reservation.cancel()
