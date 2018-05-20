#!/usr/bin/python

import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

## Read data from file
def get_data_file(interval):
	with open("plotdata.txt") as f:
	    data = list(line for line in (l.strip() for l in f) if line)

	x = [datetime.strptime(' '.join(row.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S") for row in data]
	y = [row.split(' ')[3] for row in data]


## Load data from DB

def get_data(interval):

    conn=sqlite3.connect('/home/nacre/Documents/tempPlotter/templog.db')
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT DATETIME(timestamp, '+3 hours'),temp FROM temps WHERE timestamp>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows


data = get_data(24) # last 24h

x = [datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S") for row in data]
y = [row[1] for row in data]


## Print data

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Parvekelampotila")
ax1.set_xlabel('Aika')
ax1.set_ylabel('Lampotila *C')

ax1.set_xticks(x) # Tickmark + label at every plotted point
ax1.xaxis.set_major_locator(mdates.HourLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))

ax1.plot_date(x, y, ls='-', marker="")
ax1.grid(True)

fig.autofmt_xdate(rotation=45)
fig.tight_layout()

fig.show()

plt.show()