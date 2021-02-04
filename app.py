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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api.v1.0/tobs<br/>"
        f"/api.v1.0/<start><br/>"
        f"/api.v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    weather_meas = []

    for date, prcp in results:
        weather_dict = {}
        weather_dict[date] = prcp
        weather_meas.append(weather_dict)

    return jsonify(weather_meas)

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

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=False)
