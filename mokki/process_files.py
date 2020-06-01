import os
import sys
from datetime import datetime, timedelta
import sqlite3
import pytz

path = '/home/mokki/Mokki'
sep  = ','
dbFile = '/home/mokki/data.db'

found = 0

def is_dst (tz):
    """Determine whether or not Daylight Savings Time (DST)
    is currently in effect"""

    x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(tz)) # Jan 1 of this year
    y = datetime.now(pytz.timezone(tz))

    # if DST is in effect, their offsets will be different
    return not (y.utcoffset() == x.utcoffset())

# store the data in the database
def store_data(time, d):
    conn=sqlite3.connect(dbFile)

    # use the connection as a context manager
    try:
        with conn:
            conn.execute("INSERT INTO data values((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?));", (time, d[15], d[17], d[19], d[3], d[5], d[7], d[9], d[11], d[13], d[23]))
    except sqlite3.IntegrityError:
        print "Duplicate value: "
        print time

    # use cursor + commit
    curs=conn.cursor()
#    curs.execute("INSERT INTO stats(param,valueText,valueInt,timestamp) values('uptime','17.8.2018 18:16',0,DATETIME(datetime('now', '+3 hours')))")
    curs.execute("UPDATE stats SET valueText=(?), timestamp=DATETIME(datetime('now','localtime')) where param='uptime';", (d[21],))
    conn.commit()

    # close connection
    conn.close()

def processLine(line):
    global found

    if '/' in line:
         line = line.replace('/', '0')
#        print "Incorrect line!!!"
#        print line
#        return 0

#    l = line.replace(" ","").split(sep)
    l = line.split(sep)
    for a in range(len(l)):
        if a < 20: # dont remove spaces from uptime field
            l[a] = l[a].replace(" ","")

    date = datetime.strptime(' '.join(l[0:2]), "%Y-%m-%d %H:%M:%S")

    # fix timestamp from server
    if is_dst('Europe/Helsinki'):
        date = date + timedelta(hours = 1)

    print date
    print line

    store_data(date, l)

    found = 1

def saveIP():
    mokkiIP = os.system("/home/mokki/storeIP.sh")

for file in os.listdir(path):
    current = os.path.join(path, file)
    if os.path.isfile(current):

        if file.endswith(".rep"):

            print "-- processing file {}...".format(file)
            with open(current, "r") as f:
                for line in f:
                    processLine(line)

            # remove processed file
#            os.rename(current, os.path.join('/home/mokki/old/', file))
            os.remove(current)
            print ".. file removed."

if found > 0:
    os.system("/usr/bin/python /home/mokki/drawFig.py")
    saveIP()
