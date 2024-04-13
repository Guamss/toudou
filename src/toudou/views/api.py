import io
from pydantic import Field, ValidationError, validator
from flask_httpauth import HTTPTokenAuth
from spectree import SecurityScheme, SpecTree
from toudou import services
import toudou.models as models
from flask import Blueprint, request, send_file
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic.v1 import BaseModel, constr
from flask import jsonify
import datetime
import uuid

api_spec = FlaskPydanticSpec('flask')
auth = HTTPTokenAuth(scheme='Bearer')
api = Blueprint("api", __name__, url_prefix="/api")
spec = SpecTree("flask", annotations=True)
spec.register(api)

spec = SpecTree(
    "flask",
    security_schemes=[
        SecurityScheme(
            name="bearer_token",
            data={"type": "http", "scheme": "bearer"}
        )
    ],
    security=[{"bearer_token": []}]
)
    
#TODO import

class CreateToudouApi(BaseModel):
    task: constr(min_length=2, max_length=100)
    due: datetime.date | None = None
"""    @validator('date', pre=True, always=True)
    def parse_date(cls, value):
        if value is not None:
            if isinstance(value, str):
                try:
                    return datetime.strptime(value, FORMAT).date()
                except ValueError:
                    raise ValueError("Format de date invalide. Utilisez le format {}".format(FORMAT))
            elif not isinstance(value, date):
                raise ValueError("La valeur de date doit être une chaîne ou un objet date valide.")
        return value"""

class ModifyToudouApi(BaseModel):
    id: uuid.UUID
    new_task: constr(min_length=2, max_length=100)
    new_due: datetime.date | None = None
    new_completed : bool = Field(default=False)

class GetToudouApi(BaseModel):
    id: uuid.UUID

@api.route('download_toudous', methods=['GET'])
def download_toudous_api():
    csv = services.export_to_csv()
    content_bytes = csv.getvalue().encode()
    bytes_io = io.BytesIO(content_bytes)
    return send_file(bytes_io, as_attachment=True, mimetype='application/octet-stream', download_name="toudous.csv")

@api.route('/get_toudous', methods=['GET'])
def get_todos_api():
    todos = models.getToudous()
    todo_dict_list = [None for i in range(len(todos))]
    for i in range(len(todos)):
        todo_dict = {
                        "id" : todos[i].id, 
                        "date" : todos[i].date, 
                        "task" : todos[i].task, 
                        "completeted" : todos[i].completed
                     }
        todo_dict_list[i] = todo_dict
    return jsonify(todo_dict_list)

@api.route('/get_toudou', methods=['POST'])
@api_spec.validate(body=Request(GetToudouApi))
def get_toudou_api():
    data = GetToudouApi(**request.json)
    try:
        todo = models.getToudou(data.id)
        if todo:
            return {
                    'id' : todo.id,
                    'date' : todo.date,
                    'task' : todo.task,
                    'completed' : todo.completed
                }
        return {'found' : False}
    except ValidationError as e:
        return {'error' : e.errors()}

@api.route('/create_toudou', methods=['POST'])
@auth.login_required
@api_spec.validate(body=Request(CreateToudouApi))
def create_toudou_api():
    try:
        data = CreateToudouApi(**request.json)
        task = data.task
        due = data.due
        models.create_todo(task=task, due=due, completed=False)
        return {'task': task, 'due': due}
    except ValidationError as e:
        return {'error': e.errors()}
    
@api.route('/delete_toudou', methods=['POST'])
@api_spec.validate(body=Request(GetToudouApi))
def delete_toudou_api():
    data = GetToudouApi(**request.json)
    try:
        isDeleted = models.delete_task(data.id)
        return {'deleted' : isDeleted}
    except ValidationError as e:
        return {'error' : e.errors()}
    
@api.route('/complete_toudou', methods=['POST'])
@api_spec.validate(body=Request(GetToudouApi))
def complete_toudou_api():
    data = GetToudouApi(**request.json)
    try:
        isCompleted = models.complete_task(data.id)
        return {'completed' : isCompleted}
    except ValidationError as e:
        return {'error': e.errors()}
    
@api.route('/modify_toudou', methods=['POST'])
@api_spec.validate(body=Request(ModifyToudouApi))
def modify_toudou_api():
    data = ModifyToudouApi(**request.json)
    try:
        modified = models.update_todo(id=data.id, task=data.new_task, complete=data.new_completed, due=data.new_due)
        if modified:
            return {
                    'id' : data.id,
                    'new_due' : data.new_due,
                    'new_task' : data.new_task,
                    'new_completed' : data.new_completed
                   }
        else:
            return {'found' : False}
    except ValidationError as e:
        return {'error' : e.errors()}