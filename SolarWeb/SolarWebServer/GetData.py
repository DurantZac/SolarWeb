from flask import Flask, render_template,request
import collections
app = Flask(__name__)
import sqlite3
import json
import simplejson
import pytz
from pytz import timezone
from tzlocal import get_localzone
from datetime import *
import calendar
from dateutil.relativedelta import relativedelta

import ptvsd
ptvsd.enable_attach()

def getSimpleData():
    conn = sqlite3.connect('../solarData.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1")
    row = curs.fetchall()
    for r in row:
        print(str(row))
        energy_total = r[5]
        income = r[6]
    return energy_total, income

def getData():
    conn = sqlite3.connect('../solarData.db')
    curs = conn.cursor()
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(get_localzone())
    delta = timedelta(days=1)
    form = "%Y-%m-%d"
    yesterday = now_local
    yesterday = yesterday.strftime(form)
    curs.execute("SELECT * FROM data WHERE TimeStamp > (?)",([yesterday]))
    #curs.execute("SELECT * FROM data ORDER BY TimeStamp DESC LIMIT 144")
    rows = curs.fetchall()
    conn.close()
    return rows

def getDayBarChartData():
    conn = sqlite3.connect('../solarData.db')
    curs = conn.cursor()
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(get_localzone())
    delta = timedelta(days=6)
    form = "%Y-%m-%d"
    week_local = (now_local - delta).date()
    curs.execute("SELECT MAX(EnergyByDay), TimeStamp FROM data WHERE TimeStamp > ? GROUP BY strftime('%d-%Y',TimeStamp)",[week_local])
    rows = curs.fetchall()
    return rows

def getMonthBarChartData():
    conn = sqlite3.connect('../solarData.db')
    curs = conn.cursor()
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(get_localzone())
    delta = relativedelta(months=11)
    new_month = (now_local - delta).date()
    form = "%Y-%m-%d"
    curs.execute("SELECT MAX(EnergyByMonth),strftime('%m',TimeStamp) FROM data WHERE TimeStamp > ? GROUP BY strftime('%m-%Y',TimeStamp)",[new_month])
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
    dataAsDict = []
    for r in getData():
        d = collections.OrderedDict()
        fullTime = r[1]
        d["time"] = fullTime.split(' ')[1]
        d["power_now"] = r[2]
        d["energy_by_day"] = r[3]
        d["energy_by_month"] = r[4]
        d["energy_total"] = r[5]
        d["income"] = r[6]
        dataAsDict.append(d)
    return json.dumps(dataAsDict)

@app.route("/energydaygraphdata")
def energyDayGraphData():
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(get_localzone())
    delta = timedelta(days=6)
    week_local = now_local - delta
    dayNum = week_local.weekday()
    day = calendar.day_name[dayNum]
    startDayNum = dayNum
    dataAsDict = []
    for r in getDayBarChartData:
        d = collections.OrderedDict()
        dayNum = r[1].weekday()
        dayOfWeek = calendar.day_name[dayNum]
        d["day"] = dayOfWeek
        d["energy_by_day"] = r[0]
        dataAsDict.append(d)
    print(json.dumps(dataAsDict))
    return json.dumps(dataAsDict)

@app.route("/energymonthgraphdata")
def energyMonthGraphData():
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(get_localzone())
    delta = relativedelta(months=11)
    month_local = (now_local - delta).date()
    monthNum = month_local.month
    month = calendar.month_name[monthNum]
    startMonthNum = monthNum
    dataAsDict = []
    d = collections.OrderedDict()
    for r in getMonthBarChartData():
        d["month"] = r[1]
        d["energy_by_month"] = r[0]
        dataAsDict.append(d)
    print(json.dumps(dataAsDict))
    return json.dumps(dataAsDict)

@app.route("/dialdata", methods=["GET","POST"])
def dialData():
	conn = sqlite3.connect('../solarData.db')
	curs = conn.cursor()
	curs.execute("SELECT PowerNow FROM data ORDER BY TIMESTAMP DESC LIMIT 1")
	data = curs.fetchall()
	return simplejson.dumps(dict(value="%i" % data[0]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = False)
