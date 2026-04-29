from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from LB7.src.clients.repositories import UserRepository
from LB7.src.models.DTO.auth import UserRegisterDTO, UserLoginDTO, TokenDTO, UserOutDTO
from LB7.src.models.entities import User
from LB7.src.shared.config import settings
from LB7.src.shared.exceptions import ConflictException, UnauthorizedException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthController:
    def __init__(self, db: Session):
        self._repo = UserRepository(db)

    def register(self, dto: UserRegisterDTO) -> UserOutDTO:
        if self._repo.get_by_username(dto.username):
            raise ConflictException(f"User «{dto.username}» already exists")
        if self._repo.get_by_email(dto.email):
            raise ConflictException(f"Email «{dto.email}» is already registered")

        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=self._hash_password(dto.password),
        )
        created = self._repo.create(user)
        return UserOutDTO.model_validate(created)

    def login(self, dto: UserLoginDTO) -> TokenDTO:
        user = self._repo.get_by_username(dto.username)
        if not user or not self._verify_password(dto.password, user.hashed_password):
            raise UnauthorizedException("Incorrect username or password")

        token = self._create_access_token({"sub": str(user.id)})
        return TokenDTO(access_token=token)

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise UnauthorizedException("Invalid token")
        except JWTError:
            raise UnauthorizedException("Invalid or expired token")

        user = self._repo.get_by_id(int(user_id))
        if user is None:
            raise UnauthorizedException("User not found")
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt_context.hash(password)

    @staticmethod
    def _verify_password(plain: str, hashed: str) -> bool:
        return bcrypt_context.verify(plain, hashed)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
                expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
