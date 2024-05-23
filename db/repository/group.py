from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from core.config import settings
from db.models import Group
from schemas.schemas import GroupCreate, GroupPatch, GroupUpdate


def create_new_group(db: Session, group: GroupCreate):
    """Create new group."""
    group = Group(**group.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_all_groups(db: Session):
    """Get groups list."""
    return db.query(Group).order_by(desc(Group.created_at))


def get_group(id: int, db: Session):
    """Get group by id or raise Exception."""
    group = db.query(Group).filter(Group.id == id).first()
    if not group:
        raise HTTPException(
            detail=settings.OBJECT_NOT_FOUND_MSG.format(
                object='Group', id=id
            ),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return group


def remove_group(id: int, db: Session):
    """Delete group."""
    group_in_db = db.query(Group).filter(Group.id == id)
    if not group_in_db.first():
        raise HTTPException(
            detail=settings.OBJECT_NOT_FOUND_MSG.format(
                object='Group', id=id
            ),
            status_code=status.HTTP_404_NOT_FOUND
        )
    group_in_db.delete()
    db.commit()
    return {
        'message': settings.OBJECT_DELETED_MSG.format(
            object='Group', id=id
        )
    }


def update_group_info(
    id: int, db: Session, group: Union[GroupPatch, GroupUpdate],
):
    """Full or partial update existing group."""
    group_in_db = get_group(id, db)
    if isinstance(group, GroupPatch):
        for attr, value in group.model_dump(exclude_unset=True).items():
            group_in_db.__setattr__(attr, value)
    elif isinstance(group, GroupUpdate):
        for attr, value in group.model_dump().items():
            group_in_db.__setattr__(attr, value)
    db.commit()
    return group_in_db
