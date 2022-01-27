import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station

app = Flask(__name__)

@app.route("/")

def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)

    """Shows all dates and precipitation data"""

    precip = session.query(measurement.date, measurement.prcp).\
             order_by(measurement.date).all()


    precip_dict = []

    for date, prcp in precip:
        new_dict = {}
        new_dict["date"] = date
        new_dict["prcp"] = prcp
        precip_dict.append(new_dict)

    return jsonify(precip_dict)

    session.close()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Show all station names"""

    stat = session.query(measurement.station).all()

    stat_names = []

    for station in stat:
        all_stations = {}
        all_stations["station"] = station
        stat_names.append(all_stations)

    return jsonify(stat_names)

    session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Dates and temperature observations of most active station"""

    most_active = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()

    most_active_station = most_active[0][0]

    last_year = session.query(measurement.date, measurement.tobs).filter(measurement.date >= "2016-03-23").\
    filter(measurement.station == most_active_station).order_by(measurement.date).all()

    date_list = []

    for date, tobs in last_year:
        tobs_date = {}
        tobs_date[date] = tobs
        date_list.append(tobs_date)

    return jsonify(date_list)

    session.close()
