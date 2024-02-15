from dataclasses import dataclass
import datetime

import sqlite3

from os import listdir, mkdir, path
import pickle
import uuid

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
            return f"Toudou {self.task} has to be completed before {self.date.strftime('%d/%m/%Y')}"
        else:
            return f"Toudou {self.task} has not been completed"


def complete(task: Todo):
    todo = None
    files = Todo.getAllFiles()
    for file in files:
        actual_todo = file[:-2]
        if actual_todo == task:
            todo = Todo.getByFileName(file)
    return todo

def display(id: uuid):
    todo = None
    file = f"{PATH}/{id}.p"
    if path.isfile(file):
        with open(file, 'rb') as f:
            todo = pickle.load(f)
    return todo

def create_todo(task: str, due: datetime, arg_con):
    con = arg_con
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO toudou (id, task, date, completed) VALUES (?, ?, ?, ?)", (uuid.uuid4(), task, due, False))
    except sqlite3.Error as e:
        print("Erreur : ", e)

def init_db():
    con = getConn()
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS toudou(id INTEGER UNIQUE, task TEXT, date DATE, completed BOOLEAN)")

    except sqlite3.Error as e:
        print("Erreur :", e)

def getConn():
    return sqlite3.connect("toudou.db")
