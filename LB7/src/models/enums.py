import enum


class AccountType(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    SAVINGS = "savings"


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CategoryType(str, enum.Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    LEISURE = "leisure"
    SALARY = "salary"
    HOUSING = "housing"
    HEALTH = "health"
    EDUCATION = "education"
    OTHER = "other"
