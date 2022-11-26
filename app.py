# Set up the Flask Weather App
# Import dependencies for analysis
import datetime as dt
import numpy as np
import pandas as pd

#import dependencies for SQLalchemy for accessing the 
#sqlite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import dependencies to run flask jsonify() is a helper method 
#provided by Flask to properly return JSON data. 
#jsonify() returns a Response object with the application/json mimetype set,
from flask import Flask, jsonify


# SET UP DATABASE
# create database engine for Flask application note: is the same code in python
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect database into classes
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# Set class variables: recall in our climate analysis we know
# the two classes were reflected measurement and stations
Measurement = Base.classes.measurement
Station = Base.classes.station
# Creates session link from Python to SQLite database
session = Session(engine)


#SET UP FLASK
# Create Flask app, all routes go after this code
app = Flask(__name__)

#look at module 9.5.1 for explanation on how the 
#commented code is working
# Example of app name variable
# import app
# print("example __name__ = %s", __name__)
# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")

# creating the flask route by defining our welcome route 
#to be the root IMPORTANT: all roots go after app = Flask(__name__)
@app.route("/")
#create a function welcome with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''') 
#note: follow the naming convetnion /api/v1.0/ followed by
#the name of the route. this convention signifies that this 
#is version 1 of our application. this line can be updated 
#to support future versions of the app as well. 

# 9.5.2 says to use flask run

# 9.5.3 Precipitation Route
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# check website changes, (http://127.0.0.1:5000/), should be block of dates

# 9.5.4 Stations Route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# check website changes, (http://localhost:5000/), stations with USC0051xxxx codes

#9.5.5 Monthly Temperature Route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#do flask run, (http://localhost:5000/), block of temps (F)

#9.5.6 Statistic Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# flask run
# After running this code, you'll be able to copy and paste the web address provided by Flask into a web browser. 
# Open /api/v1.0/temp/start/end route and check to make sure you get the correct result, which is
# [null,null,null]
# You would add the following path to the address in your web browser:
# /api/v1.0/temp/2017-06-01/2017-06-30
# should return 
# ["temps":[71.0,77.21989528795811,83.0]]

# from tech help
# if __name__ == '__main__':
#     app.run()