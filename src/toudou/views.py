from datetime import datetime
import uuid
import click
from flask import Flask

import toudou.models as models

app = Flask(__name__)

@click.group()
def cli():
    pass

@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    todo = models.create_todo(task, due)
    if todo:
        click.echo("Your toudou has been created successfully")
    else:
        click.echo("An error has occured")


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


@cli.command()
@click.option("-i", "--id", type=click.UUID, prompt="ID", help="Delete a already existing toudou")
def delete(id: uuid):
    todo = models.delete_task(id)
    if todo:
        click.echo("Your toudou has been deleted successfully")
    else:
        click.echo("An error has occured")


@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run()