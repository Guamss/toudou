from datetime import datetime

import uuid
from toudou import config
import click

import toudou.services as services
import toudou.models as models

@click.group()
def cli():
    models.createTable()

@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    todo = models.create_todo(task, due, False)
    if todo:
        click.echo("Your toudou has been created successfully")
    else:
        click.echo("An error has occured")

@cli.command()
@click.argument("csv_file", type=click.File("r"))
def import_csv(csv_file):
    services.import_from_csv(csv_file)

@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Search a stored toudou")
def display(id: uuid):
    toudou = models.getToudou(id)
    if toudou:
        id, task, date, completed = toudou
        todo = models.Todo(id=id, task=task, date=date, completed=completed)
        click.echo(todo)
    else:
        click.echo("This toudou does not exist")


@cli.command()
@click.option("--as-csv", is_flag=True)
def display_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv().getvalue())
    else:
        toudous = models.getToudous()
        if len(toudous) > 0:
            for toudou in toudous:
                click.echo(toudou)
        else:
            click.echo("You don't have any toudous stored yet")

@cli.command()
@click.option("--id", required=True, type=click.UUID, help="Todo's id.")
@click.option("-c", "--complete", required=True, type=click.BOOL, help="Todo is done or not.")
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due",type=click.DateTime(formats=["%Y-%m-%d"]), default=None, help="Due date of the task.")
def update(id: uuid.UUID, complete: bool, task: str, due: datetime):
    models.update_todo(id, task, complete, due)

@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Complete a toudou")
def complete(id: uuid):
    todo = models.complete_task(id)
    if todo:
        click.echo("Your toudou has been changed successfully")
    else:
        click.echo("This toudou does not exist")


@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Delete a already existing toudou")
def delete(id: uuid):
    todo = models.delete_task(id)
    if todo:
        click.echo("Your toudou has been deleted successfully")
    else:
        click.echo("An error has occured")