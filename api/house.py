import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User

# Load data from CSV file
house_api = Blueprint('house', __name__,
                   url_prefix='/api/house')
df = pd.read_csv('Housing.csv')
api = Api(house_api)

class HouseAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def get(self):
            return jsonify("ajslkfdj")
        def post(self):
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
            area = body.get('area')
            bedrooms = body.get('bedrooms')
            bathrooms = body.get('bathrooms')
            stories = body.get('stories')
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
                return predicted_price

    api.add_resource(_CRUD, '/')