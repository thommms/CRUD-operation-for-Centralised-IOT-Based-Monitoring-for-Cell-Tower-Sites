from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
import marshmallow as mm
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import logging as logger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql9565036:TijEKrD4Bl@sql9.freemysqlhosting.net:3306/sql9565036'
db = SQLAlchemy(app)

# Model
class User(db.Model):
    __tablename__ = "User"
    Username = db.Column(db.String(20), primary_key=True)
    Password = db.Column(db.String(100))
    Fullname = db.Column(db.String(100))
    Designation = db.Column(db.String(100))
    Created_at = db.Column(db.String(100))
    Updated_at = db.Column(db.String(100))

    def to_json(self):
        return {
            'Username': self.Username,
            'Password': self.Password,
            'Fullname': self.Fullname,
            'Designation': self.Designation,
            'Created_at': self.Created_at,
            'Updated_at': self.Updated_at
        }
db.create_all()

class UserSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = User
        sqla_session = db.session

    Username = fields.String(required=True)
    Password = fields.String(required=True)
    Fullname = fields.String(required=True)
    Designation = fields.String(required=True)
    Created_at = fields.String(required=True)
    Updated_at = fields.String(required=True)


@app.route('/api/v1/user', methods=['GET'])
def index():
    get_users = User.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


@app.route('/api/v1/user/<username>', methods=['GET'])
def get_user_by_username(username):
    get_user = User.query.get(username)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/api/v1/user/<username>', methods=['PUT'])
def update_user_by_username(username):
    data = request.get_json()
    get_user = User.query.get(username)
    if data.get('Username'):
        get_user.Username = data['Username']
    if data.get('Password'):
        get_user.Password = data['Password']
    if data.get('Fullname'):
        get_user.Fullname = data['Fullname']
    if data.get('Designation'):
        get_user.Designation = data['Designation']
    if data.get('Created_at'):
        get_user.Created_at = data['Created_at']
    if data.get('Updated_at'):
        get_user.Updated_at = data['Updated_at']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema(only=['Username', 'Password', 'Fullname','Designation', 'Created_at', 'Updated_at'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/api/v1/user/<username>', methods=['DELETE'])
def delete_user_by_username(username):
    get_user = User.query.get(username)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        Username= data['Username'],
        Password=data['Password'],
        Fullname= data['Fullname'],
        Designation=data['Designation'],
        Created_at= data['Created_at'],
        Updated_at=data['Updated_at']
    )
    db.session.add(user)
    db.session.commit()
    result = user.to_json()
    return make_response(jsonify(result),200)
if __name__ == "__main__":
    app.run(debug=True)

