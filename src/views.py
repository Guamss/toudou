from datetime import datetime
from os import path
import pickle
import uuid


import click

import models as models

@click.group()
def cli():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    models.create_todo(task, due, models.getConn())




@cli.command()
@click.option("-i", "--id", prompt="ID", help="Search a stored toudou")
def display(id: uuid):
    todo = models.display(id)
    if todo:
        click.echo(todo)
    else:
        click.echo("This toudou does not exist")
        exit(0)

@cli.command()
def display_all():
    files = models.Todo.getAllFiles()
    for file in files:
        click.echo(models.Todo.getByFileName(file))

@cli.command()
@click.option("-t", "--task", prompt="ID", help="Complete a toudou")
def complete(task: models.Todo):
    todo = models.complete(task)
    if todo:
        todo.changeStateCompleted()
        todo.store()
        click.echo("Your toudou has been changed successfully")
    else:
        click.echo("This toudou does not exist")