from datetime import date, timedelta
from typing import List, Optional
from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id: str, name: str):
        self.__person_id = person_id
        self.__name = name

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def get_info(self) -> str:
        pass


class Publication(ABC):
    def __init__(self, publication_id: str, title: str):
        self.__publication_id = publication_id
        self.__title = title

    @property
    def publication_id(self) -> str:
        return self.__publication_id

    @property
    def title(self) -> str:
        return self.__title

    @abstractmethod
    def get_info(self) -> str:
        pass


class Author(Person):
    def __init__(self, author_id: str, name: str, birth_date: date, nationality: str):
        super().__init__(author_id, name)
        self.__birth_date = birth_date
        self.__nationality = nationality

    def get_info(self) -> str:
        return f"Автор: {self.name} ({self.__birth_date.year} г., {self.__nationality})"


class LibraryUser(Person):
    def __init__(self, member_id: str, name: str, address: str, phone: str, email: str):
        super().__init__(member_id, name)
        self.__address = address
        self.__phone = phone
        self.__email = email

    def get_max_loan_days(self) -> int:
        return 14

    def get_info(self) -> str:
        return f"Читатель: {self.name}, тел.: {self.__phone}"


class Student(LibraryUser):
    def get_max_loan_days(self) -> int:
        return 14

    def get_info(self) -> str:
        return f"Студент: {self.name} (макс. {self.get_max_loan_days()} дней)"


class Teacher(LibraryUser):
    def get_max_loan_days(self) -> int:
        return 30

    def get_info(self) -> str:
        return f"Преподаватель: {self.name} (макс. {self.get_max_loan_days()} дней)"


class Staff(Person):
    def __init__(self, staff_id: str, name: str, hire_date: date):
        super().__init__(staff_id, name)
        self.__hire_date = hire_date

    @property
    def hire_date(self) -> date:
        return self.__hire_date

    def get_info(self) -> str:
        return f"Работник: {self.name} (нанят с {self.__hire_date})"


class Librarian(Staff):
    def get_info(self) -> str:
        return f"Библиотекарь: {self.name} (нанят с {self.hire_date} г.)"


class Book(Publication):
    def __init__(self, book_id: str, title: str, isbn: str, publication_year: int,
                 authors: List[Author], publisher: 'Publisher'):
        super().__init__(book_id, title)
        self.__isbn = isbn
        self.__publication_year = publication_year
        self.__authors = authors[:]
        self.__publisher = publisher

    def get_info(self) -> str:
        author_names = [a.name for a in self.__authors]
        return (f"Книга: «{self.title}» (ISBN: {self.__isbn}, {self.__publication_year} г.)"
                f" | Авторы: {', '.join(author_names)}"
                f" | Издательство: {self.__publisher.name}")


class BookCopy:
    def __init__(self, copy_id: str, book: Book, status: str = "available"):
        self.__copy_id = copy_id
        self.__book = book
        self.__status = status

    @property
    def copy_id(self) -> str:
        return self.__copy_id

    @property
    def book(self) -> Book:
        return self.__book

    def borrow(self) -> bool:
        if self.__status == "available":
            self.__status = "borrowed"
            return True
        return False

    def return_copy(self) -> None:
        self.__status = "available"

    def get_info(self) -> str:
        return f"Копия книги: {self.book.get_info()}\n\t Статус: {self.__status}"


class Loan:
    def __init__(self, loan_id: str, member: LibraryUser, copy: BookCopy):
        self.__loan_id = loan_id
        self.__member = member
        self.__copy = copy
        self.__loan_date = date.today()
        self.__due_date = self.__loan_date + timedelta(days=member.get_max_loan_days())
        self.__returned_date: Optional[date] = None

    def return_loan(self) -> None:
        self.__returned_date = date.today()

    def is_overdue(self) -> bool:
        return self.__returned_date is None and date.today() > self.__due_date

    def get_info(self) -> str:
        status = "возвращён" if self.__returned_date else "на руках"
        return f"Заём {self.__loan_id} | {self.__member.name} | до {self.__due_date} | {status}"


class Library:
    def __init__(self, library_id: str, name: str, address: str):
        self.__library_id = library_id
        self.__name = name
        self.__address = address
        self.__book_copies: List[BookCopy] = []
        self.__loans: List[Loan] = []
        self.__reservations: List[Reservation] = []
        self.__staff: List[Librarian] = []

    def add_copy(self, copy: BookCopy):
        self.__book_copies.append(copy)

    def add_staff(self, librarian: Librarian):
        self.__staff.append(librarian)

    def issue_loan(self, member: LibraryUser, copy: BookCopy) -> Loan:
        if copy.borrow():
            loan = Loan(f"L{len(self.__loans) + 1:04d}", member, copy)
            self.__loans.append(loan)
            return loan
        raise ValueError("Копия недоступна")

    def get_info(self) -> str:
        return f"Библиотека: {self.__name}, {self.__address}"


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
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name


class Reservation:
    def __init__(self, reservation_id: str, member: LibraryUser, copy: BookCopy, cancelled: bool = False):
        self.__reservation_id = reservation_id
        self.__member = member
        self.__copy = copy
        self.__cancelled = cancelled

    def cancel(self) -> None:
        self.__cancelled = True
        print(f"Резервирование {self.__reservation_id} отменено.")


class Fine:
    def __init__(self, fine_id: str, amount: float):
        self.__fine_id = fine_id
        self.__amount = amount
        self.__paid = False

    def pay(self) -> None:
        self.__paid = True
        print(f"Штраф {self.__fine_id} на сумму {self.__amount} BYN оплачен.")


if __name__ == "__main__":
    print("Демонстрация классов (наследование + композиция + полиморфизм):\n")

    publisher = Publisher("P001", "Беларусь", "Минск")
    author = Author("A001", "Лев Толстой", date(1828, 9, 9), "Россия")
    book = Book("B001", "Война и мир", "978-5-04-123456-7", 1869, [author], publisher)
    library = Library("LIB01", "Национальная библиотека Беларуси", "пр. Независимости 116")
    copy1 = BookCopy("C001", book)
    student = Student("M001", "Анна Смирнова", "Гикало 9", "+375-29-123-45-67", "anna@example.com")
    teacher = Teacher("M002", "Иван Петров", "Минск", "+375-29-987-65-43", "ivan@hotmail.com")
    librarian = Librarian("L001", "Мария Иванова", date(2019, 6, 1))


    print("Создание объектов:")
    print(" -", publisher.get_info())
    print(" -", author.get_info())
    print(" -", book.get_info())
    print(" -", library.get_info())
    print(" -", copy1.get_info())
    print(" -", student.get_info())
    print(" -", teacher.get_info())
    print(" -", librarian.get_info(), '\n')

    library.add_copy(copy1)
    library.add_staff(librarian)

    print("Полиморфизм LibraryUser:")
    for user in [student, teacher]:
        print(f"\t{user.get_info()} - может взять книгу на {user.get_max_loan_days()} дней")

    print("\nСценарий выдачи:")
    loan1 = library.issue_loan(student, copy1)
    print(loan1.get_info())

    print("\nЧерез 20 дней...")
    loan1.return_loan()
    copy1.return_copy()
    print(loan1.get_info())

    fine = Fine("F001", 25.0)
    fine.pay()