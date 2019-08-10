import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to Surfs Up weather app<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    yearBefore = dt.date.today() - dt.timedelta(days=365)
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date > yearBefore).order_by(Measurement.date).all())
    prcpData = []
    for result in results:
        prcpDict = {result.date: result.prcp, "Station": result.station}
        prcpData.append(prcpDict)
    return jsonify(prcpData)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    everyStation = list(np.ravel(results))
    return jsonify(everyStation)


@app.route('/api/v1.0/tobs')
def tobs():
	yearBefore = dt.date.today() - dt.timedelta(days=365)
	tobs = session.query(Measurement.tobs).filter(Measurement.date >= yearBefore).all()
	tobsList = list(np.ravel(tobs))
	return jsonify(tobsList)


@app.route("/api/v1.0/<start>")
def start(start=None):
    start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    startList=list(start)
    return jsonify(startList)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):    
    dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    datesList=list(dates)
    return jsonify(datesList)

if __name__ == '__main__':
    app.run(debug=True)      