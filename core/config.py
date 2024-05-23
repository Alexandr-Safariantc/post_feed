import os

from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Project constants."""

    # Main project data
    PROJECT_NAME = 'PostFeed'
    PROJECT_VERSION = '1.0.0'

    # Database settings
    SQLALCHEMY_DATABASE_URL = 'sqlite:///postfeed.db'

    # User constants
    EMAIL_MAX_LENGTH = 100
    FIRST_LAST_NAMES_MAX_LENGTH = 50
    PASSWORD_MAX_LENGTH = 64
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_PATTERN = r'(.*[a-z].*)(.*[A-Z].*).+'
    USERNAME_MAX_LENGTH = 50
    USERNAME_MIN_LENGTH = 7
    USERNAME_PATTERN = r'^[A-Za-z][A-Za-z0-9_]+$'

    # Group constants
    GROUP_SLUG_MAX_LENGTH = 50
    GROUP_SLUG_PATTERN = r'^[a-z0-9-]+$'
    GROUP_TITLE_MAX_LENGTH = 100

    # Post constants
    POST_TITLE_MAX_LENGTH = 200

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600
    ENCODE_ALGORITHM = 'HS256'
    SECRET_KEY: str = os.getenv('SECRET_KEY')

    # CSV import settings
    CSV_IMPORT_FILE_PATH = './db/csv_data'
    CSV_IMPORT_INVALID_PATH = 'Error! {path} not found'
    CSV_IMPORT_PROCCESSING = ('Importing objects from'
                              ' {filename}.csv is processing...')
    CSV_IMPORT_SUCCESS = ('{count} objects from {filename}.csv has been '
                          ' successfully imported into {filename} model')
    CSV_IMPORT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    # Pagination settings
    PAGE_SIZE_NAME = 'Page size'
    PAGE_SIZE_MAX = 25
    PAGE_SIZE_MIN = 1
    PAGE_SIZE_GROUP = 10
    PAGE_SIZE_POST = 5
    PAGE_SIZE_USER = 10

    # Messages
    OBJECT_DELETED_MSG = '{object} with id:{id} successfully deleted'
    OBJECT_NOT_FOUND_MSG = '{object} with id:{id} does not exist'
    ONLY_POST_AUTHOR_ACTION_MSG = 'Only author can {action} the post'

    SUPERUSER_RESOURCE_MSG = 'Resource for superusers only'
    INVALID_CREDENTIALS_MSG = 'Invalid credentials'


settings = Settings()
