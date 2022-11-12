from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
import marshmallow as mm
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import logging as logger

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/cellMonitorDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql9565036:TijEKrD4Bl@sql9.freemysqlhosting.net:3306/sql9565036'
db = SQLAlchemy(app)

# Model
class Maintenance_Team(db.Model):
    __tablename__ = "Maintenance_Team"
    Team_name = db.Column(db.String(20), primary_key=True)
    Team_leader = db.Column(db.String(100))
    Phone_number = db.Column(db.String(100))
    County = db.Column(db.String(100))
    State = db.Column(db.String(100))
    Created_at = db.Column(db.String(100))
    Updated_at = db.Column(db.String(100))


    def to_json(self):
        return {
            'Team_name': self.Team_name,
            'Team_leader': self.Team_leader,
            'Phone_number': self.Phone_number,
            'County': self.County,
            'State':self.State,
            'Created_at': self.Created_at,
            'Updated_at': self.Updated_at
        }
db.create_all()
#Team_name  Team_leader	Phone_number	County	State	Created_at	Updated_at	

class Maintenance_Team_Schema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Maintenance_Team
        sqla_session = db.session

    Team_name = fields.String(required=True)
    Team_leader = fields.String(required=True)
    Phone_number = fields.String(required=True)
    County = fields.String(required=True)
    State = fields.String(required=True)
    Created_at = fields.String(required=True)
    Updated_at = fields.String(required=True)


@app.route('/api/v1/maintenanceTeam', methods=['GET'])
def index():
    get_maintenanceTeams = Maintenance_Team.query.all()
    maintenanceTeam_schema = Maintenance_Team_Schema(many=True)
    maintenanceTeams = maintenanceTeam_schema.dump(get_maintenanceTeams)
    return make_response(jsonify({"maintenanceTeams": maintenanceTeams}))


@app.route('/api/v1/maintenanceTeam/<Team_name>', methods=['GET'])
def get_maintenanceTeam_by_Team_name(Team_name):
    get_maintenanceTeam = Maintenance_Team.query.get(Team_name)
    maintenanceTeam_schema = Maintenance_Team_Schema()
    maintenanceTeam = maintenanceTeam_schema.dump(get_maintenanceTeam)
    return make_response(jsonify({"maintenanceTeam": maintenanceTeam}))

#Team_name  Team_leader	Phone_number	County	State	Created_at	Updated_at	


@app.route('/api/v1/maintenanceTeam/<Team_name>', methods=['PUT'])
def update_maintenanceTeam_by_Team_name(Team_name):
    data = request.get_json()
    get_maintenanceTeam = Maintenance_Team.query.get(Team_name)
    if data.get('Team_name'):
        get_maintenanceTeam.Team_name = data['Team_name']
    if data.get('Team_leader'):
        get_maintenanceTeam.Team_leader = data['Team_leader']
    if data.get('Phone_number'):
        get_maintenanceTeam.Phone_number = data['Phone_number']
    if data.get('County'):
        get_maintenanceTeam.County = data['County']
    if data.get('State'):
        get_maintenanceTeam.State = data['State']
    if data.get('Created_at'):
        get_maintenanceTeam.Created_at = data['Created_at']
    if data.get('Updated_at'):
        get_maintenanceTeam.Updated_at = data['Updated_at']
    db.session.add(get_maintenanceTeam)
    db.session.commit()
    maintenanceTeam_schema = Maintenance_Team_Schema(only=['Team_name', 'Team_leader', 'Phone_number','County','State', 'Created_at', 'Updated_at'])
    maintenanceTeam = maintenanceTeam_schema.dump(get_maintenanceTeam)
    return make_response(jsonify({"maintenanceTeam": maintenanceTeam}))


@app.route('/api/v1/maintenanceTeam/<Team_name>', methods=['DELETE'])
def delete_maintenanceTeam_by_Team_name(Team_name):
    get_maintenanceTeam = Maintenance_Team.query.get(Team_name)
    db.session.delete(get_maintenanceTeam)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/maintenanceTeam', methods=['POST'])
def create_maintenanceTeam():
    data = request.get_json()
    maintenanceTeam = Maintenance_Team(
        Team_name= data['Team_name'],
        Team_leader=data['Team_leader'],
        Phone_number= data['Phone_number'],
        County=data['County'],
        State = data['State'],
        Created_at= data['Created_at'],
        Updated_at=data['Updated_at']
    )
    db.session.add(maintenanceTeam)
    db.session.commit()
    result = maintenanceTeam.to_json()
    return make_response(jsonify(result),200)
if __name__ == "__main__":
    app.run(debug=True)

