from collections import defaultdict
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from LB7.src.clients.repositories import TransactionRepository, AccountRepository
from LB7.src.models.DTO.analytics import AnalyticsSummaryDTO, CategorySummaryDTO
from LB7.src.models.entities import TransactionType, CategoryType


class AnalyticsController:
    def __init__(self, db: Session):
        self._tx_repo = TransactionRepository(db)
        self._acc_repo = AccountRepository(db)

    def get_summary(
            self,
            user_id: int,
            date_from: datetime,
            date_to: datetime,
            category: Optional[CategoryType] = None,
    ) -> AnalyticsSummaryDTO:
        accounts = self._acc_repo.get_by_user(user_id)
        account_ids = [a.id for a in accounts]

        if not account_ids:
            return AnalyticsSummaryDTO(
                date_from=date_from.isoformat(),
                date_to=date_to.isoformat(),
                total_income=0.0,
                total_expense=0.0,
                balance_change=0.0,
                by_category=[],
            )

        transactions = self._tx_repo.get_by_user_and_period(
            account_ids=account_ids,
            date_from=date_from,
            date_to=date_to,
            category=category,
        )

        total_income = 0.0
        total_expense = 0.0
        cat_totals: dict = defaultdict(lambda: {"total": 0.0, "count": 0})

        for tx in transactions:
            if tx.transaction_type == TransactionType.INCOME:
                total_income += tx.amount
            else:
                total_expense += tx.amount

            cat_totals[tx.category]["total"] += tx.amount
            cat_totals[tx.category]["count"] += 1

        by_category = [
            CategorySummaryDTO(
                category=cat,
                total=round(data["total"], 2),
                count=data["count"],
            )
            for cat, data in sorted(cat_totals.items(), key=lambda x: x[1]["total"], reverse=True)
        ]

        return AnalyticsSummaryDTO(
            date_from=date_from.isoformat(),
            date_to=date_to.isoformat(),
            total_income=round(total_income, 2),
            total_expense=round(total_expense, 2),
            balance_change=round(total_income - total_expense, 2),
            by_category=by_category,
        )
