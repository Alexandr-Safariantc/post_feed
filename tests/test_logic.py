from http import HTTPStatus

import pytest

from conftest import (
    GROUP_DATA,
    GROUP_UPDATED_DATA,
    POST_DATA,
    SUPERUSER_DATA,
    USER_NOT_AUTHOR_DATA,
    USER_UPDATED_DATA,
)
from core.hashing import Hasher
from db.models import Group, Post, User
import utils


def test_user_cant_create_group(db_session, group_list, not_author_client):
    """Creating group is unavailable for regular user."""
    assert not_author_client.post(
        group_list, json=GROUP_DATA
    ).status_code == HTTPStatus.UNAUTHORIZED
    assert db_session.query(Group).count() == 0


def test_superuser_can_create_group(db_session, group_list, superuser_client):
    """Creating group is available for superuser."""
    assert superuser_client.post(
        group_list, json=GROUP_DATA
    ).status_code == HTTPStatus.CREATED
    assert db_session.query(Group).count() == 1
    created_group = db_session.query(Group).first()
    assert created_group.description == GROUP_DATA.get('description')
    assert created_group.slug == GROUP_DATA.get('slug')
    assert created_group.title == GROUP_DATA.get('title')


@pytest.mark.parametrize('client_, data, status', (
    (utils.AUTHENTICATED_USER, GROUP_DATA, HTTPStatus.UNAUTHORIZED),
    (utils.SUPERUSER, GROUP_UPDATED_DATA, HTTPStatus.OK),
))
def test_update_group(client_, data, status, group, group_detail):
    """Update group is available for superuser only."""
    assert client_.put(
        group_detail, json=GROUP_UPDATED_DATA
    ).status_code == status
    assert group.description == data.get('description')
    assert group.slug == data.get('slug')
    assert group.title == data.get('title')


@pytest.mark.parametrize('client_, data, status', (
    (utils.AUTHENTICATED_USER, GROUP_DATA, HTTPStatus.UNAUTHORIZED),
    (utils.SUPERUSER, GROUP_UPDATED_DATA, HTTPStatus.OK),
))
def test_partial_update_group(client_, data, status, group, group_detail):
    """Partial update group is available for superuser only."""
    assert client_.patch(
        group_detail, json=GROUP_UPDATED_DATA
    ).status_code == status
    assert group.description == data.get('description')
    assert group.slug == data.get('slug')
    assert group.title == data.get('title')


def test_user_cant_delete_group(
    db_session, group, group_detail, not_author_client
):
    """Deleting group is unavailable for regular user."""
    assert not_author_client.delete(
        group_detail
    ).status_code == HTTPStatus.UNAUTHORIZED
    assert db_session.query(Group).count() == 1
    assert group.description == GROUP_DATA.get('description')
    assert group.slug == GROUP_DATA.get('slug')
    assert group.title == GROUP_DATA.get('title')


def test_superuser_can_delete_group(
    db_session, group_detail, superuser_client
):
    """Deleting group is available for superuser."""
    assert superuser_client.delete(
        group_detail
    ).status_code == HTTPStatus.NO_CONTENT
    assert db_session.query(Group).count() == 0


def test_anon_user_cant_create_post(client, db_session, posts_list):
    """Creating post is unavailable for regular user."""
    assert client.post(
        posts_list, json=POST_DATA
    ).status_code == HTTPStatus.UNAUTHORIZED
    assert db_session.query(Post).count() == 0


def test_auth_user_can_create_post(
    author, author_client, db_session, post_data, posts_list
):
    """Creating post is available for authenticated user."""
    assert author_client.post(
        posts_list, json=post_data
    ).status_code == HTTPStatus.CREATED
    assert db_session.query(Post).count() == 1
    created_post = db_session.query(Post).first()
    assert created_post.author_id == author.id
    assert created_post.group_id == post_data.get('group_id')
    assert created_post.text == post_data.get('text')
    assert created_post.title == post_data.get('title')


@pytest.mark.parametrize('client_, data, status', (
    (utils.AUTHENTICATED_USER, utils.POST_DATA, HTTPStatus.UNAUTHORIZED),
    (utils.AUTHENTICATED_AUTHOR, utils.POST_UPDATED_DATA, HTTPStatus.OK),
))
def test_update_post(author, client_, data, post, post_detail, status):
    """Update post is available for author only."""
    assert client_.put(post_detail, json=data).status_code == status
    assert post.author_id == author.id
    assert post.group_id == data.get('group_id')
    assert post.text == data.get('text')
    assert post.title == data.get('title')


@pytest.mark.parametrize('client_, data, status', (
    (utils.AUTHENTICATED_USER, utils.POST_DATA, HTTPStatus.UNAUTHORIZED),
    (utils.AUTHENTICATED_AUTHOR, utils.POST_UPDATED_DATA, HTTPStatus.OK),
))
def test_partial_update_post(author, client_, data, post, post_detail, status):
    """Partial update post is available for author only."""
    assert client_.patch(post_detail, json=data).status_code == status
    assert post.author_id == author.id
    assert post.group_id == data.get('group_id')
    assert post.text == data.get('text')
    assert post.title == data.get('title')


def test_not_author_cant_delete_post(
    author, db_session, not_author_client, post, post_data, post_detail
):
    """Deleting post is unavailable for not author user."""
    assert not_author_client.delete(
        post_detail
    ).status_code == HTTPStatus.UNAUTHORIZED
    assert db_session.query(Post).count() == 1
    assert post.author_id == author.id
    assert post.group_id == post_data.get('group_id')
    assert post.text == post_data.get('text')
    assert post.title == post_data.get('title')


@pytest.mark.parametrize('client_,', (
    (utils.AUTHENTICATED_AUTHOR, utils.SUPERUSER,)
))
def test_author_superuser_can_delete_post(client_, db_session, post_detail):
    """Deleting post is available for author and superuser."""
    assert client_.delete(
        post_detail
    ).status_code == HTTPStatus.NO_CONTENT
    assert db_session.query(Post).count() == 0


@pytest.mark.parametrize('data,', (
    (USER_NOT_AUTHOR_DATA, SUPERUSER_DATA,)
))
def test_user_creation(client, data, db_session, users_list):
    """Anonymous can create regular user but not superuser."""
    assert client.post(
        users_list, json=data
    ).status_code == HTTPStatus.CREATED
    assert db_session.query(User).count() == 1
    created_user = db_session.query(User).first()
    assert created_user.email == data.get('email')
    assert Hasher.verify_password(data.get('password'), created_user.password)
    assert created_user.username == data.get('username')
    assert created_user.is_superuser is False


@pytest.mark.parametrize('client_, data, status', (
    (
        utils.AUTHENTICATED_USER,
        USER_UPDATED_DATA,
        HTTPStatus.OK
    ),
    (
        utils.UNAUTHENTICATED_USER,
        USER_NOT_AUTHOR_DATA,
        HTTPStatus.UNAUTHORIZED
    ),
))
def test_update_user(client_, current_user_detail, data, not_author, status):
    """Update user data is available for auth user only."""
    assert client_.put(
        current_user_detail, json=USER_UPDATED_DATA
    ).status_code == status
    assert not_author.email == data.get('email')
    assert not_author.first_name == data.get('first_name')
    assert not_author.last_name == data.get('last_name')


@pytest.mark.parametrize('client_, data, status', (
    (
        utils.AUTHENTICATED_USER,
        USER_UPDATED_DATA,
        HTTPStatus.OK
    ),
    (
        utils.UNAUTHENTICATED_USER,
        USER_NOT_AUTHOR_DATA,
        HTTPStatus.UNAUTHORIZED
    ),
))
def test_partial_update_user(
    client_, current_user_detail, data, not_author, status
):
    """Partial update user data is available for auth user only."""
    assert client_.patch(
        current_user_detail, json=USER_UPDATED_DATA
    ).status_code == status
    assert not_author.email == data.get('email')
    assert not_author.first_name == data.get('first_name')
    assert not_author.last_name == data.get('last_name')


@pytest.mark.parametrize('client_, status, content', (
    (utils.AUTHENTICATED_USER, HTTPStatus.OK, 'access_token'),
    (utils.UNAUTHENTICATED_USER, HTTPStatus.NOT_FOUND, 'detail'),
))
def test_getting_access_token(client_, content, login, status):
    """Getting access token is available for auth users only."""
    response = client_.post(login, data=USER_NOT_AUTHOR_DATA)
    assert response.status_code == status
    assert content in response.json()
