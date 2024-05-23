import datetime as dt

from jose import jwt
from typing import Optional

from core.config import settings


def create_access_token(
    data: dict, expires_time: Optional[dt.timedelta] = None
):
    """Create JWT for user authentication."""
    to_encode = data.copy()
    if expires_time:
        expire = dt.datetime.now() + expires_time
    else:
        expire = dt.datetime.now() + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ENCODE_ALGORITHM
    )
