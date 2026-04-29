from abc import ABC, abstractmethod
from typing import List, Optional, Type, TypeVar, Generic

from sqlalchemy import and_
from sqlalchemy.orm import Session

from LB7.src.models.entities import Base, Account, User, Budget, Transaction

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        ...

    @abstractmethod
    def get_all(self, **filters) -> List[T]:
        ...

    @abstractmethod
    def create(self, entity: T) -> T:
        ...

    @abstractmethod
    def update(self, entity: T) -> T:
        ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        ...


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, db: Session, model: Type[T]):
        self._db = db
        self._model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self._db.query(self._model).filter(self._model.id == entity_id).first()

    def get_all(self, **filters) -> List[T]:
        query = self._db.query(self._model)
        for key, value in filters.items():
            if value is not None and hasattr(self._model, key):
                query = query.filter(getattr(self._model, key) == value)
        return query.all()

    def create(self, entity: T) -> T:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self._db.delete(entity)
            self._db.commit()
            return True
        return False


class AccountRepository(SQLAlchemyRepository[Account]):

    def __init__(self, db: Session):
        super().__init__(db, Account)

    def get_by_user(self, user_id: int) -> List[Account]:
        return self._db.query(Account).filter(Account.user_id == user_id).all()


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        return self._db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()


class TransactionRepository(SQLAlchemyRepository[Transaction]):

    def __init__(self, db: Session):
        super().__init__(db, Transaction)

    def get_by_account(self, account_id: int) -> List[Transaction]:
        return self._db.query(Transaction).filter(
            Transaction.account_id == account_id
        ).all()

    def get_by_user_and_period(
            self,
            account_ids: List[int],
            date_from=None,
            date_to=None,
            category=None,
            transaction_type=None,
    ) -> List[Transaction]:
        query = self._db.query(Transaction).filter(
            Transaction.account_id.in_(account_ids)
        )
        if date_from:
            query = query.filter(Transaction.created_at >= date_from)
        if date_to:
            query = query.filter(Transaction.created_at <= date_to)
        if category:
            query = query.filter(Transaction.category == category)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        return query.order_by(Transaction.created_at.desc()).all()


class BudgetRepository(SQLAlchemyRepository[Budget]):

    def __init__(self, db: Session):
        super().__init__(db, Budget)

    def get_by_user(self, user_id: int) -> List[Budget]:
        return self._db.query(Budget).filter(Budget.user_id == user_id).all()

    def get_by_user_and_period(
            self, user_id: int, year: int, month: int
    ) -> List[Budget]:
        return (
            self._db.query(Budget)
            .filter(
                and_(
                    Budget.user_id == user_id,
                    Budget.year == year,
                    Budget.month == month,
                )
            )
            .all()
        )

    def get_by_user_category_period(
            self, user_id: int, category, year: int, month: int
    ) -> Optional[Budget]:
        return (
            self._db.query(Budget)
            .filter(
                and_(
                    Budget.user_id == user_id,
                    Budget.category == category,
                    Budget.year == year,
                    Budget.month == month,
                )
            )
            .first()
        )
