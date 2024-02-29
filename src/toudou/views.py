from datetime import datetime
import uuid
import click

import toudou.models as models

@click.group()
def cli():
    pass

@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    models.create_todo(task, due)


@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Search a stored toudou")
def display(id: uuid):
    toudou = models.Todo.getToudou(id)
    if toudou:
        id, task, date, completed = toudou
        todo = models.Todo(id=id, task=task, date=date, completed=completed)
        click.echo(todo)
    else:
        click.echo("This toudou does not exist")


@cli.command()
def display_all():
    pass
    toudous = models.Todo.getToudous()
    if len(toudous) > 0:
        for toudou in toudous:
            id, task, date, completed = toudou
            todo = models.Todo(id=id, task=task, date=date, completed=completed)
            click.echo(todo)
    else:
        click.echo("You don't have any toudous stored yet")

@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Complete a toudou")
def complete(id: uuid):
    todo = models.complete_task(id)
    if todo:
        click.echo("Your toudou has been changed successfully")
    else:
        click.echo("This toudou does not exist")
