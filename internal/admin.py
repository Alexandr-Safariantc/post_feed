from sqladmin import ModelView

from db.models import Group, Post, User


class GroupAdmin(ModelView, model=Group):
    """Group model view for admin site."""

    name_plural = 'Groups'
    column_exclude_list = [Group.description]
    column_searchable_list = [Group.slug, Group.title]
    column_default_sort = 'created_at'


class PostAdmin(ModelView, model=Post):
    """Post model view for admin site."""

    name_plural = 'Posts'
    column_exclude_list = [Post.text, Post.author_id, Post.group_id]
    column_sortable_list = [Post.pub_date]
    column_searchable_list = [Post.author, Post.group, Post.title]


class UserAdmin(ModelView, model=User):
    """User model view for admin site."""

    name_plural = 'Users'
    column_exclude_list = [
        User.password, User.first_name, User.updated_on, User.posts
    ]
    column_sortable_list = [User.is_active, User.is_superuser]
    column_searchable_list = [User.email, User.last_name, User.username]
    column_default_sort = 'date_joined'
