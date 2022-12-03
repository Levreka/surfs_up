# NOTe: THIS CODE TAKES PLACE AFTER ANALYSIS WHICH MEANS SOME OF THIS
#CODE TAKES INTO CONSIDERATION SOME OF THE FINDINGS OF PREVIOUS ANALYSIS
# 
# 
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

# you can view code up to this point by running flask run in 
#command promp make sure you are in the right folder holding the file


#PRECIPITATION ROUTE BUILD
#CAUTION
#Every time you create a new route, your code should be aligned to 
#the left in order to avoid errors.

#create the app route for precipitation
@app.route("/api/v1.0/precipitation")
#create the precipitation function code will look almost identical 
#to python code minor changes to best intigrated to our apps
def precipitation():
   #code is just like in our climate analysis python file
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #precipitation variable is created to hld the session query only name of variable changes
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   #new line of code not in our climate analysis step 1 create variable name precip
   #step two create a condition 
   precip = {date: prcp for date, prcp in precipitation}
   #return the results of the query
   return jsonify(precip)
# if you want to view this code run the flask in cmd prompt and add the route 
#http://127.0.0.1:5000/api/v1.0/precipitation like so after you put it into browser

# 9.5.4 Stations Route
#As a reminder, this code should occur outside of 
#the previous route and have no indentation. 
#add a new route statations
@app.route("/api/v1.0/stations")
#defined the route function called stations()
def stations():
    #create a variable results that will get all the stations
    results = session.query(Station.station).all()
    #start unraveling our results inot one dimensional arrays by using np.ravel ()
    #with results as our parameters and converting it into a list by
    #using list()
    stations = list(np.ravel(results))
    #convert the list into a json file by using jsnoify
    return jsonify(stations=stations)

    #do flask run/ dont forget to add extension at the end 

#9.5.5 Monthly Temperature Route
#As a reminder, this code should occur outside of 
#the previous route and have no indentation.
#defined a new route called tobs
@app.route("/api/v1.0/tobs")
#create function named monthly()
def temp_monthly():
    #calculate the date one eyar ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #create a results variable that will query query the primary station 'USC00519281'
    #for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    #start unraveling our results inot one dimensional arrays by using np.ravel ()
    #with results as our parameters and converting it into a list by
    #using list() 
    temps = list(np.ravel(results))
    #convert the list into a json file by using jsnoify
    return jsonify(temps=temps)
#do flask run/ dont forget to add extension at the end

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