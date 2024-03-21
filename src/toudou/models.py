from dataclasses import dataclass, field
from toudou import config, DATABASE, TODO_FOLDER, TABLE_NAME
from sqlalchemy import create_engine, MetaData, Table, UUID, Column, String, Boolean, DateTime, select, update, delete, inspect
from sqlalchemy.exc import OperationalError, StatementError, ArgumentError
from os import makedirs
import datetime
import uuid

engine = create_engine(config['DATABASE_URL'], echo=config['DEBUG'])
metadata_obj = MetaData()
toudouTable = Table(
    TABLE_NAME,
    metadata_obj,
    Column("id", UUID, primary_key=True, default=uuid.uuid4()),
    Column("task", String, nullable=False),
    Column("date", DateTime, nullable=True),
    Column("completed", Boolean, nullable=False)
)

@dataclass
class Todo:
    """
    Class representing a to-do task.

    Attributes:
        task (str): The description of the task.
        id (uuid.UUID): The unique identifier of the task.
        date (datetime.date): The due date of the task (optional).
        completed (bool): Indicates whether the task is completed or not.
    """
    task: str
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    date: datetime.date = None
    completed: bool = False
            
    def changeDateFormat(self):
        """
        Method to format the task's date in 'day/month/year' format.

        Returns:
            str: The formatted date.
        """
        return self.date.strftime('%d/%m/%Y')
    
    def __str__(self):
        """
        Method to obtain a textual representation of the task.

        Returns:
            str: The textual representation of the task.
        """
        if self.completed:
            return f"Toudou {self.task} has been completed"
        elif not self.completed and self.date:
            return f"Toudou {self.task} has to be completed before {self.date.strftime('%d/%m/%Y')}"
        else:
            return f"Toudou {self.task} has not been completed"


def complete_task(id: uuid):
    """
    Mark a task as completed.

    Args:
        id (uuid.UUID): The unique identifier of the task.

    Returns:
        bool: True if the task has been successfully marked as completed, False otherwise.
    """
    try:
        stmt = update(toudouTable).where(toudouTable.c.id == id).values(completed=True)
        with engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount == 1
    except ArgumentError as e:
        print("An error occurred while updating the data:", e)

def update_todo(id : uuid.UUID, task: str, complete: bool, due: datetime.date):
    try:
        count_rows(id)
    except OperationalError as e:
        print("An error occurred while updating the data:", e)
        return None
    except ValueError as ve:
        print(str(ve))
        return None

    if due:
        smt = update(toudouTable).where(toudouTable.c.id == id).values(task=task,completed=complete, date=due)
    else:
        smt = update(toudouTable).where(toudouTable.c.id == id).values(task=task, completed=complete, date=due)
    with engine.begin() as conn:
        result = conn.execute(smt)
    return result.rowcount == 1
        
def getToudous():
    """
    Retrieve all to-do tasks from the database.

    Returns:
        list: A list of Todo objects representing all to-do tasks.
    """
    try:
        stmt = select(toudouTable)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        toudous = []
        for toudou_row in result.fetchall():
            id, task, date, completed = toudou_row
            todo = Todo(id=id, task=task, date=date, completed=completed)
            toudous.append(todo)
        return toudous
    except StatementError as e:
        print("Selection error: ", e)

def getNotCompletedToudous():
    try:
        stmt = select(toudouTable).where(toudouTable.c.completed == False)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        toudous = []
        for toudou_row in result.fetchall():
            id, task, date, completed = toudou_row
            todo = Todo(id=id, task=task, date=date, completed=completed)
            toudous.append(todo)
        return toudous
    except StatementError as e:
        print("Selection error: ", e)

def getToudou(id: uuid):
    """
    Retrieve a to-do task based on its unique identifier.

    Args:
        id (uuid.UUID): The unique identifier of the task to retrieve.

    Returns:
        Todo or None: The Todo object corresponding to the found task, or None if no matching task is found.
    """
    try:
        stmt = select(toudouTable).where(toudouTable.c.id == id)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        return result.fetchone()
    except StatementError as e:
        print("Selection error: ", e)

def create_todo(task: str, due: datetime, completed: bool):
    """
    Create a new to-do task.

    Args:
        task (str): The description of the task.
        due (datetime): The due date of the task.

    Returns:
        bool: True if the task has been successfully created, False otherwise.
    """
    try:
        ins = toudouTable.insert().values(task=task, date=due, completed=completed)
        with engine.begin() as conn:
            result = conn.execute(ins)
        return result.rowcount == 1
    except OperationalError as e:
        print("An error occurred while inserting data:", e)

def createTable():
    """
    Create the to-do tasks table in the database if it doesn't already exist.

    The function creates the table using the connection information provided by the initConn() function,
    then checks if the table already exists in the database. If the table doesn't exist, it is created.

    Returns:
        None
    """
    makedirs(TODO_FOLDER, exist_ok=True)
    
    inspector = inspect(engine)
    if not inspector.has_table(DATABASE): 
        metadata_obj.create_all(engine)

def delete_task(id: uuid):
    """
    Delete a to-do task.

    Args:
        id (uuid.UUID): The unique identifier of the task to delete.

    Returns:
        bool: True if the task has been successfully deleted, False otherwise.
    """
    try: 
        stmt = delete(toudouTable).where(toudouTable.c.id == id)
        with engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount == 1
    except OperationalError as e:
        print("An error occurred while deleting data:", e)

def count_rows(id : uuid.UUID) -> int:
    stmt = select(toudouTable).where(toudouTable.c.id == id)
    try:
        with engine.connect() as connection:
            result = connection.execute(stmt)
            rows = result.fetchall()
            if not rows:
                raise ValueError("Unknown ID")
            return len(rows)
    except OperationalError as e:
        raise e
