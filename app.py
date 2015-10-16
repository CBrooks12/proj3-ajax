"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");
  miles = request.args.get('miles',0,type=float)
  distance = request.args.get('distance', 3, type=float)
  distType = request.args.get('distType', 4, type=str)
  app.logger.debug(distType);
  app.logger.debug(miles);
  if distType == 'Miles':
      miles = miles * 1.609
  date_time = request.args.get('date', 0, type=str)
  date_time = date_time + " " + request.args.get('time', 0, type=str)

  base = arrow.get(date_time,'MM/DD/YYYY HH:mm')

  if miles>float(distance*1.1) or miles < 0:
      d = {'openBase': 'Distance input error', 'closeBase': 'Distance input error'}
      d = json.dumps(d)
      return jsonify(result = d)
  elif miles == 0:
      d = {'openBase': format_arrow_date(base), 'closeBase': format_arrow_date(base.replace(minutes=+60))}
      d = json.dumps(d)
      return jsonify(result = d)
  
  closeTimeMinutes = close_time_calc(miles)
  closeTimeMinutes*=60
  openTimeMinutes = open_time_calc(miles)
  openTimeMinutes*=60
  closeBase = base.replace(minutes=+closeTimeMinutes)
  openBase = base.replace(minutes=+openTimeMinutes)
  closeBase = format_arrow_date(closeBase) #base.format('MM/DD/YYYY HH:mm')
  openBase = format_arrow_date(openBase)
  #app.logger.debug(base);
  d = {'openBase': openBase, 'closeBase': closeBase}
  d = json.dumps(d)
  return jsonify(result = d)

def close_time_calc(miles):
    if miles <= 600:
        timeMinutes = miles/15
    else:
        timeMinutes = 600/15
        timeMinutes = timeMinutes + (miles-600)/11.428   
    return timeMinutes

def open_time_calc(miles):
    timeMinutes = 0;
    overTime = 0;
    if miles >= 1000:
        overTime = (miles-1000)
        timeMinutes = timeMinutes + overTime/26 
    if miles >= 600:
        overTime =  (miles-600) - overTime
        timeMinutes = timeMinutes + overTime/28
    if miles >= 400:
        overTime = (miles-400) - overTime
        timeMinutes = timeMinutes + overTime/30
    if miles >= 200:
        overTime = (miles-200) - overTime
        timeMinutes+= overTime/32
    overTime = miles - overTime
    timeMinutes = timeMinutes + overTime/34
    return timeMinutes
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY HH:mm")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
