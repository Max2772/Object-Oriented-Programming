from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from LB7.src.clients.repositories import (
    TransactionRepository,
    AccountRepository,
    BudgetRepository,
)
from LB7.src.models.DTO.transactions import TransactionCreateDTO, TransactionOutDTO
from LB7.src.models.entities import Transaction
from LB7.src.models.enums import TransactionType, CategoryType
from LB7.src.shared.exceptions import (
    NotFoundException,
    ForbiddenException,
)


class TransactionController:

    def __init__(self, db: Session):
        self._tx_repo = TransactionRepository(db)
        self._acc_repo = AccountRepository(db)
        self._budget_repo = BudgetRepository(db)

    def create_transaction(
            self, user_id: int, dto: TransactionCreateDTO
    ) -> dict:
        account = self._acc_repo.get_by_id(dto.account_id)
        if not account:
            raise NotFoundException(f"Account with id={dto.account_id} not found")
        if account.user_id != user_id:
            raise ForbiddenException("No access to this account")

        if dto.transaction_type == TransactionType.INCOME:
            account.balance += dto.amount
        else:
            account.balance -= dto.amount

        self._acc_repo.update(account)

        transaction = Transaction(
            amount=dto.amount,
            transaction_type=dto.transaction_type,
            category=dto.category,
            description=dto.description,
            account_id=dto.account_id,
        )
        created = self._tx_repo.create(transaction)
        result = {
            "transaction": TransactionOutDTO.model_validate(created),
            "warning": None,
        }

        if dto.transaction_type == TransactionType.EXPENSE:
            warning = self._check_budget_limit(user_id, dto.category, created.created_at)
            if warning:
                result["warning"] = warning

        return result

    def get_transactions(
            self,
            user_id: int,
            account_id: Optional[int] = None,
            date_from: Optional[datetime] = None,
            date_to: Optional[datetime] = None,
            category: Optional[CategoryType] = None,
            transaction_type: Optional[TransactionType] = None,
    ) -> List[TransactionOutDTO]:
        accounts = self._acc_repo.get_by_user(user_id)
        if account_id:
            account_ids = [a.id for a in accounts if a.id == account_id]
            if not account_ids:
                raise ForbiddenException("No access to this account")
        else:
            account_ids = [a.id for a in accounts]

        if not account_ids:
            return []

        transactions = self._tx_repo.get_by_user_and_period(
            account_ids=account_ids,
            date_from=date_from,
            date_to=date_to,
            category=category,
            transaction_type=transaction_type,
        )
        return [TransactionOutDTO.model_validate(t) for t in transactions]

    def delete_transaction(self, user_id: int, transaction_id: int) -> bool:
        transaction = self._tx_repo.get_by_id(transaction_id)
        if not transaction:
            raise NotFoundException(f"Transaction with id={transaction_id} not found")

        account = self._acc_repo.get_by_id(transaction.account_id)
        if not account or account.user_id != user_id:
            raise ForbiddenException("No access to this transaction")

        if transaction.transaction_type == TransactionType.INCOME:
            account.balance -= transaction.amount
        else:
            account.balance += transaction.amount
        self._acc_repo.update(account)

        return self._tx_repo.delete(transaction_id)

    def _check_budget_limit(
            self, user_id: int, category: CategoryType, tx_date: datetime
    ) -> Optional[str]:
        year = tx_date.year
        month = tx_date.month

        budget = self._budget_repo.get_by_user_category_period(
            user_id, category, year, month
        )
        if not budget:
            return None

        accounts = self._acc_repo.get_by_user(user_id)
        account_ids = [a.id for a in accounts]
        if not account_ids:
            return None

        from datetime import timezone as tz
        month_start = datetime(year, month, 1, tzinfo=tz.utc)
        if month == 12:
            month_end = datetime(year + 1, 1, 1, tzinfo=tz.utc)
        else:
            month_end = datetime(year, month + 1, 1, tzinfo=tz.utc)

        expenses = self._tx_repo.get_by_user_and_period(
            account_ids=account_ids,
            date_from=month_start,
            date_to=month_end,
            category=category,
            transaction_type=TransactionType.EXPENSE,
        )
        total_spent = sum(t.amount for t in expenses)

        if total_spent > budget.monthly_limit:
            return (
                f"Warning! Budget limit for category '{category.value}' exceeded: "
                f"limit {budget.monthly_limit:.2f}, spent {total_spent:.2f}"
            )
        return None
