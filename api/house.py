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
            print('wtf bro')
            return jsonify(House.predict(request.get_json()))

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    