from http import HTTPStatus

import pytest

from tests.conftest import (
    GROUP_DATA,
    GROUP_UPDATED_DATA,
    POST_DATA,
    POST_UPDATED_DATA,
    USER_AUTHOR_DATA,
    USER_NOT_AUTHOR_DATA,
)
import utils


@pytest.mark.parametrize('url, client_, status', (
    (utils.GROUP_DETAIL_URL, utils.UNAUTHENTICATED_USER, HTTPStatus.OK),
    (utils.GROUPS_LIST_URL, utils.UNAUTHENTICATED_USER, HTTPStatus.OK),
    (utils.POST_DETAIL_URL, utils.UNAUTHENTICATED_USER, HTTPStatus.OK),
    (utils.POSTS_LIST_URL, utils.UNAUTHENTICATED_USER, HTTPStatus.OK),
    (
        utils.USER_DETAIL_URL,
        utils.UNAUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (utils.USER_DETAIL_URL, utils.SUPERUSER, HTTPStatus.OK),
    (utils.USER_ME_URL, utils.UNAUTHENTICATED_USER, HTTPStatus.UNAUTHORIZED),
    (utils.USER_ME_URL, utils.AUTHENTICATED_USER, HTTPStatus.OK),
    (
        utils.USERS_LIST_URL,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (utils.USERS_LIST_URL, utils.SUPERUSER, HTTPStatus.OK),
))
def test_get_method_availability(url, client_, status):
    """Get method availability for not auth, auth, superuser clients."""
    assert client_.get(url).status_code == status


@pytest.mark.parametrize('url, data, client_, status', (
    (
        utils.GROUPS_LIST_URL,
        GROUP_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.GROUPS_LIST_URL,
        GROUP_DATA,
        utils.SUPERUSER,
        HTTPStatus.CREATED
    ),
    (
        utils.LOGIN_URL,
        USER_AUTHOR_DATA,
        utils.AUTHENTICATED_AUTHOR,
        HTTPStatus.OK
    ),
    (
        utils.POSTS_LIST_URL,
        POST_DATA,
        utils.UNAUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.POSTS_LIST_URL,
        POST_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.CREATED
    ),
    (
        utils.POSTS_LIST_URL,
        POST_DATA,
        utils.SUPERUSER,
        HTTPStatus.CREATED
    ),
    (
        utils.USERS_LIST_URL,
        USER_NOT_AUTHOR_DATA,
        utils.UNAUTHENTICATED_USER,
        HTTPStatus.CREATED
    ),
))
def test_post_method_availability(
    url, data, client_, status, post_updated_data
):
    """Post method availability for not auth, auth, superuser clients."""
    if data == POST_DATA:
        assert client_.post(url, json=post_updated_data).status_code == status
    elif data == USER_AUTHOR_DATA:
        assert client_.post(url, data=data).status_code == status
    else:
        assert client_.post(url, json=data).status_code == status


@pytest.mark.parametrize('url, data, client_, status', (
    (
        utils.GROUP_DETAIL_URL,
        GROUP_UPDATED_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.GROUP_DETAIL_URL,
        GROUP_UPDATED_DATA,
        utils.SUPERUSER,
        HTTPStatus.OK
    ),
    (
        utils.POST_DETAIL_URL,
        POST_UPDATED_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.POST_DETAIL_URL,
        POST_UPDATED_DATA,
        utils.AUTHENTICATED_AUTHOR,
        HTTPStatus.OK
    ),
    (
        utils.USER_ME_URL,
        USER_NOT_AUTHOR_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.OK
    ),
))
def test_put_method_availability(
    data, client_, post_data, status, url
):
    """Put method availability for not auth, auth, superuser clients."""
    if data == POST_UPDATED_DATA:
        assert client_.put(url, json=post_data).status_code == status
    else:
        assert client_.put(url, json=data).status_code == status


@pytest.mark.parametrize('url, data, client_, status', (
    (
        utils.GROUP_DETAIL_URL,
        GROUP_UPDATED_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.GROUP_DETAIL_URL,
        GROUP_UPDATED_DATA,
        utils.SUPERUSER,
        HTTPStatus.OK
    ),
    (
        utils.POST_DETAIL_URL,
        POST_UPDATED_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.POST_DETAIL_URL,
        POST_UPDATED_DATA,
        utils.AUTHENTICATED_AUTHOR,
        HTTPStatus.OK
    ),
    (
        utils.USER_ME_URL,
        USER_NOT_AUTHOR_DATA,
        utils.AUTHENTICATED_USER,
        HTTPStatus.OK
    ),
))
def test_patch_method_availability(
    data, client_, post_data, status, url
):
    """Patch method availability for not auth, auth, superuser clients."""
    if data == POST_UPDATED_DATA:
        assert client_.put(url, json=post_data).status_code == status
    else:
        assert client_.put(url, json=data).status_code == status


@pytest.mark.parametrize('url, client_, status', (
    (
        utils.GROUP_DETAIL_URL,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.GROUP_DETAIL_URL,
        utils.SUPERUSER,
        HTTPStatus.NO_CONTENT
    ),
    (
        utils.POST_DETAIL_URL,
        utils.AUTHENTICATED_USER,
        HTTPStatus.UNAUTHORIZED
    ),
    (
        utils.POST_DETAIL_URL,
        utils.AUTHENTICATED_AUTHOR,
        HTTPStatus.NO_CONTENT
    ),
    (
        utils.POST_DETAIL_URL,
        utils.SUPERUSER,
        HTTPStatus.NO_CONTENT
    ),
    (
        utils.USER_DETAIL_URL,
        utils.SUPERUSER,
        HTTPStatus.METHOD_NOT_ALLOWED
    ),
))
def test_delete_method_availability(url, client_, status):
    """Delete method availability for not auth, auth, superuser clients."""
    assert client_.delete(url).status_code == status
