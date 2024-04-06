from pydantic import Field
import toudou.models as models
from flask import Blueprint, request
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic import BaseModel, constr
from flask import jsonify

api_spec = FlaskPydanticSpec('flask')
api = Blueprint("api", __name__, url_prefix="/api")

class Profile(BaseModel):
    name: constr(min_length=2, max_length=40) # type: ignore
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        description='user age(Human)'
    )

@api.route('/truc', methods=['POST'])
@api_spec.validate(body=Request(Profile))
def user_profile():
    print(request.context.body)
    return {'text': 'it works'}

@api.route('/get_todos', methods=['GET'])
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