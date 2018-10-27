#########################################################################
from flask import Flask, jsonify
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

begin_date = dt.date(2017, 8, 20)
end_date = dt.date(2017, 8, 23)
year_from_beg = begin_date - dt.timedelta(days=365)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

meas = Base.classes.measurement
station = Base.classes.station

sess = Session(engine)

app = Flask(__name__)

#########################################################################
@app.route("/")

def welcome():
	print("We have a new visitor.")

	return ("Our API routes are as follows:<br/>"
		   "[1] /api/v1.0/precipitation<br/>"
		   "[2] /api/v1.0/stations<br/>"
		   "[3] /api/v1.0/tobs<br/>"
		   "[4] /api/v1.0/start_date<br/>"
		   "[5] /api/v1.0/start_date/end_date<br/>"
		   "<br/>"
		   "Very Important Warning:"
		   "In order for the search to work correctly, please enter your query with the following one of the following formats:<br/>"
		   "[1] YYYYMDD if there is only one digit in the month or<br/>"
		   "[2] YYYYMMDD if there are two digits in the month.<br/><br/>"
		   "Our database only holds information for dates between 20100101 and 20170823, inclusive.<br/>"
		   "The 'precipitation' page hosts dates and temperature observations starting from date August 21, 2016 and ending on August 20, 2017 (which is the start date of our excursion).<br/>"
		   "The 'stations' page returns a JSON list of stations from our database.<br/>"
		   "The 'tobs' page return a JSON list of temperature observations betweens the dates August 21, 2016 and August 20, 2017, inclusive.<br/>"
		   "The 'start_date' endpoint returns a JSON list of the mimimum, average, and maximum temperatures for all dates greater than or equal to the start date.<br/>"
		   "The 'start_date/'end_date' endpoint returns a JSON list of the minimum, average, and maximum temperatures for all dates between the start and end dates, inclusive.")

#########################################################################
@app.route("/api/v1.0/precipitation")
def prcp():
	sess.query(meas.date, meas.tobs).filter(meas.date > year_from_beg).all()
	keys=[]
	values=[]
	for i in sess.query(meas.date, meas.tobs).filter(meas.date > year_from_beg).all():
	    keys.append(i[0])
	    values.append(i[1])
	results = dict(zip(keys, values))
	return jsonify(results)

#########################################################################
@app.route("/api/v1.0/stations")
def list_stations():
	stations=[]
	for i in sess.query(meas.station, station.station).filter(meas.station == station.station).\
	    group_by(meas.station).all():
	    stations.append(i[0])
	return jsonify(stations)

#########################################################################
@app.route("/api/v1.0/tobs")
def tobs_list():
	tobs=[]
	for i in sess.query(meas.tobs).filter(meas.date > year_from_beg).all():
	    tobs.append(i[0])
	return jsonify(tobs)

#########################################################################
@app.route("/api/v1.0/<start>")
def start(start):

	if len(start) > 8 or len(start) < 7:
	    return ("In order for the search to work correctly, please enter your query with the following one of the following formats: <br/>"
		   		"[1] YYYYMDD if there is only one digit in the month or<br/>"
		   		"[2] YYYYMMDD if there are two digits in the month.")

	broken_date = [i for i in start]

	if len(start) == 7:
		year = f"{broken_date[0]}{broken_date[1]}{broken_date[2]}{broken_date[3]}"
		month = f"{broken_date[4]}"
		day = f"{broken_date[5]}{broken_date[6]}"
		year = int(year)
		month = int(month)
		day = int(day)
		search_date = dt.date(year, month, day)
		results = sess.query(meas.tobs).filter(meas.date >= search_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

	if len(start) == 8:
		year = f"{broken_date[0]}{broken_date[1]}{broken_date[2]}{broken_date[3]}"
		month = f"{broken_date[4]}{broken_date[5]}"
		day = f"{broken_date[6]}{broken_date[7]}"
		year = int(year)
		month = int(month)
		day = int(day)
		search_date = dt.date(year, month, day)
		results = sess.query(meas.tobs).filter(meas.date >= search_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

#########################################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

	if len(start) > 8 or len(start) < 7:
	    return ("In order for the search to work correctly, please enter your query with the following one of the following formats: <br/>"
		   		"[1] YYYYMDD if there is only one digit in the month or<br/>"
		   		"[2] YYYYMMDD if there are two digits in the month.")
	elif len(end) > 8 or len(end) < 7:
		return ("In order for the search to work correctly, please enter your query with the following one of the following formats: <br/>"
		   		"[1] YYYYMDD if there is only one digit in the month or<br/>"
		   		"[2] YYYYMMDD if there are two digits in the month.")

	broken_start = [i for i in start]
	broken_end = [i for i in end]

	if len(start) == 7 and len(end) == 7:
		start_year = f"{broken_start[0]}{broken_start[1]}{broken_start[2]}{broken_start[3]}"
		start_month = f"{broken_start[4]}"
		start_day = f"{broken_start[5]}{broken_start[6]}"
		start_year = int(start_year)
		start_month = int(start_month)
		start_day = int(start_day)
		start_date = dt.date(start_year, start_month, start_day)

		end_year = f"{broken_end[0]}{broken_end[1]}{broken_end[2]}{broken_end[3]}"
		end_month = f"{broken_end[4]}"
		end_day = f"{broken_end[5]}{broken_end[6]}"
		end_year = int(end_year)
		end_month = int(end_month)
		end_day = int(end_day)
		end_date = dt.date(end_year, end_month, end_day)

		results = sess.query(meas.tobs).filter(meas.date >= start_date).filter(meas.date <= end_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

	if len(start) == 8 and len(end) == 7:
		start_year = f"{broken_start[0]}{broken_start[1]}{broken_start[2]}{broken_start[3]}"
		start_month = f"{broken_start[4]}{broken_start[5]}"
		start_day = f"{broken_start[6]}{broken_start[7]}"
		start_year = int(start_year)
		start_month = int(start_month)
		start_day = int(start_day)
		start_date = dt.date(start_year, start_month, start_day)

		end_year = f"{broken_end[0]}{broken_end[1]}{broken_end[2]}{broken_end[3]}"
		end_month = f"{broken_end[4]}"
		end_day = f"{broken_end[5]}{broken_end[6]}"
		end_year = int(end_year)
		end_month = int(end_month)
		end_day = int(end_day)
		end_date = dt.date(end_year, end_month, end_day)

		results = sess.query(meas.tobs).filter(meas.date >= start_date).filter(meas.date <= end_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

	if len(start) == 7 and len(end) == 8:
		start_year = f"{broken_start[0]}{broken_start[1]}{broken_start[2]}{broken_start[3]}"
		start_month = f"{broken_start[4]}"
		start_day = f"{broken_start[5]}{broken_start[6]}"
		start_year = int(start_year)
		start_month = int(start_month)
		start_day = int(start_day)
		start_date = dt.date(start_year, start_month, start_day)

		end_year = f"{broken_end[0]}{broken_end[1]}{broken_end[2]}{broken_end[3]}"
		end_month = f"{broken_end[4]}{broken_end[5]}"
		end_day = f"{broken_end[6]}{broken_end[7]}"
		end_year = int(end_year)
		end_month = int(end_month)
		end_day = int(end_day)
		end_date = dt.date(end_year, end_month, end_day)

		results = sess.query(meas.tobs).filter(meas.date >= start_date).filter(meas.date <= end_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

	if len(start) == 8 and len(end) == 8:
		start_year = f"{broken_start[0]}{broken_start[1]}{broken_start[2]}{broken_start[3]}"
		start_month = f"{broken_start[4]}{broken_start[5]}"
		start_day = f"{broken_start[6]}{broken_start[7]}"
		start_year = int(start_year)
		start_month = int(start_month)
		start_day = int(start_day)
		start_date = dt.date(start_year, start_month, start_day)

		end_year = f"{broken_end[0]}{broken_end[1]}{broken_end[2]}{broken_end[3]}"
		end_month = f"{broken_end[4]}{broken_end[5]}"
		end_day = f"{broken_end[6]}{broken_end[7]}"
		end_year = int(end_year)
		end_month = int(end_month)
		end_day = int(end_day)
		end_date = dt.date(end_year, end_month, end_day)

		results = sess.query(meas.tobs).filter(meas.date >= start_date).filter(meas.date <= end_date).all()
		results = list(np.ravel(results))
		return jsonify({"Minimum Temperature": min(results), "Average Temperature": np.mean(results), "Maximum Temperature": max(results)})

#########################################################################
if __name__ == "__main__":
	app.run(debug=True)







