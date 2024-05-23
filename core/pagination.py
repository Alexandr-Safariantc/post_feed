from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import (
    CustomizedPage, UseName, UseParamsFields
)

from core.config import settings


T = TypeVar('T')

GroupPaginator = CustomizedPage[
    Page[T],
    UseName('GroupPaginator'),
    UseParamsFields(size=Query(
        settings.PAGE_SIZE_GROUP,
        ge=settings.PAGE_SIZE_MIN,
        lt=settings.PAGE_SIZE_MAX,
        description=settings.PAGE_SIZE_NAME)
    ),
]

PostPaginator = CustomizedPage[
    Page[T],
    UseName('PostPaginator'),
    UseParamsFields(size=Query(
        settings.PAGE_SIZE_POST,
        ge=settings.PAGE_SIZE_MIN,
        lt=settings.PAGE_SIZE_MAX,
        description=settings.PAGE_SIZE_NAME)
    ),
]

UserPaginator = CustomizedPage[
    Page[T],
    UseName('UserPaginator'),
    UseParamsFields(size=Query(
        settings.PAGE_SIZE_USER,
        ge=settings.PAGE_SIZE_MIN,
        lt=settings.PAGE_SIZE_MAX,
        description=settings.PAGE_SIZE_NAME)
    ),
]
