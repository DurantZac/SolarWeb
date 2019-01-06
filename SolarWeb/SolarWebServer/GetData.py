from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3, os, sys, json, simplejson, pytz, collections, calendar, datetime
from pytz import timezone
from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta

import ptvsd
ptvsd.enable_attach()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getSimpleData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    curs.execute("SELECT sum(watts) as energy_total FROM data")
    row = curs.fetchall()[0]
    income = round(float(row['energy_total']) * 1000 * 0.24,2)
    return row['energy_total'], income

def getTodaysData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d));
    query = "SELECT TimeStamp, Watts FROM data WHERE TimeStamp > {0}".format([today])
    curs.execute(query)
    rows = curs.fetchall()
    conn.close()
    return rows

def getDayBarChartData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    delta = datetime.timedelta(days=6)
    week_local = (datetime.datetime.now() - delta).date().strftime("%Y-%m-%d")
    curs.execute("SELECT Sum(Watts) as Watts,"
				 "strftime('%d-%m-%Y',TimeStamp) as TimeStamp,"
				 "cast (strftime('%w', TimeStamp) as integer) as dayNum,"
				 "case cast (strftime('%w', TimeStamp) as integer) when 0 then 'Sunday' when 1 then 'Monday' when 2 then 'Tuesday' when 3 then 'Wednesday' when 4 then 'Thursday' when 5 then 'Friday'"
				 "else 'Saturday' end as DayofWeek "
				 "FROM data WHERE TimeStamp > ? GROUP BY strftime('%d-%m-%Y',TimeStamp) ORDER BY strftime('%Y',TimeStamp),strftime('%j',TimeStamp) ",[week_local])
    rows = curs.fetchall()
    return rows

def getMonthBarChartData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    now_local = datetime.datetime.now()
    delta = relativedelta(months=11)
    new_month = (now_local - delta).date().strftime("%Y-%m-%d")
    curs.execute("SELECT Sum(Watts) as EnergyByMonth,strftime('%m',TimeStamp) as Month FROM data WHERE TimeStamp > ? GROUP BY strftime('%m-%Y',TimeStamp) ORDER BY strftime('%Y',TimeStamp), strftime('%m',TimeStamp)",[new_month])
    rows = curs.fetchall()
    return rows

@app.route("/")
def index():
    energy_total, income = getSimpleData()
    templateData = {
	    'energy_total': energy_total,
	    'income': income,
            }
    return render_template('index.html',**templateData)

@app.route("/powergraphdata")
def powerGraphData():
    return json.dumps(getTodaysData())

@app.route("/energydaygraphdata")
def energyDayGraphData():
    return json.dumps(getDayBarChartData())

@app.route("/energymonthgraphdata")
def energyMonthGraphData():
    return json.dumps(getMonthBarChartData())

@app.route("/dialdata", methods=["GET","POST"])
def dialData():
	conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
	curs = conn.cursor()
	curs.execute("SELECT Watts FROM data ORDER BY TIMESTAMP DESC LIMIT 1")
	data = curs.fetchall()
	return simplejson.dumps(dict(value="%i" % data[0]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = False)
