import os
import sys
from datetime import datetime
import sqlite3

path = '/home/mokki/Mokki'
sep  = ','
dbFile = '/home/mokki/data.db'

found = 0

# store the data in the database
def store_data(time, d):
    conn=sqlite3.connect(dbFile)
    curs=conn.cursor()

    curs.execute("INSERT INTO data values((?),(?),(?),(?),(?),(?),(?),(?),(?),(?));", (time, d[15], d[17], d[19], d[3], d[5], d[7], d[9], d[11], d[13]))

#    curs.execute("INSERT INTO stats(param,valueText,valueInt,timestamp) values('uptime','17.8.2018 18:16',0,DATETIME(datetime('now', '+3 hours')))")
    curs.execute("UPDATE stats SET valueText=(?), timestamp=DATETIME(datetime('now', '+3 hours')) where param='uptime';", (d[21],))

    # commit the changes
    conn.commit()
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
    print date
    print line

    store_data(date, l)

    found = 1


for file in os.listdir(path):
    current = os.path.join(path, file)
    if os.path.isfile(current):

        if file.endswith(".rep"):

            print "-- processing file {}...".format(file)
            with open(current, "r") as f:
                for line in f:
                    processLine(line)

            # remove processed file
            os.rename(current, os.path.join('/home/mokki/old/', file))

if found > 0:
    os.system("/usr/bin/python /home/mokki/drawFig.py")
