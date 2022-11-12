from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
import marshmallow as mm
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import logging as logger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/todo'
db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    todo_description = db.Column(db.String(100))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'todo_description': self.todo_description
        }

db.create_all()


class TodoSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Todo
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    todo_description = fields.String(required=True)


@app.route('/api/v1/todo', methods=['GET'])
def index():
    get_todos = Todo.query.all()
    todo_schema = TodoSchema(many=True)
    todos = todo_schema.dump(get_todos)
    return make_response(jsonify({"todos": todos}))


@app.route('/api/v1/todo/<id>', methods=['GET'])
def get_todo_by_id(id):
    get_todo = Todo.query.get(id)
    todo_schema = TodoSchema()
    todo = todo_schema.dump(get_todo)
    return make_response(jsonify({"todo": todo}))


@app.route('/api/v1/todo/<id>', methods=['PUT'])
def update_todo_by_id(id):
    data = request.get_json()
    get_todo = Todo.query.get(id)
    if data.get('title'):
        get_todo.title = data['title']
    if data.get('todo_description'):
        get_todo.todo_description = data['todo_description']
    db.session.add(get_todo)
    db.session.commit()
    todo_schema = TodoSchema(only=['id', 'title', 'todo_description'])
    todo = todo_schema.dump(get_todo)
    return make_response(jsonify({"todo": todo}))


@app.route('/api/v1/todo/<id>', methods=['DELETE'])
def delete_todo_by_id(id):
    get_todo = Todo.query.get(id)
    db.session.delete(get_todo)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/todo', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = Todo(
        title= data['title'],
        todo_description=data['todo_description']
    )
    db.session.add(todo)
    db.session.commit()
    result = todo.to_json()
    return make_response(jsonify(result),200)
if __name__ == "__main__":
    app.run(debug=True)

