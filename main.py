import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup

import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User
# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
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
@app.route('/house/', methods=['POST'])
def house():
    df = pd.read_csv('Housing.csv')
    body = request.get_json()
    labelencoder = LabelEncoder()
    df['mainroad'] = labelencoder.fit_transform(df['mainroad'])
    df['guestroom'] = labelencoder.fit_transform(df['guestroom'])
    df['basement'] = labelencoder.fit_transform(df['basement'])
    df['hotwaterheating'] = labelencoder.fit_transform(df['hotwaterheating'])
    df['airconditioning'] = labelencoder.fit_transform(df['airconditioning'])
    df['prefarea'] = labelencoder.fit_transform(df['prefarea'])

    # Assuming 'furnishingstatus' is the target variable
    df['furnishingstatus'] = labelencoder.fit_transform(df['furnishingstatus'])

    # Splitting the dataset into the features and target variable
    X = df.drop(columns=['price'])
    y = df['price']

    # Training the Random Forest Regressor model
    regressor = RandomForestRegressor(n_estimators=10, random_state=42)
    regressor.fit(X, y)

    # Accepting user input for house features
    area = int(body.get('area'))
    bedrooms = int(body.get('bedrooms'))
    bathrooms = int(body.get('bathrooms'))
    stories = int(body.get('stories'))
    mainroad = body.get('mainroad')
    guestroom = body.get('guestroom')
    basement = body.get('basement')
    hotwaterheating = body.get('hotwaterheating')
    airconditioning = body.get('airconditioning')
    parking = body.get('parking')
    prefarea = body.get('prefarea')
    furnishingstatus = body.get('furnishingstatus')

    # Mapping user inputs to numeric values
    mainroad = 1 if mainroad.lower() == 'yes' else 0
    guestroom = 1 if guestroom.lower() == 'yes' else 0
    basement = 1 if basement.lower() == 'yes' else 0
    hotwaterheating = 1 if hotwaterheating.lower() == 'yes' else 0
    airconditioning = 1 if airconditioning.lower() == 'yes' else 0
    prefarea = 1 if prefarea.lower() == 'yes' else 0

    # Mapping furnishing status to numeric values
    furnishingstatus_map = {'furnished': 0, 'semi-furnished': 1, 'unfurnished': 2}
    furnishingstatus = furnishingstatus_map.get(furnishingstatus.lower(), -1)  # Default value if not found

    if furnishingstatus == -1:
        print("Invalid furnishing status. Please enter 'furnished', 'semi-furnished', or 'unfurnished'.")
    else:
        # Predicting the price
        predicted_price = regressor.predict([[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus]])[0]
        return jsonify(predicted_price)
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