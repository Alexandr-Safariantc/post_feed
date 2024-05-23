from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from db.models import User
from schemas.schemas import UserCreate, UserPatch, UserUpdate


def create_new_user(db: Session, user: UserCreate):
    """Create new user."""
    user_data = user.model_dump()
    user_data.update({'password': Hasher.get_hashed_password(user.password)})
    created_user = User(**user_data)
    db.add(created_user)
    db.commit()
    return created_user


def get_all_users(db: Session):
    """Get users list."""
    return db.query(User).order_by(desc(User.date_joined))


def get_user(db: Session, id: int = None, username: str = None):
    """Get user from db by id or username or raise Exception."""
    if id is not None:
        user = db.query(User).filter(User.id == id).first()
    elif username is not None:
        user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            detail=settings.OBJECT_NOT_FOUND_MSG.format(
                object='User', id=id
            ),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user


def update_user_info(
    current_user_id: int,
    db: Session,
    user: Union[UserPatch, UserUpdate],
):
    """Full or partial update existing user."""
    user_in_db = get_user(id=current_user_id, db=db)
    if isinstance(user, UserPatch):
        for attr, value in user.model_dump(exclude_unset=True).items():
            user_in_db.__setattr__(attr, value)
    elif isinstance(user, UserUpdate):
        for attr, value in user.model_dump().items():
            user_in_db.__setattr__(attr, value)
    db.commit()
    return user_in_db
