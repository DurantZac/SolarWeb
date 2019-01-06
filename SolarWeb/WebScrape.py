from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sqlite3
import sys
import time
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

sampleFreq = 5*60
def add_data(power_now, energy_by_day, energy_by_month, energy_total, income):
    conn = sqlite3.connect('solarData.db')
    curs = conn.cursor()
    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(get_localzone())
    now_local = now_local.strftime ("%Y-%m-%d %H:%M:%S")
    curs.execute("INSERT INTO data values((?),(?),(?),(?),(?),(?),(?))",(None, now_local,power_now,energy_by_day,energy_by_month,energy_total,income))
    conn.commit()
    conn.close()

def try_get(url):
    try:
        with closing(get(url,stream=True)) as resp:
            return resp.content
    except RequestException as e:
        return None

def get_values():
    raw_html = try_get("https://www.ginlongmonitoring.com/Terminal/TerminalMain.aspx?pid=12799")
    html = BeautifulSoup(raw_html, 'html.parser')
    for p in html.select('span'):
        if p.has_attr('id'):
            if p['id'] == 'ctl00_childPanel_lblNow':
                length = len(p.text)
                data = p.text[:length-3]
                power_now = data
            if p['id'] == 'ctl00_childPanel_lblDEQ':
                length = len(p.text)
                data = p.text[:length-4]
                energy_by_day = data
            if p['id'] == 'ctl00_childPanel_lblMEQ':
                length = len(p.text)
                data = p.text[:length-4]
                energy_by_month = data
            if p['id'] == 'ctl00_childPanel_lblSEQ2':
                length = len(p.text)
                data = p.text[:length-4]
                energy_total = data
    
    income = round(float(energy_total) * 1000 * 0.24,2)

    print("Now: " + power_now)  
    print("Day: " + energy_by_day)
    print("Month: " + energy_by_month)
    print("Total: " + energy_total)
    print("Income: " + str(income))

    add_data(float(power_now),float(energy_by_day),float(energy_by_month),float(energy_total),float(income))
    
def main():
     while True:
        now_utc = datetime.now(pytz.utc)
        now_local = now_utc.astimezone(get_localzone())
        starttime = datetime.time(5)
        endtime = datetime.time(22)
        if(now_local.time > starttime and now_local.time < endtime):
            get_values()
        time.sleep(sampleFreq)

main()
