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
def index():
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
if __name__ == "__main__":
    app.run(debug=True)

