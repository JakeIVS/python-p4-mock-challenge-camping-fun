#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        camper_list = []
        for camper in Camper.query.all():
            camper.serialize_rules=('-signups',)
            camper_list.append(camper.to_dict())
        return make_response(camper_list, 200)

class Camper_id(Resource):
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first()
        if camper:
            return make_response(camper.to_dict(), 200)
        else:
            return make_response({'error':'Camper not found'}, 400)
    def patch(self,id):
        camper = Camper.query.filter(Camper.id == id).first()
        if camper:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(camper, attr, data[attr])
                db.session.add(camper)
                db.session.commit()
                return make_response(camper.to_dict(), 202)
            except:
                return make_response({'error':['validation errors']})
        else: #camper does not exist
            return make_response({'error':'Camper not found'})

        
api.add_resource(Campers, '/campers')
api.add_resource(Camper_id, '/campers/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
