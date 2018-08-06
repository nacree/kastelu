# -*- coding: utf-8 -*-
#!/usr/bin/python

import time

start_time = time.time()

import numpy as np
import sqlite3
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def get_data(interval):

    conn=sqlite3.connect('/home/mokki/data.db')
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM data")
    else:
        curs.execute("SELECT timestamp,temperature,wind_s,rain_a,rain_i,humidity,pressure FROM data WHERE timestamp>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()
    conn.close()

    return rows

print("1 --- %s seconds ---" % (time.time() - start_time))

data = get_data(24) # last 24h

x = [datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S") for row in data]

tmp = zip(*data)
y = tmp[1] # temperature
w = tmp[2] # wind
z1 = tmp[3] # rain
z2 = tmp[4] # rain intensity
hu = tmp[5] # humidity
pr = tmp[6] # pressure

avg = mean(y) # avg temp

## Print data

plt.ioff()

#i = 3
#if i == 2:
for i in range(5):

    print "Loop i={}".format(i)

    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_xlabel('Aika')

    if i == 0:
        ax1.set_title(u'Ulkolämpötila')
        ax1.set_ylabel(u'Lampotila °C')
    elif i == 1:
        ax1.set_title(u'Tuulen nopeus')
        ax1.set_ylabel(u'Nopeus m/s')
    elif i == 2:
        ax1.set_title(u'Kumulatiivinen sademäärä')
        ax1.set_ylabel(u'Sademäärä mm')
    elif i == 3:
        ax1.set_title(u'Suhteellinen kosteus')
        ax1.set_ylabel(u'Kosteus %')
    elif i == 4:
        ax1.set_title(u'Ilmanpaine')
        ax1.set_ylabel(u'Ilmanpaine hPa')


    print("2 --- %s seconds ---" % (time.time() - start_time))

    #ax1.set_xticks(x) # Tickmark + label at every plotted point
    ax1.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,3)))
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('\n%d/%m/%Y'))

    if i == 0:
        ax1.plot_date(x, y, ls='-', marker="")
    elif i == 1:
        ax1.plot_date(x, w, ls='-', marker="")
    elif i == 2:
        ax1.plot_date(x, z1, ls='-', marker="")
#        ax1.plot_date(x, z2, color='k', ls='-', marker="")
        interval = 1.0/24/6
#        ax1.bar(x, z1, width=interval)
        ax1.bar(x, z2, color='k', width=interval)
        ax1.xaxis_date()
    elif i == 3:
        ax1.plot_date(x, hu, ls='-', marker="")
    elif i == 4:
        ax1.plot_date(x, pr, ls='-', marker="")

    ax1.grid(b=True, which='major')
    ax1.grid(b=True, which='minor', linestyle='--')

    #fig.autofmt_xdate(rotation=70)
    fig.tight_layout()

    if i == 0:
        # add avg as horizontal line
        ax1.axhline(y=avg, color='k', linestyle='--', linewidth=1)

    #plt.setp(ax1.get_xticklabels(), rotation=45)

    print("3 --- %s seconds ---" % (time.time() - start_time))

    file = ""
    if i == 0:
        file = "/var/www/html/data/mokki_temp.png"
    elif i == 1:
        file = "/var/www/html/data/mokki_wind.png"
    elif i == 2:
        file = "/var/www/html/data/mokki_rain.png"
    elif i == 3:
        file = "/var/www/html/data/mokki_humi.png"
    elif i == 4:
        file = "/var/www/html/data/mokki_pres.png"

    fig.savefig(file)

    print("4 --- %s seconds ---" % (time.time() - start_time))
