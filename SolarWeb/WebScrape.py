from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sqlite3, sys, os, time, pytz, datetime, requests, json, random
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

conn = sqlite3.connect(os.path.join(sys.path[0], 'SolarWebServer/SolarData.db'))
curs = conn.cursor()

sampleFreq = 5*60
def add_data(row): #power_now, energy_by_day, energy_by_month, energy_total, income
    now_local = datetime.datetime.now()
    query = "INSERT OR IGNORE INTO data(TimeStamp, Watts) values('{0}',{1})".format(row[0].replace("/", "-"),row[1])
    curs.execute(query)
    conn.commit()
    #conn.close()

def add_dailydata(row): #kwh, year, month, day, hour, min, sec
    test = row["Year"]
    date = datetime.datetime(int(row["Year"]),int(row["Mouth"])+1,int(row["Day"]))
    query = "INSERT OR REPLACE INTO DailyData(TimeStamp, KWH) values('{0}',{1})".format(date,row["y"])
    curs.execute(query)
    conn.commit()
    #conn.close()

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

startup = True
def getData():
            #recheck the last week on startup
            delta = relativedelta(days=0) 
            global startup 
            if startup == True:
                delta = relativedelta(days=7)
                startup = False
            start_dt = datetime.date.today() - delta
            end_dt =  datetime.date.today()
            s = requests.session()
            s.post("https://www.ginlongmonitoring.com/Terminal/TerminalMain.aspx?pid=12799")
            for dt in daterange(start_dt, end_dt):
                response = s.post('https://www.ginlongmonitoring.com/Terminal/iChart/iChartService.ashx?ac=MainChart&Type=14&load_data_type=chart', params = { 'Time' : dt.strftime("%Y-%m-%d"), 'rand' : random.randint(1,100) /100, 'localTimeZone': 13})
                try:
                    responsedict = json.loads(response.text)
                    response = responsedict['power']
                    for row in response:
                        add_data(row)
                except:
                    print(response.text)
                response = s.post('https://www.ginlongmonitoring.com/Terminal/iChart/iChartService.ashx?ac=MainChart&Type=12&load_data_type=chart', params = { 'Time' : dt.strftime("%Y-%m-%d"), 'rand' : random.randint(1,100) /100, 'localTimeZone': 13})
                try:
                    responsedict = json.loads(response.text)
                    for row in responsedict:
                        add_dailydata(row)
                except Exception as e:
                    print(e)
                
              

def time_in_range(start, end, x):
    #Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
  
def main():
     while True:
         if time_in_range(datetime.time(5, 0, 0), datetime.time(22, 0, 0), datetime.datetime.now().time()):
             getData()
         time.sleep(sampleFreq)

main()
