import click

from db.management.commands import import_csv


@click.group()
def posts():
    """
    A web app for reading posts in feed and publishing your own.
    You can add test data into database to try project features.
    """
    pass


@posts.command(help='Import test data from .csv file into database.')
def test_data():
    import_csv.handle()
    click.secho(
        bold=True,
        fg='green',
        message='Test data was successfully imported!',
    )


if __name__ == '__main__':
    posts()
