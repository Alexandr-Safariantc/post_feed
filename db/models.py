import datetime as dt

from sqlalchemy.orm import declarative_base, relationship
import sqlalchemy as db

from core.config import settings


Base = declarative_base()


class User(Base):
    """Model for users."""

    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    date_joined = db.Column(db.DateTime(), default=dt.datetime.now())
    email = db.Column(
        db.String(settings.EMAIL_MAX_LENGTH),
        index=True,
        nullable=False,
        unique=True
    )
    first_name = db.Column(db.String(settings.FIRST_LAST_NAMES_MAX_LENGTH))
    is_active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    last_name = db.Column(db.String(settings.FIRST_LAST_NAMES_MAX_LENGTH))
    password = db.Column(db.String(), nullable=False)
    posts = relationship('Post', cascade='all, delete')
    updated_on = db.Column(
        db.DateTime(), default=dt.datetime.now(), onupdate=dt.datetime.now()
    )
    username = db.Column(
        db.String(settings.USERNAME_MAX_LENGTH),
        index=True,
        nullable=False,
        unique=True
    )

    def __repr__(self) -> str:
        return f'{self.username}'


class Group(Base):
    """Model for groups with posts."""

    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=dt.datetime.now())
    description = db.Column(db.Text(), nullable=False)
    slug = db.Column(
        db.String(settings.GROUP_SLUG_MAX_LENGTH),
        nullable=False,
        unique=True
    )
    title = db.Column(
        db.String(settings.GROUP_TITLE_MAX_LENGTH), nullable=False
    )

    __table_args__ = (db.Index(
        'title_description_index' 'title', 'description'),
    )

    def __repr__(self) -> str:
        return self.title


class Post(Base):
    """Model for posts."""

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, index=True)
    author = relationship('User', overlaps='posts')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group = relationship('Group')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    pub_date = db.Column(db.DateTime(), default=dt.datetime.now())
    text = db.Column(db.Text(), nullable=False, index=True)
    title = db.Column(
        db.String(settings.POST_TITLE_MAX_LENGTH), nullable=False, index=True
    )

    def __repr__(self) -> str:
        return (f'Текст: {self.text[:30]}; Автор: {self.author};'
                f' Группа: {self.group}; Опубликован: {self.pub_date};')
