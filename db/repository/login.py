from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from db.repository.user import get_user
from db.session import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def authenticate_user(username: str, password: str, db: Session):
    """Authenticate current user with request credentials."""
    user = get_user(username=username, db=db)
    if not Hasher.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=settings.INVALID_CREDENTIALS_MSG
        )
    return user


def check_is_superuser(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Raise exception if user is not superuser."""
    user = get_current_user(token=token, db=db)
    if user.is_superuser:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=settings.SUPERUSER_RESOURCE_MSG
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Get request User instance."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=settings.INVALID_CREDENTIALS_MSG
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ENCODE_ALGORITHM]
        )
        username: str = payload.get('username')
        password: str = payload.get('password')
        if username is None or password is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return get_user(username=username, db=db)
