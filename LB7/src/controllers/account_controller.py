from typing import List
from sqlalchemy.orm import Session

from LB7.src.clients.repositories import AccountRepository
from LB7.src.models.entities import Account
from LB7.src.models.DTO.account import AccountCreateDTO, AccountUpdateDTO, AccountOutDTO
from LB7.src.shared.exceptions import NotFoundException, ForbiddenException


class AccountController:
    def __init__(self, db: Session):
        self._repo = AccountRepository(db)

    def create_account(self, user_id: int, dto: AccountCreateDTO) -> AccountOutDTO:
        account = Account(
            name=dto.name,
            account_type=dto.account_type,
            balance=dto.balance,
            user_id=user_id,
        )
        created = self._repo.create(account)
        return AccountOutDTO.model_validate(created)

    def get_accounts(self, user_id: int) -> List[AccountOutDTO]:
        accounts = self._repo.get_by_user(user_id)
        return [AccountOutDTO.model_validate(a) for a in accounts]

    def get_account(self, user_id: int, account_id: int) -> AccountOutDTO:
        account = self._get_owned_account(user_id, account_id)
        return AccountOutDTO.model_validate(account)

    def update_account(
        self, user_id: int, account_id: int, dto: AccountUpdateDTO
    ) -> AccountOutDTO:
        account = self._get_owned_account(user_id, account_id)
        if dto.name is not None:
            account.name = dto.name
        if dto.account_type is not None:
            account.account_type = dto.account_type
        updated = self._repo.update(account)
        return AccountOutDTO.model_validate(updated)

    def delete_account(self, user_id: int, account_id: int) -> bool:
        self._get_owned_account(user_id, account_id)
        return self._repo.delete(account_id)

    def _get_owned_account(self, user_id: int, account_id: int) -> Account:
        account = self._repo.get_by_id(account_id)
        if not account:
            raise NotFoundException(f"Account with id={account_id} not found")
        if account.user_id != user_id:
            raise ForbiddenException("No access to this account")
        return account
