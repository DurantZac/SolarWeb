import sqlite3 as lite
import sys,os
con = lite.connect(os.path.join(sys.path[0], 'SolarWebServer/SolarData.db'))
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, TimeStamp DATETIME, Watts NUMERIC, UNIQUE(TimeStamp))")
    
                
