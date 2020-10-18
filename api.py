from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import datetime as dt

# create engine
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Base.metadata.create_all(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
print(Base.classes.keys())
latest = dt.date(2017, 8 ,23)
one_year = latest - dt.timedelta(days=365)

# step 1:
app = Flask(__name__)
@app.route("/")
def helloWorld():
    # urls that tell the user the end points that are available
    return (
        f"Hawaii Weather Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )
    
#return percipitation data for the past year
@app.route("/api/v1.0/precipitation")
def getprcp():
    percipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()
    percip = {date: prcp for date, prcp in percipitation}
    return jsonify(percip)

#return list of stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

#return temp observations for past year
@app.route("/api/v1.0/tobs")   
def temps():
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()

    tobs = list(np.ravel(results))
    return jsonify(tobs)

#return list of the minimum temp, the average temp and the max temp 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):




if __name__ == '__main__':
    app.run()