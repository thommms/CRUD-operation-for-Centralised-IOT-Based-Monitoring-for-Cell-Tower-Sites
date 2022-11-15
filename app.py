from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
import marshmallow as mm
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import logging as logger
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/cellMonitorDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql9565036:TijEKrD4Bl@sql9.freemysqlhosting.net:3306/sql9565036'
db = SQLAlchemy(app)

#===========================cell site info==============================
# Model
class CellSiteInfo(db.Model):
    __tablename__ = "Cell_Site_info"
    Site_id = db.Column(db.Integer, primary_key=True)
    Site_name = db.Column(db.String(30))
    Site_location = db.Column(db.String(30))
    Country = db.Column(db.String(30))
    State = db.Column(db.String(30))
    Team_name = db.Column(db.String(30))
    Telecom_owner = db.Column(db.String(30))
    Status = db.Column(db.String(30))
    Created_at = db.Column(db.String(30))
    Updated_at = db.Column(db.String(30))

    def to_json(self):
        return {
            'Site_id': self.Site_id,
            'Site_name': self.Site_name,
            'Site_location': self.Site_location,
            'Country': self.Country,
            'State': self.State,
            'Team_name': self.Team_name,
            'Telecom_owner': self.Telecom_owner,
            'Status':self.Status,
            'Created_at': self.Created_at,
            'Updated_at': self.Updated_at
        }
db.create_all()

class CellSiteInfoSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = CellSiteInfo
        sqla_session = db.session

    Site_id = fields.Number(dump_only=True)
    Site_name = fields.String(required=True)
    Site_location = fields.String(required=True)
    Country = fields.String(required=True)
    State = fields.String(required=True)
    Team_name = fields.String(required=True)
    Country = fields.String(required=True)
    Telecom_owner = fields.String(required=True)
    Status = fields.String(required=True)
    Created_at = fields.String(required=True)
    Updated_at = fields.String(required=True)


@app.route('/api/v1/cellSite', methods=['GET'])
def index_cellSite():
    get_cellSites = CellSiteInfo.query.all()
    cellSite_schema = CellSiteInfoSchema(many=True)
    cellSites = cellSite_schema.dump(get_cellSites)
    return make_response(jsonify({"cellSites": cellSites}))

@app.route('/api/v1/cellSite/<Site_id>', methods=['GET'])
def get_cellSite_by_Site_id(Site_id):
    get_cellSite = CellSiteInfo.query.get(Site_id)
    cellSite_schema = CellSiteInfoSchema()
    cellSite = cellSite_schema.dump(get_cellSite)
    return make_response(jsonify({"cellSite": cellSite}))

@app.route('/api/v1/cellSite/<Site_id>', methods=['PUT'])
def update_cellSite_by_Site_id(Site_id):
    data = request.get_json()
    get_cellSite = CellSiteInfo.query.get(Site_id)
    # if data.get('Site_id'):
    #     get_cellSite.Site_id = data['Site_id']
    if data.get('Site_name'):
        get_cellSite.Site_name = data['Site_name']
    if data.get('Site_location'):
        get_cellSite.Site_location = data['Site_location']
    if data.get('Country'):
        get_cellSite.Country = data['Country']
    if data.get('State'):
        get_cellSite.State = data['State']
    if data.get('Team_name'):
        get_cellSite.Team_name = data['Team_name']
    if data.get('Telecom_owner'):
        get_cellSite.Telecom_owner = data['Telecom_owner']
    if data.get('Status'):
        get_cellSite.Status = data['Status']
    if data.get('Created_at'):
        get_cellSite.Created_at = data['Created_at']
    if data.get('Updated_at'):
        get_cellSite.Updated_at = data['Updated_at']
    db.session.add(get_cellSite)
    db.session.commit()
    cellSite_schema = CellSiteInfoSchema(only=['Site_id', 'Site_name', 'Site_location','Country','State','Team_name','Telecom_owner','Status', 'Created_at', 'Updated_at'])
    cellSite = cellSite_schema.dump(get_cellSite)
    return make_response(jsonify({"cellSite": cellSite}))


@app.route('/api/v1/cellSite/<Site_id>', methods=['DELETE'])
def delete_cellSite_by_Site_id(Site_id):
    get_cellSite = CellSiteInfo.query.get(Site_id)
    db.session.delete(get_cellSite)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/cellSite', methods=['POST'])
def create_cellSite():
    data = request.get_json()
    cellSite = CellSiteInfo(
        # Site_id= data['Site_id'],
        Site_name=data['Site_name'],
        Site_location= data['Site_location'],
        Country=data['Country'],
        State= data['State'],
        Team_name=data['Team_name'],
        Telecom_owner= data['Telecom_owner'],
        Status=data['Status'],
        Created_at= data['Created_at'],
        Updated_at=data['Updated_at']
    )
    db.session.add(cellSite)
    db.session.commit()
    result = cellSite.to_json()
    return make_response(jsonify(result),200)

#========================Historical Tag Data==============================

# Model
class HistoricalData(db.Model):
    __tablename__ = "Historical_Tag_Data"
    gu_id = db.Column(db.String(200), primary_key=True)
    Site_id = db.Column(db.Integer)
    Temperature = db.Column(db.String(30))
    Humidity = db.Column(db.String(30))
    Battery_charge = db.Column(db.String(30))
    Input_voltage = db.Column(db.String(30))
    Diesel_level = db.Column(db.String(30))
    Intrusion = db.Column(db.String(30))
    Timestamp = db.Column(db.DateTime, index=True)
    Created_at = db.Column(db.String(30))
    Updated_at = db.Column(db.String(30))

    def to_json(self):
        return {
            'gu_id': self.gu_id,
            'Site_id': self.Site_id,
            'Temperature': self.Temperature,
            'Humidity': self.Humidity,
            'Battery_charge': self.Battery_charge,
            'Input_voltage': self.Input_voltage,
            'Diesel_level': self.Diesel_level,
            'Intrusion': self.Intrusion,
            'Timestamp':self.Timestamp,
            'Created_at': self.Created_at,
            'Updated_at': self.Updated_at
        }
db.create_all()

class HistoricalDataSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = HistoricalData
        sqla_session = db.session
    
    gu_id = fields.String(required=True)
    Site_id = fields.Number(dump_only=True)
    Temperature = fields.String(required=True)
    Humidity = fields.String(required=True)
    Battery_charge = fields.String(required=True)
    Input_voltage = fields.String(required=True)
    Diesel_level = fields.String(required=True)
    Intrusion = fields.String(required=True)
    Timestamp = fields.DateTime(required=True)
    Created_at = fields.String(required=True)
    Updated_at = fields.String(required=True)

@app.route('/api/v1/historicalData', methods=['GET'])
def index_historicalData():
    get_historicalData = HistoricalData.query.all()
    historicalData_schema = HistoricalDataSchema(many=True)
    historicalData = historicalData_schema.dump(get_historicalData)
    return make_response(jsonify({"historicalData": historicalData}))

@app.route('/api/v1/historicalData/<gu_id>', methods=['GET'])
def get_historicalData_by_gu_id(gu_id):
    get_historicalData = HistoricalData.query.get(gu_id)
    historicalData_schema = HistoricalDataSchema()
    historicalData = historicalData_schema.dump(get_historicalData)
    return make_response(jsonify({"historicalData": historicalData}))

@app.route('/api/v1/historicalData/<gu_id>', methods=['PUT'])
def update_historicalData_by_gu_id(gu_id):
    data = request.get_json()
    get_historicalData = HistoricalData.query.get(gu_id)
    if data.get('Site_id'):
        get_historicalData.Site_id = data['Site_id']
    if data.get('Temperature'):
        get_historicalData.Temperature = data['Temperature']
    if data.get('Humidity'):
        get_historicalData.Humidity = data['Humidity']
    if data.get('Battery_charge'):
        get_historicalData.Battery_charge = data['Battery_charge']
    if data.get('Input_voltage'):
        get_historicalData.Input_voltage = data['Input_voltage']
    if data.get('Diesel_level'):
        get_historicalData.Diesel_level = data['Diesel_level']
    if data.get('Intrusion'):
        get_historicalData.Intrusion = data['Intrusion']
    if data.get('Timestamp'):
        get_historicalData.Timestamp = data['Timestamp']
    if data.get('Created_at'):
        get_historicalData.Created_at = data['Created_at']
    if data.get('Updated_at'):
        get_historicalData.Updated_at = data['Updated_at']
    db.session.add(get_historicalData)
    db.session.commit()
    historicalData_schema = HistoricalDataSchema(only=['gu_id','Site_id', 'Temperature', 'Humidity','Battery_charge','Input_voltage','Diesel_level','Intrusion','Timestamp', 'Created_at', 'Updated_at'])
    historicalData = historicalData_schema.dump(get_historicalData)
    return make_response(jsonify({"historicalData": historicalData}))

@app.route('/api/v1/historicalData/<gu_id>', methods=['DELETE'])
def delete_historicalData_by_gu_id(gu_id):
    get_historicalData = HistoricalData.query.get(gu_id)
    db.session.delete(get_historicalData)
    db.session.commit()
    return make_response("", 204)

@app.route('/api/v1/historicalData', methods=['POST'])
def create_historicalData():
    data = request.get_json()
    historicalData = HistoricalData(
        Site_id= data['Site_id'],
        Temperature=data['Temperature'],
        Humidity= data['Humidity'],
        Battery_charge=data['Battery_charge'],
        Input_voltage= data['Input_voltage'],
        Diesel_level=data['Diesel_level'],
        Intrusion= data['Intrusion'],
        Timestamp=data['Timestamp'],
        Created_at= data['Created_at'],
        Updated_at=data['Updated_at']
    )
    db.session.add(historicalData)
    db.session.commit()
    result = historicalData.to_json()
    return make_response(jsonify(result),200)

@app.route('/api/v1/getReports',methods= ['GET'])
def generate_report():
    info = request.get_json()
    site_id=info['Site_id']
    to_date=info['to_date']
    from_date=info['from_date']
    sql = text('select * from Historical_Tag_Data where site_id=%s and Timestamp between "%s" and "%s"'%(site_id,str(from_date),str(to_date)))
    result = db.engine.execute(sql)
    record = {}
    reports =[]
    for data in result:
        record = {
            'site_id':data['site_id'],
            'Temperature':data['Temperature'],
            'Humidity': data['Humidity'],
            'Battery_charge':data['Battery_charge'],
            'Input_voltage': data['Input_voltage'],
            'Diesel_level':data['Diesel_level'],
            'Intrusion': data['Intrusion'],
            'Timestamp':data['Timestamp'],
            'Created_at': data['Created_at'],
            'Updated_at':data['Updated_at']
        }
        reports.append(record)
        record={}

    return make_response(jsonify(reports),200)

#=====================maintenance===============================
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
def index_maintenanceTeam():
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

#==========================User============================
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
def index_user():
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

