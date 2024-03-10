from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)
api = Api(app)

TODOS = {
  '1': {'task': 'task1'},
  '2': {'task': 'task2'},
  '3': {'task': 'task3'},
  '4': {'task': 'task4'},
  '5': {'task': 'task5'},
}

def abort_todo(todo_id):
  if todo_id not in TODOS:
    abort(404, message=f"id: {todo_id} doesn't exist")

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
  def get(self, todo_id):
    abort_todo(todo_id)
    return TODOS[todo_id]

  def put(self, todo_id):
    args = parser.parse_args()
    task = {'task': args['task']}

    TODOS[todo_id] = task
    return task, 201

  def delete(self, todo_id):
    abort_todo(todo_id)
    del TODOS[todo_id]
    return '', 204


class TodoList(Resource):
  def get(self):
    return TODOS

  def post(self):
    args = parser.parse_args()
    todo_id = int(max(TODOS.keys())) + 1
    TODOS[todo_id] = {'task': args['task']}
    return TODOS[todo_id], 201

api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(TodoList, '/todos')


if __name__ == '__main__':
  app.run()

