""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from flask import Blueprint, request, jsonify, current_app, Response
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from projects.projects import app_projects # Blueprint directory import projects definition
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv('Housing.csv')
dataList = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating',
            'airconditioning', 'parking', 'prefarea', 'furnishingstatus']
labelencoder = LabelEncoder()
X = df.drop(columns=['price'])
y = df['price']
regressor = RandomForestRegressor(n_estimators=10, random_state=42)
regressor.fit(X, y)

for i in dataList:
    df[i] = labelencoder.fit_transform(df[i])
class House():
    def __init__(self, area, bedrooms, bathrooms, stories, parking, mainroad, guestroom, basement, hotwaterheating, airconditioning, prefarea, furnishingstatus):
        self._area = area
        self._bedrooms = bedrooms
        self._bathrooms = bathrooms
        self._stories = stories
        self._parking = parking
        self._mainroad = mainroad
        self._guestroom = guestroom
        self._basement = basement
        self._hotwaterheating = hotwaterheating
        self._airconditioning = airconditioning
        self._prefarea = prefarea
        self._furnishingstatus = furnishingstatus

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        self._area = value

    @property
    def bedrooms(self):
        return self._bedrooms

    @bedrooms.setter
    def bedrooms(self, value):
        self._bedrooms = value

    @property
    def bathrooms(self):
        return self._bathrooms

    @bathrooms.setter
    def bathrooms(self, value):
        self._bathrooms = value

    @property
    def stories(self):
        return self._stories

    @stories.setter
    def stories(self, value):
        self._stories = value

    @property
    def parking(self):
        return self._parking

    @parking.setter
    def parking(self, value):
        self._parking = value

    @property
    def mainroad(self):
        return self._mainroad

    @mainroad.setter
    def mainroad(self, value):
        self._mainroad = value

    @property
    def guestroom(self):
        return self._guestroom

    @guestroom.setter
    def guestroom(self, value):
        self._guestroom = value

    @property
    def basement(self):
        return self._basement

    @basement.setter
    def basement(self, value):
        self._basement = value

    @property
    def hotwaterheating(self):
        return self._hotwaterheating

    @hotwaterheating.setter
    def hotwaterheating(self, value):
        self._hotwaterheating = value

    @property
    def airconditioning(self):
        return self._airconditioning

    @airconditioning.setter
    def airconditioning(self, value):
        self._airconditioning = value

    @property
    def prefarea(self):
        return self._prefarea

    @prefarea.setter
    def prefarea(self, value):
        self._prefarea = value

    @property
    def furnishingstatus(self):
        return self._furnishingstatus

    @furnishingstatus.setter
    def furnishingstatus(self, value):
        self._furnishingstatus = value

    def predict(self):
        stringToInt(self._mainroad)
        stringToInt(self._guestroom)
        stringToInt(self._basement)
        stringToInt(self._hotwaterheating)
        stringToInt(self._airconditioning)
        stringToInt(self._prefarea)
        stringToInt(self._area)
        stringToInt(self._bedrooms)
        stringToInt(self._bathrooms)
        stringToInt(self._stories)
        stringToInt(self._parking)

        # Mapping furnishing status to numeric values
        furnishingstatus_map = {'furnished': 0, 'semi-furnished': 2, 'unfurnished': 2}
        self._furnishingstatus = furnishingstatus_map.get(self.furnishingstatus.lower(), -1)  # Default value if not found

        varList.append(self._furnishingstatus)
        print(varList)
        if self.furnishingstatus == -1:
            print("Invalid furnishing status. Please enter 'furnished', 'semi-furnished', or 'unfurnished'.")
        else:
            # Reset regressor
            regressor = RandomForestRegressor(n_estimators=10, random_state=42)
            regressor.fit(X, y)

            # Predicting the price
            predicted_price = regressor.predict([varList])[0]
            return predicted_price
        
varList = []
def stringToInt(var):
    if var == 'yes':
        var = 1
    elif var == 'no':
        var = 0
    else: 
        var = int(var)
    varList.append(var)
    print(var)


"""Database Creation and Testing """

            