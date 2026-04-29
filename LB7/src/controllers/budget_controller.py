from datetime import datetime, timezone as tz
from typing import List

from sqlalchemy.orm import Session

from LB7.src.clients.repositories import BudgetRepository, AccountRepository, TransactionRepository
from LB7.src.models.DTO.budget import BudgetCreateDTO, BudgetOutDTO, BudgetStatusDTO
from LB7.src.models.entities import Budget
from LB7.src.models.enums import TransactionType, CategoryType
from LB7.src.shared.exceptions import NotFoundException, ForbiddenException


class BudgetController:
    def __init__(self, db: Session):
        self._budget_repo = BudgetRepository(db)
        self._acc_repo = AccountRepository(db)
        self._tx_repo = TransactionRepository(db)

    def create_or_update_budget(self, user_id: int, dto: BudgetCreateDTO) -> BudgetOutDTO:
        existing = self._budget_repo.get_by_user_category_period(
            user_id, dto.category, dto.year, dto.month
        )
        if existing:
            existing.monthly_limit = dto.monthly_limit
            updated = self._budget_repo.update(existing)
            return BudgetOutDTO.model_validate(updated)

        budget = Budget(
            category=dto.category,
            monthly_limit=dto.monthly_limit,
            year=dto.year,
            month=dto.month,
            user_id=user_id,
        )
        created = self._budget_repo.create(budget)
        return BudgetOutDTO.model_validate(created)

    def get_budgets(self, user_id: int, year: int, month: int) -> List[BudgetStatusDTO]:
        budgets = self._budget_repo.get_by_user_and_period(user_id, year, month)
        result = []
        for budget in budgets:
            spent = self._calculate_spent(user_id, budget.category, year, month)
            remaining = budget.monthly_limit - spent
            result.append(
                BudgetStatusDTO(
                    category=budget.category,
                    monthly_limit=budget.monthly_limit,
                    spent=round(spent, 2),
                    remaining=round(remaining, 2),
                    exceeded=spent > budget.monthly_limit,
                    year=year,
                    month=month,
                )
            )
        return result

    def delete_budget(self, user_id: int, budget_id: int) -> bool:
        budget = self._budget_repo.get_by_id(budget_id)
        if not budget:
            raise NotFoundException(f"Limit with id={budget_id} not found")
        if budget.user_id != user_id:
            raise ForbiddenException("No access to this limit")
        return self._budget_repo.delete(budget_id)

    def _calculate_spent(
            self, user_id: int, category: CategoryType, year: int, month: int
    ) -> float:
        accounts = self._acc_repo.get_by_user(user_id)
        account_ids = [a.id for a in accounts]
        if not account_ids:
            return 0.0

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
        return sum(t.amount for t in expenses)
