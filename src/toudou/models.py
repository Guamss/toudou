from dataclasses import dataclass, field
from sqlalchemy import create_engine, MetaData, Table, Column, String, Uuid, Boolean, DateTime, select, update, delete, inspect
from sqlalchemy.exc import OperationalError, StatementError, ArgumentError

from os import makedirs

import datetime

import uuid

TODO_FOLDER = "database"
DATABASE ="toudou.db"
TABLE_NAME = "TOUDOU"

@dataclass
class Todo:
    task: str
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    date: datetime.date = None
    completed: bool = False

    @staticmethod
    def getToudou(id: uuid):
        engine, metadata, toudou = initConn()
        try:
            stmt = select(toudou).where(toudou.c.id == id)
            with engine.connect() as conn:
                result = conn.execute(stmt)
            return result.fetchone()
        except StatementError as e:
            print("Selection error : ", e)

    @staticmethod
    def getToudous():
       engine, metadata, toudou = initConn()
       try:
        stmt = select(toudou)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        toudous = []
        for toudou in  result.fetchall():
            id, task, date, completed = toudou
            todo = Todo(id=id, task=task, date=date, completed=completed)
            toudous.append(todo)
        return toudous
       except StatementError as e:
           print("Selection error : ", e)

    def __str__(self):
        if self.completed:
            return f"Toudou {self.task} has been completed"
        elif not self.completed and self.date:
            return f"Toudou {self.task} has to be completed before {self.date.strftime('%d/%m/%Y')}"
        else:
            return f"Toudou {self.task} has not been completed"


def complete_task(id: uuid):
    engine, metadata, toudou = initConn()
    try:
        stmt = update(toudou).where(toudou.c.id == id).values(completed=True)
        with engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount == 1
    except ArgumentError as e:
        print("An error occured while updating the datas : ", e)


def create_todo(task: str, due: datetime):
    engine, metadata, toudou = initConn()
    try:
        ins = toudou.insert().values(task = task, date = due, completed = False)
        with engine.begin() as conn:
            result = conn.execute(ins)
        return result.rowcount == 1
    except OperationalError as e:
        print("An error occured while inserting datas : ", e)

def createTable():
    engine, metadata_obj, toudou = initConn()
    makedirs(TODO_FOLDER, exist_ok=True)
    
    inspector = inspect(engine)
    if not inspector.has_table(DATABASE): 
        metadata_obj.create_all(engine)

def delete_task(id: uuid):
    engine, metadata, toudou = initConn()
    try:
        stmt = delete(toudou).where(toudou.c.id == id)
        with engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount == 1
    except OperationalError as e:
        print("An error occured while deleting datas : ", e)


def initConn():
    engine = create_engine(f"sqlite:///{TODO_FOLDER}/{DATABASE}", echo=False)
    metadata_obj = MetaData()

    toudouTable = Table(
        TABLE_NAME,
        metadata_obj,
        Column("id", Uuid, primary_key=True, default=uuid.uuid4()),
        Column("task", String, nullable=False),
        Column("date", DateTime, nullable=True),
        Column("completed", Boolean, nullable=False)
    )
    return engine,metadata_obj,toudouTable 
