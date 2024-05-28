import threading
import csv
# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup

import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.houses import House
from model.users import User
# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.house import house_api
# database migrations
from model.users import initUsers
from model.players import initPlayers

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(house_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/nba', methods=["GET"])
def nba():
    def csv_to_dict(csv_file):
        result = {}
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                key = row.pop('Rk')
                processed_row = {}
                for k, v in row.items():
                    try:
                        processed_row[k] = float(v)
                    except ValueError:
                        processed_row[k] = v
                result[key] = processed_row
        return result

    csv_file = 'nba.csv'
    data = csv_to_dict(csv_file)

    def sortfunc():
        tempdict = []
        tempdict.append([data["1"]["Player"],data["1"]['PTS']])
        for i in range(2,len(data)):
            current = [data[f"{i+1}"]["Player"],data[f"{i+1}"]["PTS"]]
            spot = binary_spot_search(current, tempdict)
            tempdict.insert(spot, current)
        end(tempdict)

    def binary_spot_search(value, dict):
        found = False
        unchange = dict
        while not found:
            length = len(dict)
            pos = length//2
            middle = dict[pos]
            if value[1] == middle[1]:
                found = True
                return unchange.index(middle)
            elif value[1] > dict[-1][1]:
                temp = dict[-1]
                temp1 = unchange.index(temp)
                found = True
                return temp1+1
            elif value[1] < dict[0][1]:
                found = True
                return 0
            elif middle[1] < value[1]:
                if len(dict) == 1:
                    found = True
                    return unchange.index(dict[0])
                dict = dict[pos:]
            elif value[1] < middle[1]:
                if len(dict) == 1:
                    found = True
                    return unchange.index(dict[0])+1
                dict = dict[:pos]

    def listflip(list1):
        list2 = []
        for i in range(len(list1)):
            list2.append(list1[-1*(i+1)])
        return list2
    returnlist = []
    def end(dict):
        dict1 = listflip(dict)
        for i in range(len(dict1)):
            returnlist.append([[dict1[i][0]], [dict1[i][1]]])

    sortfunc()
    return json.dumps(returnlist)


@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io']:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8086")