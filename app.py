import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"-----------------------------------------<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"*will return precipitation records as date:precipitation amount<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"*will return station id numbers<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"*will return date and temperature records for the last year from the most active station (USC00519281)<br/><br/>"
        f"-   -   -   -   -   -   -   -   -   -   - <br/>"
        f"**Note: Dates must be entered as yyyy-mm-dd for the routes below:<br/>"
        f"/api/v1.0/start%20date<br/>"
        f"/api/v1.0/start%20date/end%20date<br/>"
        f"*will return the minimum, average, and maximum temperature within the date range specified. If no end date is given, the end of the dataset will be used.<br/>"
        f"*Returns records as [[[minimum]],[[average]],[[maximum]]]"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    weather_dict = {}

    for date, prcp in results:
        
        weather_dict[date] = prcp

    return jsonify(weather_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-24').filter(Measurement.station=='USC00519281').all()

    session.close()

    # to create a simple list would just be: temp_list = list(np.ravel(results)) , but I would like to place results in a dictionary first for clarity and organization

    temp_list = []

    for date, tobs in results:
        temp_dict = {}
        temp_dict[date]=tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    weather_list = []

    low = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    high = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    weather_list.append(low)
    weather_list.append(avg)
    weather_list.append(high)

    return jsonify(weather_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    weather_list = []

    low = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    high = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    weather_list.append(low)
    weather_list.append(avg)
    weather_list.append(high)

    return jsonify(weather_list)    

if __name__ == '__main__':
    app.run(debug=False)
