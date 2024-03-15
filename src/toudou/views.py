from datetime import datetime
import io
import uuid
from toudou import logging
import click
from flask import Blueprint, Flask, abort, jsonify, render_template, request, url_for, redirect, flash, Response

import toudou.services as services
import toudou.models as models

web_ui = Blueprint("web_ui", __name__, url_prefix="/")

@web_ui.before_request
def before():
    models.createTable()

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
    toudou = models.Todo.getToudou(id)
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
        toudous = models.Todo.getToudous()
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


@web_ui.route('/')
def welcome():
    return render_template('welcome.html')

@web_ui.route('/modify', methods= ['POST', 'GET'])
def modify():
    error = None
    if request.method == 'POST':
        try:
            id = request.form['id']
            task = request.form['tname']
            if request.form['complete'] == "False": complete = ""
            else: complete = request.form['complete']
            due = request.form['due']
        except Exception as e:
            error = e
            abort(500, error)
        try:
            due = None if due == "" else datetime.strptime(due, '%Y-%m-%d')
        except ValueError as e:
            error = e
            abort(500, error)
        if task != "":
            todo = models.update_todo(uuid.UUID(id), task, bool(complete), due)
            if todo:
                flash("Your toudou has been modified successfully")
                return redirect(url_for('web_ui.display'))
            else:
                error = "An error has occured"
                abort(500, error)
    else:
        return render_template('formModify.html', toudous = models.Todo.getToudous())


@web_ui.route('/create', methods= ['POST', 'GET'])
def create():
    error = None
    if request.method == 'POST':
        try:
            task = request.form['tname']
            due = request.form['due']
        except Exception as e:
            error = e
            abort(500, error)
        try:
            due = None if due == "" else datetime.strptime(due, '%Y-%m-%d')
        except ValueError as e:
            error = e
            abort(500, error)
        if task != "":
            todo = models.create_todo(task, due, False)
            if todo:
                flash("Your toudou has been created successfully")
                return redirect(url_for('web_ui.display'))
            else:
                error = "An error has occured"
                abort(500, error)
    else:
        return render_template('formCreation.html')

@web_ui.route('/delete', methods= ['POST', 'GET'])
def delete():
    error = None
    if request.method == 'POST':
        try:
            id = request.form['id']
        except Exception as e:
            error = e
            abort(500, error)
        if id != "":
            try:
                todo = models.delete_task(uuid.UUID(id))
            except ValueError as e:
                error = e
                abort(500, error)
            if todo:
                flash("Your toudou has been deleted successfully")
                return redirect(url_for('web_ui.display'))
            else:
                error = "An error has occured"
                abort(500, error)
    else:
        return render_template("formDelete.html", toudous = models.Todo.getToudous())
    
@web_ui.route('/complete', methods= ['POST', 'GET'])
def complete():
    error = None
    if request.method == 'POST':
        try:
            id = request.form['id']
        except Exception as e:
            error = e
            abort(500, error)
        if id != "":
            try:
                todo = models.complete_task(uuid.UUID(id))
            except ValueError as e:
                error = e
                abort(500, error)
            if todo:
                flash("Your toudou has been deleted successfully")
                return redirect(url_for('web_ui.welcome'))
            else:
                error = "An error has occured"
                abort(500, error)
    else:
        return render_template("formComplete.html", toudous = models.Todo.getNotCompletedToudous())

@web_ui.route('/display')
def display():
    todos = models.Todo.getToudous()
    if todos == None : todos = []
    return render_template('display.html', todos = todos)
    

@web_ui.route('/download')
def download():
    csv_data = services.get_string_csv()
    response = Response(csv_data, content_type='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=toudous.csv"
    return response

@web_ui.route('/upload', methods= ['POST', 'GET'])
def upload():
    error = None
    if request.method == "POST":
        try:
            file = request.files['file']
        except Exception as e:
            error = e
            abort(500, error) 
        if file:
            services.import_from_csv(io.StringIO(file.stream.read().decode("UTF8")))
            return redirect(url_for('web_ui.display'))
        else:
            return redirect(url_for('web_ui.welcome'))
    else:
        return render_template('upload.html')
    

@web_ui.errorhandler(500)
def handle_internal_error(error : Exception):
    flash(str(error))
    logging.exception(str(error))
    return redirect(url_for("web_ui.welcome"))