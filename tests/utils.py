import pytest


GROUP_DETAIL_URL = pytest.lazy_fixture('group_detail')
GROUPS_LIST_URL = pytest.lazy_fixture('group_list')
LOGIN_URL = pytest.lazy_fixture('login')
POST_DETAIL_URL = pytest.lazy_fixture('post_detail')
POSTS_LIST_URL = pytest.lazy_fixture('posts_list')
USER_DETAIL_URL = pytest.lazy_fixture('user_detail')
USER_ME_URL = pytest.lazy_fixture('current_user_detail')
USERS_LIST_URL = pytest.lazy_fixture('users_list')

AUTHENTICATED_AUTHOR = pytest.lazy_fixture('author_client')
AUTHENTICATED_USER = pytest.lazy_fixture('not_author_client')
SUPERUSER = pytest.lazy_fixture('superuser_client')
UNAUTHENTICATED_USER = pytest.lazy_fixture('client')

POST_DATA = pytest.lazy_fixture('post_data')
POST_UPDATED_DATA = pytest.lazy_fixture('post_updated_data')
