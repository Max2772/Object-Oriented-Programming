import enum

class AccountType(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    SAVINGS = "savings"


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"