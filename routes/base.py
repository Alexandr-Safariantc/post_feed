from fastapi import APIRouter

from routes.v1 import groups, login, posts, users


API_URL_PREFIX = '/api/v1'

api_router = APIRouter()
api_router.include_router(
    groups.router, prefix=API_URL_PREFIX + '/groups', tags=['groups']
)
api_router.include_router(
    login.router, prefix=API_URL_PREFIX + '/login', tags=['login']
)
api_router.include_router(
    posts.router, prefix=API_URL_PREFIX + '/posts', tags=['posts']
)
api_router.include_router(
    users.router, prefix=API_URL_PREFIX + '/users', tags=['users'],
)
