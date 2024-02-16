from datetime import datetime
import uuid
import click

import models as models

@click.group()
def cli():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    models.create_todo(task, due, models.getConn())


@cli.command()
@click.option("-i", "--id", prompt="ID", help="Search a stored toudou")
def display(id: uuid):
    toudou = models.Todo.getToudou(id, models.getConn())
    if toudou:
        id, task, date, completed = toudou
        todo = models.Todo(id=id, task=task, date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'), completed=completed)
        click.echo(todo)
    else:
        click.echo("This toudou does not exist")


@cli.command()
def display_all():
    toudous = models.Todo.getToudous(models.getConn())
    if len(toudous) > 0:
        for toudou in toudous:
            id, task, date, completed = toudou
            todo = models.Todo(id=id, task=task, date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'), completed=completed)
            click.echo(todo)
    else:
        click.echo("You don't have any toudous stored yet")

@cli.command()
@click.option("-i", "--id", prompt="ID", help="Complete a toudou")
def complete(id: uuid):
    todo = models.complete_task(id, models.getConn())
    if todo:
        click.echo("Your toudou has been changed successfully")
    else:
        click.echo("This toudou does not exist")