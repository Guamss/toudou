import io

from toudou import config

import uuid

from flask import Blueprint, abort, render_template, send_file, url_for, redirect, flash
from toudou.views.wtf import DeleteToudouForm, CreateToudouForm, ModifyToudouForm, UploadForm, CompleteToudouForm

from toudou.views.app import auth, get_user_roles
import toudou.services as services
import toudou.models as models

web_ui = Blueprint("web_ui", __name__, url_prefix="/")

@web_ui.route('/')
@auth.login_required
def welcome():
    return render_template('welcome.html', user = auth.current_user())

@web_ui.route('/modify', methods= ['POST', 'GET'])
@auth.login_required(role="admin")
def modify():
    error = None
    form = ModifyToudouForm()
    form.id.choices = models.convert_to_tuple_list(models.getToudous())
    if form.validate_on_submit():
        try:
            id = form.id.data
            task = form.tname.data
            if form.complete.data == "False": complete = ""
            else: complete = form.complete.data
            due = form.due.data
        except Exception as e:
            error = e
            abort(500, error)
        if task != "":
            todo = models.update_todo(id, task, bool(complete), due)
            if todo:
                flash("Your toudou has been modified successfully")
                return redirect(url_for('web_ui.display'))
            else:
                error = "An error has occured"
                abort(500, error)
    return render_template('formModify.html', form = form)


@web_ui.route('/create', methods= ['POST', 'GET'])
@auth.login_required(role="admin")
def create():
    error = None
    form = CreateToudouForm()
    if form.validate_on_submit():
        try:
            task = form.name.data
            due = form.due.data
        except Exception as e:
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
    return render_template('formCreation.html', form = form)
    
@web_ui.route('/complete', methods= ['POST', 'GET'])
@auth.login_required(role="admin")
def complete():
    error = None
    form = CompleteToudouForm()
    form.id.choices = models.convert_to_tuple_list(models.getNotCompletedToudous())
    if form.validate_on_submit():
        try:
            id = form.id.data
        except Exception as e:
            error = e
            abort(500, error)
        if id != "":
            try:
                todo = models.complete_task(id)
            except ValueError as e:
                error = e
                abort(500, error)
            if todo:
                flash("Your toudou has been completed successfully")
                return redirect(url_for('web_ui.display'))
            else:
                error = "An error has occured"
                abort(500, error)
    else:
        return render_template("formComplete.html", form = form)

@web_ui.route('/display', methods=['GET', 'POST'])
@auth.login_required
def display():
    user = auth.current_user()
    error = None
    form = DeleteToudouForm()
    if form.validate_on_submit() and get_user_roles(user) == ['admin']:
        try:
            id = form.toudou_ID.data
        except Exception as e:
            error = e
            abort(500, error)
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

    todos = models.getToudous()
    if todos == None : todos = []
    return render_template('display.html', todos = todos, form = form)
    

@web_ui.route('/download')
@auth.login_required
def download():
    csv = services.export_to_csv()
    content_bytes = csv.getvalue().encode()
    bytes_io = io.BytesIO(content_bytes)
    return send_file(bytes_io, as_attachment=True, mimetype='application/octet-stream',download_name="toudous.csv")

@web_ui.route('/upload', methods= ['POST', 'GET'])
@auth.login_required(role="admin")
def upload():
    error = None
    form = UploadForm()
    if form.validate_on_submit():
        try:
            file = form.file.data
        except Exception as e:
            error = e
            abort(500, error)
        if file:
            try:
                with file.stream as f:
                    services.import_from_csv(io.TextIOWrapper(f, encoding='utf-8'))
                flash("Your file has been imported successfully")
                return redirect(url_for('web_ui.display'))
            except ValueError as e:
                error = e
                abort(500, error)
        else:
            error = "An error has occured"
            abort(500, error)
        
    return render_template('upload.html', form = form)
    

@web_ui.errorhandler(500)
def handle_internal_error(error : Exception):
    flash(str(error))
    config['LOGGING'].exception(str(error))
    return redirect(url_for("web_ui.welcome"))