import click

from .db import db


def init_app(app):
    @app.cli.command("initdb")
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def init_db(drop):
        """

        init the app database.

        """
        if drop:
            click.confirm("This operation will delete the database, do you want to continue?", abort=True)
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")
