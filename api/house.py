import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.houses import House

house_api = Blueprint('house_api', __name__,
                   url_prefix='/house')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(house_api)

class HouseAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def get(self):
            return jsonify('hi')
        def post(self): # Create method
            varlist = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating',
                    'airconditioning', 'parking', 'prefarea', 'furnishingstatus']
            
            data = request.get_json()
            house = House(data.get('area'), data.get('bedrooms'), data.get('bathrooms'), data.get('stories'), data.get('mainroad'), data.get('guestroom'),
                          data.get('basement'),data.get('hotwaterheating'),data.get('airconditioning'), data.get('parking'), data.get('prefarea'), data.get('furnishingstatus'))
            return house.predict()

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    