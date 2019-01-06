import sqlite3 as lite
import sys
con = lite.connect('solarData.db')
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, TimeStamp DATETIME, PowerNow NUMERIC, EnergyByDay NUMERIC, EnergyByMonth NUMERIC, EnergyTotal NUMERIC, Income NUMERIC)")
    
                
