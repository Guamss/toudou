import datetime
import pickle
import click
import uuid

from os import mkdir
from os import path
from os import listdir

from dataclasses import dataclass

PATH = "./toudou_files"


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    date: datetime.date = None
    completed: bool = False


    def changeStateCompleted(self):
        self.completed = not self.completed

    @staticmethod
    def getAllFiles():
        return [f for f in listdir(PATH) if f[-2:] == ".p"]

    @staticmethod
    def getByFileName(file: str):
        try:
            with open(f'{PATH}/{file}', 'rb') as f:
                return pickle.load(f)
        except:
            print("This file does not exist !")

    def store(self):
        if not path.exists(PATH):
            mkdir(f"{PATH}")
        with open(f'{PATH}/{self.id}.p', 'wb') as f:
            pickle.dump(self, f)

    def __str__(self):
        if self.completed:
            return f"Toudou {self.task} has been completed"
        elif not self.completed and self.date:
            return f"Toudou {self.task} has to be completed before {self.date}"
        else:
            return f"Toudou {self.task} has not been completed"


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
#TODO : date à mettre
def create(task: str):
    todo = Todo(uuid.uuid4(), task)
    todo.store()


@cli.command()
@click.option("-i", "--id", prompt="ID", help="Search a stored toudou")
def show(id: uuid):
    try:
        file = f"{PATH}/{id}.p"
        if path.isfile(file):
            with open(file, 'rb') as f:
                todo = pickle.load(f)
                click.echo(todo)
    except:
        click.echo("This toudou does not exist")

@cli.command()
def display():
    files = Todo.getAllFiles()
    for file in files:
        click.echo(Todo.getByFileName(file))

@cli.command()
@click.option("-t", "--task", prompt="Your task", help="Complete a toudou")
def complete(task: Todo):
    todo = None
    files = Todo.getAllFiles()
    for file in files:
        actual_todo = file[:-2]
        if actual_todo == task:
            todo = Todo.getByFileName(file)
    if todo:
        todo.changeStateCompleted()
        todo.store()
        click.echo("Your toudou has been changed successfully")
    else:
        click.echo("This toudou does not exist")
