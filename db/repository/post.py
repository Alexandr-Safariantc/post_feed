from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from core.config import settings
from db.models import Post
from db.repository.group import get_group
from db.repository.user import get_user
from schemas.schemas import PostCreate, PostPatch, PostUpdate


def create_new_post(author_id: int, db: Session, post: PostCreate):
    """Create new post."""
    get_group(post.group_id, db)
    created_post = Post(**post.model_dump(), author_id=author_id)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


def get_all_posts(db: Session):
    """Get posts list."""
    return db.query(Post).order_by(desc(Post.pub_date))


def get_post(id: int, db: Session):
    """Get post detail by id or raise Exception."""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            detail=settings.OBJECT_NOT_FOUND_MSG.format(
                object='Post', id=id
            ),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return post


def remove_post(id: int, db: Session, user_id: int):
    """Delete post."""
    post_in_db = db.query(Post).filter(Post.id == id)
    if not post_in_db.first():
        raise HTTPException(
            detail=settings.OBJECT_NOT_FOUND_MSG.format(
                object='Post', id=id
            ),
            status_code=status.HTTP_404_NOT_FOUND
        )
    if (post_in_db.first().author_id != user_id
            and get_user(db, user_id).is_superuser is False):
        raise HTTPException(
            detail=settings.ONLY_POST_AUTHOR_ACTION_MSG.format(
                action='delete'
            ),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    post_in_db.delete()
    db.commit()
    return {
        'message': settings.OBJECT_DELETED_MSG.format(
            object='Post', id=id
        )
    }


def update_post_info(
    id: int,
    post: Union[PostUpdate, PostPatch],
    db: Session,
    user_id: int
):
    """Full or partial update existing post."""
    post_in_db = get_post(id, db)
    if post_in_db.author_id != user_id:
        raise HTTPException(
            detail=settings.ONLY_POST_AUTHOR_ACTION_MSG.format(
                action='edit'
            ),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    if post.group_id is not None:
        get_group(post.group_id, db)
    if isinstance(post, PostPatch):
        for attr, value in post.model_dump(exclude_unset=True).items():
            post_in_db.__setattr__(attr, value)
    elif isinstance(post, PostUpdate):
        for attr, value in post.model_dump().items():
            post_in_db.__setattr__(attr, value)
    db.commit()
    return post_in_db
