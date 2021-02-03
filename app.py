import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

app = Flast(__name__)

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

@app.route("/api.v1.0/precipitation")
def precip():
    session = Session(engine)

    results = session.query()