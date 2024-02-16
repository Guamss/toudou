from dataclasses import dataclass
import datetime

import sqlite3

import uuid

@dataclass
class Todo:
    id: uuid.UUID
    task: str
    date: datetime.date = None
    completed: bool = False

    @staticmethod
    def getToudou(id: uuid, arg_con : sqlite3.Connection):
        con = arg_con
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM toudou WHERE id = ?", (str(id),))
            result = cur.fetchone()
            cur.close()
            return result
        except sqlite3.Error as e:
            print("Selection error : ", e)

    @staticmethod
    def getToudous(arg_con : sqlite3.Connection):
        con = arg_con
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM  toudou")
            result = cur.fetchall()
            cur.close()
            return result
        except sqlite3.Error as e:
            print("Selection error : ", e)

    def __str__(self):
        if self.completed:
            return f"Toudou {self.task} has been completed"
        elif not self.completed and self.date:
            return f"Toudou {self.task} has to be completed before {self.date.strftime('%d/%m/%Y')}"
        else:
            return f"Toudou {self.task} has not been completed"


def complete_task(id: uuid, arg_con : sqlite3.Connection):
    con = arg_con
    cur = con.cursor()
    try:
        cur.execute("UPDATE toudou SET completed = 1 WHERE id = ?", (str(id),))
        cur.close()
        con.commit()
        return cur.rowcount == 1
    except sqlite3.Error as e:
        print("An error occured while updating the datas : ", e)


def create_todo(task: str, due: datetime, arg_con : sqlite3.Connection):
    con = arg_con
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO toudou (id, task, date, completed) VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), task, due, False))
        cur.close()
        con.commit()
    except sqlite3.Error as e:
        print("An error occured while inserting datas : ", e)

def init_db():
    con = getConn()
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS toudou(
                    id BLOB NOT NULL UNIQUE, 
                    task VARCHAR(500) NOT NULL, 
                    date DATE, 
                    completed BOOLEAN NOT NULL)""")
        cur.close()
    except sqlite3.Error as e:
        print("An error occured while creating the table:", e)

def getConn():
    return sqlite3.connect("toudou.db")
