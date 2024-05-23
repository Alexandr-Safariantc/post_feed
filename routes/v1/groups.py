from fastapi import APIRouter, Depends, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from core.pagination import GroupPaginator
from db.models import User
from db.repository.group import (
    create_new_group,
    get_all_groups,
    get_group,
    remove_group,
    update_group_info,
)
from db.repository.login import check_is_superuser
from db.session import get_db
from schemas.schemas import GroupCreate, GroupShow, GroupUpdate


router = APIRouter()


@router.get('/', response_model=GroupPaginator[GroupShow])
def get_groups_list(db: Session = Depends(get_db)):
    return paginate(get_all_groups(db=db))


@router.post(
    '/', response_model=GroupShow, status_code=status.HTTP_201_CREATED
)
def create_group(
    group: GroupCreate,
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return create_new_group(group=group, db=db)


@router.get('/{id}', response_model=GroupShow)
def get_group_detail(id: int, db: Session = Depends(get_db)):
    return get_group(id=id, db=db)


@router.put('/{id}', response_model=GroupShow)
def update_group(
    id: int,
    group: GroupUpdate,
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return update_group_info(id=id, group=group, db=db)


@router.patch('/{id}', response_model=GroupShow)
def partial_update_group(
    id: int,
    group: GroupUpdate,
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return update_group_info(id=id, group=group, db=db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    id: int,
    current_user: User = Depends(check_is_superuser),
    db: Session = Depends(get_db),
):
    return remove_group(id=id, db=db)
