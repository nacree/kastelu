#!/usr/bin/python

import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
# import constants for the days of the week
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

## Load data from DB

def get_data():

    conn=sqlite3.connect('/tmp/templog.db')
    curs=conn.cursor()

    curs.execute("SELECT date(DATETIME(timestamp, '+3 hours')) as d,round(avg(temp),2), round(max(temp),2), round(min(temp),2) FROM temps group by d")

    rows=curs.fetchall()

    conn.close()

    return rows


data = get_data()

x  = [datetime.strptime(row[0],"%Y-%m-%d") for row in data]
tavg = [row[1] for row in data]
tmax = [row[2] for row in data]
tmin = [row[3] for row in data]

## Print data

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Parvekelampotila")
ax1.set_xlabel('Aika')
ax1.set_ylabel('Lampotila *C')

ax1.set_xticks(x) # Tickmark + label at every plotted point

# tick on mondays every week
loc = mdates.WeekdayLocator(byweekday=MO) #, tz=mdates.tz)
ax1.xaxis.set_major_locator(loc)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

ax1.plot_date(x, tavg, ls='-', marker=".", color='blue',  label='Average')
ax1.plot_date(x, tmax, ls='-', marker="",  color='red',   label='Max')
ax1.plot_date(x, tmin, ls='-', marker="",  color='black', label='Min')

ax1.legend(loc='best', fancybox=True, framealpha=0.5)

ax1.grid(True)

fig.autofmt_xdate(rotation=45)
fig.tight_layout()

fig.show()

plt.show()