from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field

from core.config import settings


class GroupCreate(BaseModel):
    """Serialize data for Group instance creation."""

    description: str
    slug: str = Field(pattern=settings.GROUP_SLUG_PATTERN)
    title: str


class GroupPatch(BaseModel):
    """Serialize data for Group instance partial updating."""

    description: Optional[int] = None
    slug: Optional[datetime] = None
    title: Optional[str] = None


class GroupUpdate(GroupCreate):
    """Serialize data for Group instance updating."""
    pass


class GroupShow(GroupCreate):
    """Serialize data for safety methods with Group instance."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    """Serialize data for Post instance creation."""

    group_id: int
    pub_date: Optional[datetime] = datetime.now()
    text: str
    title: str = Field(max_length=settings.POST_TITLE_MAX_LENGTH)


class PostPatch(BaseModel):
    """Serialize data for Post instance partial updating."""

    group_id: Optional[int] = None
    pub_date: Optional[datetime] = None
    text: Optional[str] = None
    title: Optional[str] = None


class PostUpdate(PostCreate):
    """Serialize data for Post instance updating."""
    pass


class PostShow(BaseModel):
    """Serialize data for safety methods with Post instance."""

    id: int
    author_id: int
    group_id: int
    pub_date: datetime
    text: str
    title: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Serialize data for getting token."""

    access_token: str
    token_type: str


class UserCreate(BaseModel):
    """Serialize data for User instance creation."""

    email: EmailStr
    first_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )
    last_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )
    password: str = Field(
        max_length=settings.PASSWORD_MAX_LENGTH,
        min_length=settings.PASSWORD_MIN_LENGTH,
        pattern=settings.PASSWORD_PATTERN
    )
    username: str = Field(
        max_length=settings.USERNAME_MAX_LENGTH,
        min_length=settings.USERNAME_MIN_LENGTH,
        pattern=settings.USERNAME_PATTERN
    )


class UserPatch(BaseModel):
    """Serialize data for User instance partial updating."""

    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )
    last_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )


class UserUpdate(BaseModel):
    """Serialize data for User instance updating."""

    email: EmailStr
    first_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )
    last_name: Optional[str] = Field(
        None, max_length=settings.FIRST_LAST_NAMES_MAX_LENGTH
    )


class UserShow(BaseModel):
    """Serialize data for safety methods with User instance."""

    id: int
    date_joined: datetime
    email: EmailStr
    first_name: Union[str, None]
    last_name: Union[str, None]
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
