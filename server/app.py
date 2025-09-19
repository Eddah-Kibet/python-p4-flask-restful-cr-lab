#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_serialized = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plants_serialized), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByID(Resource):
    def get(self, plant_id):
        plant = db.session.get(Plant, plant_id)
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response(jsonify({"error": "Plant not found"}), 404)

api.add_resource(PlantByID, '/plants/<int:plant_id>')
api.add_resource(Plants, '/plants')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
