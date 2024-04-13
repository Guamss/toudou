from pydantic import Field, ValidationError
from flask_httpauth import HTTPTokenAuth
import toudou.models as models
from flask import Blueprint, request
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic.v1 import BaseModel, constr
from flask import jsonify
import datetime
import uuid

api_spec = FlaskPydanticSpec('flask')
auth = HTTPTokenAuth(scheme='Bearer')
api = Blueprint("api", __name__, url_prefix="/api")

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

#TODO import
#TODO export

class CreateToudouApi(BaseModel):
    task: constr(min_length=2, max_length=100)
    due: datetime.date | None = None

class ModifyToudouApi(BaseModel):
    id: uuid.UUID
    new_task: constr(min_length=2, max_length=100)
    new_due: datetime.date | None = None
    new_completed : bool = Field(default=False)

class GetToudouApi(BaseModel):
    id: uuid.UUID

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

@auth.verify_token
@api.route('/create_toudou', methods=['POST'])
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