from fastapi import APIRouter, Depends, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from core.pagination import PostPaginator
from db.models import User
from db.repository.login import get_current_user
from db.repository.post import (
    create_new_post, get_all_posts, get_post, remove_post, update_post_info
)
from db.session import get_db
from schemas.schemas import PostCreate, PostPatch, PostShow, PostUpdate


router = APIRouter()


@router.get('/', response_model=PostPaginator[PostShow])
def get_posts_list(db: Session = Depends(get_db)):
    return paginate(get_all_posts(db=db))


@router.post('/', response_model=PostShow, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_post(author_id=current_user.id, db=db, post=post)


@router.get('/{id}', response_model=PostShow)
def get_post_detail(id: int, db: Session = Depends(get_db)):
    return get_post(id=id, db=db)


@router.put('/{id}', response_model=PostShow)
def update_post(
    id: int,
    post: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_post_info(
        id=id, post=post, db=db, user_id=current_user.id
    )


@router.patch('/{id}', response_model=PostShow)
def partial_update_post(
    id: int,
    post: PostPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_post_info(
        id=id, post=post, db=db, user_id=current_user.id
    )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_post(id=id, db=db, user_id=current_user.id)
