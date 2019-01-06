from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sqlite3
import sys
import time
from datetime import datetime, date, timedelta
from pytz import timezone
from tzlocal import get_localzone

conn = sqlite3.connect('solarData.db')
curs = conn.cursor()

days= [21]
power_now = 0
energy_by_day = 0
energy_by_month = 0
energy_total = 0
income = 0
for month in range(1,13):
    for day in range(1,29):
        time = datetime(2018,month,day)
        for i in range(0,288):
            if(i < 144):
                power_now = power_now + (0.01*i)
            else:
                power_now = power_now - (0.01*i)
                if(power_now < 0):
                    power_now = 0
            energy_by_day = energy_by_day + power_now
            energy_by_month = energy_by_month + power_now
            energy_total = energy_total + power_now
            income = energy_total * 0.5
            curs.execute("INSERT INTO data values((?),(?),(?),(?),(?),(?),(?))",(None,time,power_now,energy_by_day,energy_by_month,energy_total,income))
            time = time + timedelta(minutes = 5)
        energy_by_day = 0
    energy_by_month = 0
for month in range(1,13):
    date = datetime(2018,month,1)
    curs.execute("INSERT INTO data values((?),(?),(?),(?),(?),(?),(?))",(None,date,0,0,0,0,0))
    
conn.commit()
conn.close()
