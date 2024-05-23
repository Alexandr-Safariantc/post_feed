from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqladmin import Admin

from core.config import settings
from db.models import Base
from db.session import engine
from internal.admin import GroupAdmin, PostAdmin, UserAdmin
from routes.base import api_router


def create_tables():
    """Create db tables if not exist."""
    Base.metadata.create_all(bind=engine)


def include_router(app):
    """Import routes."""
    app.include_router(api_router)


def start_app():
    """Start Fast API app, create admin site."""
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION
    )
    admin = Admin(app, engine)
    admin.add_view(GroupAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(UserAdmin)
    create_tables()
    add_pagination(app)
    include_router(app)
    return app


app = start_app()
