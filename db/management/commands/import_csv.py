import csv
import datetime as dt

import click

from core.config import settings
from db.models import Group, Post, User
from db.session import SessionLocal


TABLES = {
    'groups': Group,
    'users': User,
    'posts': Post,
}


def handle():
    """Extract data from .csv file and call create_object func."""
    for table in TABLES:
        file_path = f'{settings.CSV_IMPORT_FILE_PATH}/{table}.csv'
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                csv_data = [
                    row for row in csv.DictReader(csvfile, delimiter='|')
                ]
        except FileNotFoundError:
            raise FileExistsError(settings.CSV_IMPORT_INVALID_PATH.format(
                path=file_path
            ))
        else:
            create_object(
                cls=TABLES[table], csv_data=csv_data, table=table,
            )


def create_object(cls, csv_data, table):
    """Create objects with data from .csv file."""
    print_info(name=table)
    db = SessionLocal()
    for obj_data in csv_data:
        if table in ['groups', 'users']:
            db.add(cls(**obj_data))
            db.commit()
        elif table == 'posts':
            db.add(Post(
                author_id=int(obj_data.get('author_id')),
                group_id=int(obj_data.get('group_id')),
                pub_date=dt.datetime.strptime(
                    obj_data.get('pub_date'),
                    settings.CSV_IMPORT_TIME_FORMAT
                ),
                text=obj_data.get('text'),
                title=obj_data.get('title'),
            ))
            db.commit()
    print_info(name=table, obj_count=len(csv_data))


def print_info(name, obj_count=None):
    """Print process and success import message."""
    if obj_count is None:
        click.secho(
            settings.CSV_IMPORT_PROCCESSING.format(filename=name),
            fg='yellow',
        )
    else:
        click.secho(
            settings.CSV_IMPORT_SUCCESS.format(
                count=obj_count, filename=name
            ),
            fg='green',
        )
