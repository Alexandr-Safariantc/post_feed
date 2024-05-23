import os
import sys
from datetime import datetime, timedelta

from jose import jwt
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any, Generator
import pytest

from core.config import settings
from core.hashing import Hasher
from db.models import Base, Group, Post, User
from db.session import get_db
from routes.base import API_URL_PREFIX, api_router


GROUP_DATA = {
    'description': 'Test_group',
    'slug': 'testgroup',
    'title': 'Test_group'
}
GROUP_UPDATED_DATA = {
    'description': 'New_test_group',
    'slug': 'newtestgroup',
    'title': 'New_test_group'
}
POST_DATA = {'text': 'Test post', 'title': 'test title'}
POST_UPDATED_DATA = {'text': 'New_test_post', 'title': 'new_test_title'}
SUPERUSER_DATA = {
    'email': 'test@superuser.com',
    'password': 'Superuser_Password_1',
    'username': 'test_superuser',
    'is_superuser': True,
}
USER_AUTHOR_DATA = {
    'email': 'test@author.com',
    'password': 'Author_Password_1',
    'username': 'test_author',
}
USER_NOT_AUTHOR_DATA = {
    'email': 'test@notauthor.com',
    'password': 'Not_Author_Password_1',
    'username': 'test_not_author',
}
USER_UPDATED_DATA = {
    'email': 'newtest@notauthor.com',
    'first_name': 'new_test_user',
    'last_name': 'new_test_user',
}


# Include internal repo to sys.path for import from db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_app():
    """Start FastAPI app, include routes."""
    app = FastAPI()
    app.include_router(api_router)
    add_pagination(app)
    return app


TEST_DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(
    TEST_DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    """Create new db tables for each test case."""
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """Create test database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # Use session in tests
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """Create FastAPI TestClient, override the get_db dependency."""

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def superuser(db_session):
    """Create and return superuser."""
    superuser = User(
        email=SUPERUSER_DATA['email'],
        is_superuser=SUPERUSER_DATA['is_superuser'],
        password=Hasher.get_hashed_password(SUPERUSER_DATA['password']),
        username=SUPERUSER_DATA['username'],
    )
    db_session.add(superuser)
    db_session.commit()
    return superuser


@pytest.fixture
def superuser_token(superuser):
    """Create JWT for superuser."""
    return jwt.encode(
        algorithm=settings.ENCODE_ALGORITHM,
        claims={
            'username': superuser.username, 'password': superuser.password
        },
        key=settings.SECRET_KEY,
    )


@pytest.fixture
def superuser_client(app, client, superuser_token):
    """Create and return authenticated superuser client."""
    return TestClient(
        app=app,
        headers={'Authorization': f"Bearer {superuser_token}"}
    )


@pytest.fixture
def author(db_session):
    """Create User instance for post author."""
    author = User(
        email=USER_AUTHOR_DATA['email'],
        password=Hasher.get_hashed_password(USER_AUTHOR_DATA['password']),
        username=USER_AUTHOR_DATA['username'],
    )
    db_session.add(author)
    db_session.commit()
    return author


@pytest.fixture
def author_token(author):
    """Create JWT for author."""
    return jwt.encode(
        algorithm=settings.ENCODE_ALGORITHM,
        claims={
            'username': author.username, 'password': author.password
        },
        key=settings.SECRET_KEY,
    )


@pytest.fixture
def author_client(app, client, author_token):
    """Create and return authenticated author client."""
    return TestClient(
        app=app,
        headers={'Authorization': f"Bearer {author_token}"}
    )


@pytest.fixture
def not_author(db_session):
    """Create User instance for not author."""
    not_author = User(
        email=USER_NOT_AUTHOR_DATA['email'],
        password=Hasher.get_hashed_password(USER_NOT_AUTHOR_DATA['password']),
        username=USER_NOT_AUTHOR_DATA['username'],
    )
    db_session.add(not_author)
    db_session.commit()
    return not_author


@pytest.fixture
def many_not_authors(db_session):
    """Create PAGE_SIZE_USER + 1 User instances."""
    user_email = USER_NOT_AUTHOR_DATA.get('email')
    user_password = USER_NOT_AUTHOR_DATA.get('password')
    user_username = USER_NOT_AUTHOR_DATA.get('username')
    db_session.bulk_save_objects([
        User(
            email=f'{index}{user_email}',
            password=f'{user_password} {index}',
            username=f'{user_username} {index}'
        )
        for index in range(settings.PAGE_SIZE_USER + 1)
    ])
    db_session.commit()


@pytest.fixture
def not_author_token(not_author):
    """Create JWT for not author."""
    return jwt.encode(
        algorithm=settings.ENCODE_ALGORITHM,
        claims={
            'username': not_author.username, 'password': not_author.password
        },
        key=settings.SECRET_KEY,
    )


@pytest.fixture
def not_author_client(app, client, not_author_token):
    """Create and return authenticated not author client."""
    return TestClient(
        app=app,
        headers={'Authorization': f"Bearer {not_author_token}"}
    )


@pytest.fixture
def group(db_session):
    """Create and return Group instance."""
    group = Group(**GROUP_DATA)
    db_session.add(group)
    db_session.commit()
    return group


@pytest.fixture
def many_groups(db_session):
    """Create PAGE_SIZE_GROUP + 1 Group instances."""
    group_description = GROUP_DATA.get('description')
    group_slug = GROUP_DATA.get('slug')
    group_title = GROUP_DATA.get('title')
    db_session.bulk_save_objects([
        Group(
            description=f'{group_description} {index}',
            slug=f'{group_slug}{index}',
            title=f'{group_title} {index}'
        )
        for index in range(settings.PAGE_SIZE_GROUP + 1)
    ])
    db_session.commit()


@pytest.fixture
def group_updated(db_session):
    """Create and return updated Group instance."""
    group = Group(**GROUP_UPDATED_DATA)
    db_session.add(group)
    db_session.commit()
    return group


@pytest.fixture
def post_data(group):
    """Return post data."""
    post_data = POST_DATA.copy()
    post_data.update({
        'group_id': group.id,
    })
    return post_data


@pytest.fixture
def post_updated_data(group_updated):
    """Return updated post data."""
    post_updated_data = POST_UPDATED_DATA.copy()
    post_updated_data.update({
        'group_id': group_updated.id,
    })
    return post_updated_data


@pytest.fixture
def post(author, db_session, group):
    """Create and return Post instance."""
    post = Post(
        author_id=author.id, group_id=group.id, **POST_DATA
    )
    db_session.add(post)
    db_session.commit()
    return post


@pytest.fixture
def many_posts(author, db_session, group):
    """Create PAGE_SIZE_POST + 1 Post instances."""
    post_text = POST_DATA.get('text')
    post_title = POST_DATA.get('title')
    db_session.bulk_save_objects([
        Post(
            author_id=author.id,
            group_id=group.id,
            pub_date=datetime.today() - timedelta(days=index),
            text=f'{post_text} {index}',
            title=f'{post_title} {index}'
        )
        for index in range(settings.PAGE_SIZE_POST + 1)
    ])
    db_session.commit()


@pytest.fixture
def login():
    """Return user login url."""
    return f'{API_URL_PREFIX}/login/token'


@pytest.fixture
def users_list():
    """Return users list url."""
    return f'{API_URL_PREFIX}/users'


@pytest.fixture
def user_detail(not_author, users_list):
    """Return user detail url."""
    return f'{users_list}/{not_author.id}'


@pytest.fixture
def current_user_detail(not_author, users_list):
    """Return current user detail url."""
    return f'{users_list}/me'


@pytest.fixture
def group_list():
    """Return groups list url."""
    return f'{API_URL_PREFIX}/groups'


@pytest.fixture
def group_detail(group, group_list):
    """Return group detail url."""
    return f'{group_list}/{group.id}'


@pytest.fixture
def posts_list():
    """Return posts list url."""
    return f'{API_URL_PREFIX}/posts'


@pytest.fixture
def post_detail(post, posts_list):
    """Return post detail url."""
    return f'{posts_list}/{post.id}'
