from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from LB7.src.clients.database import get_db
from LB7.src.controllers.auth_controller import AuthController
from LB7.src.models.entities import User
from LB7.src.shared.exceptions import UnauthorizedException

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    auth = AuthController(db)
    try:
        return auth.get_current_user(token)
    except UnauthorizedException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
