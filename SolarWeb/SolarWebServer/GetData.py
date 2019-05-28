from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3, os, sys, json, simplejson, pytz, collections, calendar, datetime
from pytz import timezone
from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getSimpleData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    curs.execute("SELECT sum(KWH) / 1000 as energy_total FROM dailydata")
    row = curs.fetchall()[0]
    income = round(float(row['energy_total']) * 176, 2)
    return round(row['energy_total'],2), income

def getTodaysData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    query = "SELECT TimeStamp, Watts FROM data WHERE TimeStamp > '{0}'".format(today)
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
    curs.execute("SELECT Sum(KWH) as KWH,"
				 "strftime('%d-%m-%Y',TimeStamp) as TimeStamp,"
				 "cast (strftime('%w', TimeStamp) as integer) as dayNum,"
				 "case cast (strftime('%w', TimeStamp) as integer) when 0 then 'Sunday' when 1 then 'Monday' when 2 then 'Tuesday' when 3 then 'Wednesday' when 4 then 'Thursday' when 5 then 'Friday'"
				 "else 'Saturday' end as DayofWeek "
				 "FROM dailydata WHERE TimeStamp > ? GROUP BY strftime('%d-%m-%Y',TimeStamp) ORDER BY strftime('%Y',TimeStamp),strftime('%j',TimeStamp) ",[week_local])
    rows = curs.fetchall()
    return rows

def getMonthBarChartData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    now_local = datetime.datetime.now()
    delta = relativedelta(months=11)
    new_month = (now_local - delta).date().strftime("%Y-%m-%d")
    curs.execute("SELECT Sum(KWH) as EnergyByMonth,"
                 "case strftime('%m', TimeStamp) when '01' then 'January' when '02' then 'Febuary' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June' when '07' then 'July' when '08' then 'August' when '09' then 'September' when '10' then 'October' when '11' then 'November' when '12' then 'December' else '' end as Month "
                 "FROM dailydata WHERE TimeStamp > ?"
                 "GROUP BY strftime('%m-%Y',TimeStamp) ORDER BY strftime('%Y',TimeStamp), strftime('%m',TimeStamp)",[new_month])
    rows = curs.fetchall()
    return rows

def getReturnOnInvestmentChartData():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
    conn.row_factory = dict_factory
    curs = conn.cursor()
    now_local = datetime.datetime.now()
    delta = relativedelta(months=11)
    new_month = (now_local - delta).date().strftime("%Y-%m-%d")
    curs.execute("SELECT Sum(KWH) * 0.176 as EnergySavingByYear, 3622 as Depreciation, strftime('%Y',TimeStamp) as Year FROM dailydata WHERE TimeStamp > ? GROUP BY strftime('%Y',TimeStamp) ORDER BY strftime('%Y',TimeStamp), strftime('%m',TimeStamp)",[new_month])
    rows = curs.fetchall()
    try:
        for row in rows:
            test = row['Year']
            yeardiff =  int(row['Year']) - 2018
            inflation = 1 + (.3 * yeardiff) 
            row['EnergySavingByYear'] = (row['EnergySavingByYear'] * inflation)
    except Exception as e:
           print(e)
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

@app.route("/returnoninvestment")
def returnOnInvestmentChartData():
    return json.dumps(getReturnOnInvestmentChartData())

@app.route("/dialdata", methods=["GET","POST"])
def dialData():
	conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarData.db'))
	curs = conn.cursor()
	curs.execute("SELECT Watts FROM data Where TIMESTAMP < strftime('%Y-%m-%d %H-%M',datetime('now','localtime')) ORDER BY TIMESTAMP DESC LIMIT 1")
	data = curs.fetchall()
	watts = data[0][0]
	return simplejson.dumps(dict(value="%.2f" % round((watts/1000),2)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82, debug = False)
