from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
import marshmallow as mm
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/cellMonitorDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql9565036:TijEKrD4Bl@sql9.freemysqlhosting.net:3306/sql9565036'
db = SQLAlchemy(app)

# Model
class HistoricalData(db.Model):
    __tablename__ = "Historical_Tag_Data"
    gu_id = db.Column(db.Integer, primary_key=True)
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
    
    gu_id = fields.Number(dump_only=True)
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
def index():
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

if __name__ == "__main__":
    app.run(debug=True)
