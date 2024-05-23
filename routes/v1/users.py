from fastapi import APIRouter, Depends, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from core.pagination import UserPaginator
from db.models import User
from db.repository.login import check_is_superuser, get_current_user
from db.repository.user import (
    create_new_user, get_all_users, get_user, update_user_info
)
from db.session import get_db
from schemas.schemas import UserCreate, UserPatch, UserShow, UserUpdate


router = APIRouter()


@router.get('/me', response_model=UserShow)
def about_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user info."""
    return get_user(id=current_user.id, db=db)


@router.put('/me', response_model=UserShow)
def update_user(
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user_info(
        current_user_id=current_user.id, db=db, user=user
    )


@router.patch('/me', response_model=UserShow)
def partial_update_user(
    user: UserPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user_info(
        current_user_id=current_user.id, db=db, user=user
    )


@router.get('/', response_model=UserPaginator[UserShow])
def get_users_list(
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return paginate(get_all_users(db=db))


@router.post('/', response_model=UserShow, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user=user, db=db)


@router.get('/{id}', response_model=UserShow)
def get_user_detail(
    id: int,
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return get_user(id=id, db=db)
