import pytest

from core.config import settings
from tests.conftest import (
    GROUP_UPDATED_DATA,
    POST_UPDATED_DATA,
    USER_AUTHOR_DATA,
    USER_UPDATED_DATA,
)
import utils


@pytest.mark.parametrize('url, client_, page_size', (
    (
        utils.GROUPS_LIST_URL,
        utils.AUTHENTICATED_USER,
        settings.PAGE_SIZE_GROUP
    ),
    (
        utils.POSTS_LIST_URL,
        utils.AUTHENTICATED_USER,
        settings.PAGE_SIZE_POST
    ),
    (
        utils.USERS_LIST_URL,
        utils.SUPERUSER,
        settings.PAGE_SIZE_USER
    ),
))
def test_pagination(
    client_, many_groups, many_not_authors, many_posts, page_size, url
):
    """Group, post, user pages paginator test."""
    response = client_.get(url)
    assert len(response.json().get('items')) == page_size
    assert response.json().get('size') == page_size


@pytest.mark.parametrize('url, client_, order_field', (
    (
        utils.GROUPS_LIST_URL,
        utils.AUTHENTICATED_USER,
        'created_at'
    ),
    (
        utils.POSTS_LIST_URL,
        utils.AUTHENTICATED_USER,
        'pub_date'
    ),
))
def test_ordering(client_, many_groups, many_posts, order_field, url):
    """Group, post pages paginator test."""
    all_dates = [
        obj.get(order_field) for obj
        in client_.get(url).json().get('items')
    ]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.parametrize('client_, url, method, data', (
    (utils.SUPERUSER, utils.GROUPS_LIST_URL, 'get', None),
    (utils.SUPERUSER, utils.GROUPS_LIST_URL, 'post', GROUP_UPDATED_DATA),
    (utils.SUPERUSER, utils.GROUP_DETAIL_URL, 'get', None),
    (utils.SUPERUSER, utils.GROUP_DETAIL_URL, 'put', GROUP_UPDATED_DATA),
    (utils.SUPERUSER, utils.GROUP_DETAIL_URL, 'patch', GROUP_UPDATED_DATA),
))
def test_group_content(client_, data, group, group_list, method, url):
    """Check response content from Group endpoints."""
    if data is None:
        response = client_.get(url).json()
        if url == group_list:
            response = response.get('items')[0]
    if method == 'post':
        response = client_.post(url, json=data).json()
    if method == 'put':
        response = client_.put(url, json=data).json()
    if method == 'patch':
        response = client_.patch(url, json=data).json()
    assert 'id' in response
    assert 'created_at' in response
    assert 'description' in response
    assert 'slug' in response
    assert 'title' in response


@pytest.mark.parametrize('client_, url, method, data', (
    (
        utils.AUTHENTICATED_AUTHOR,
        utils.POSTS_LIST_URL,
        'get',
        None
    ),
    (
        utils.AUTHENTICATED_AUTHOR,
        utils.POSTS_LIST_URL,
        'post',
        utils.POST_DATA
    ),
    (
        utils.AUTHENTICATED_AUTHOR,
        utils.POST_DETAIL_URL,
        'get',
        None
    ),
    (
        utils.AUTHENTICATED_AUTHOR,
        utils.POST_DETAIL_URL,
        'put',
        utils.POST_DATA
    ),
    (
        utils.AUTHENTICATED_AUTHOR,
        utils.POST_DETAIL_URL,
        'patch',
        POST_UPDATED_DATA
    ),
))
def test_post_content(client_, data, post, posts_list, method, url):
    """Check response content from Post endpoints."""
    if data is None:
        response = client_.get(url).json()
        if url == posts_list:
            response = response.get('items')[0]
    if method == 'post':
        response = client_.post(url, json=data).json()
    if method == 'put':
        response = client_.put(url, json=data).json()
    if method == 'patch':
        response = client_.patch(url, json=data).json()
    assert 'id' in response
    assert 'author_id' in response
    assert 'group_id' in response
    assert 'pub_date' in response
    assert 'text' in response
    assert 'title' in response


@pytest.mark.parametrize('client_, url, method, data', (
    (utils.SUPERUSER, utils.USERS_LIST_URL, 'get', None),
    (utils.AUTHENTICATED_USER, utils.USERS_LIST_URL, 'post', USER_AUTHOR_DATA),
    (utils.SUPERUSER, utils.USER_DETAIL_URL, 'get', None),
    (utils.AUTHENTICATED_USER, utils.USER_ME_URL, 'get', None),
    (utils.AUTHENTICATED_USER, utils.USER_ME_URL, 'put', USER_UPDATED_DATA),
    (utils.AUTHENTICATED_USER, utils.USER_ME_URL, 'patch', USER_UPDATED_DATA),
))
def test_user_content(client_, data, not_author, users_list, method, url):
    """Check response content from User endpoints."""
    if data is None:
        response = client_.get(url).json()
        if url == users_list:
            response = response.get('items')[0]
    if method == 'post':
        response = client_.post(url, json=data).json()
    if method == 'put':
        response = client_.put(url, json=data).json()
    if method == 'patch':
        response = client_.patch(url, json=data).json()
    assert 'id' in response
    assert 'date_joined' in response
    assert 'email' in response
    assert 'first_name' in response
    assert 'is_active' in response
    assert 'last_name' in response
    assert 'username' in response
    assert 'is_superuser' in response
