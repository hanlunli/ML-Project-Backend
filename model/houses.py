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


def stringToInt(list, index):
    # print(string, string)
    if list[index] == 'no':
        list[index] = 0
    else:
        list[index] = 1
class House():
    
    def predict(data):
        area = '';bedrooms = '';bathrooms = '';stories = '';parking = '';mainroad = '';guestroom = '';basement = ''; hotwaterheating='';airconditioning='';prefarea='';furnishingstatus=''
        df = pd.read_csv('Housing.csv')
        dataList = ['area','bedrooms','bathrooms','stories','mainroad','guestroom','basement','hotwaterheating','airconditioning','parking','prefarea','furnishingstatus']
        labelencoder = LabelEncoder()
        for i in dataList:
            df[i] = labelencoder.fit_transform(df[i])

        X = df.drop(columns=['price'])
        y = df['price']

        varList = [area,bedrooms,bathrooms,stories,mainroad,guestroom,basement,hotwaterheating,airconditioning,parking,prefarea,furnishingstatus]
        regressor = RandomForestRegressor(n_estimators=10, random_state=42)
        regressor.fit(X, y)

        for i in range(len(varList)):
            varList[i] = data.get(dataList[i])
        stringToInt(varList,4);stringToInt(varList,5);stringToInt(varList,6);stringToInt(varList,7);stringToInt(varList,8);stringToInt(varList,10);

        # Mapping furnishing status to numeric values
        furnishingstatus_map = {'furnished': 0, 'semi-furnished': 2, 'unfurnished': 2}
        varList[11] = furnishingstatus_map.get(varList[11].lower(), -1)  # Default value if not found
        print(varList)

        for i in range(len(varList)):
            varList[i] = int(varList[i])
        print(varList, 'after')

        if furnishingstatus == -1:
            print("Invalid furnishing status. Please enter 'furnished', 'semi-furnished', or 'unfurnished'.")
        else:
            # Predicting the price
            predicted_price = regressor.predict([[i for i in varList]])[0]
            return predicted_price


"""Database Creation and Testing """

            