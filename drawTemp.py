# -*- coding: utf-8 -*-
#!/usr/bin/python

import numpy as np
import sqlite3
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def write_stats(stats):
    avg  = stats[0]
    last = stats[1]

    with open("/var/www/html/data/stats.php", "w") as f:
        f.write("<?php\n\n")
        f.write("$avg  = array(\"{}\",{});\n".format(avg[1], avg[2] ))
        f.write("$last = array(\"{}\",{});\n".format(last[1],last[2]))
        f.write("\n\n?>\n")


## Read data from file
def get_data_file(interval):
	with open("plotdata.txt") as f:
	    data = list(line for line in (l.strip() for l in f) if line)

	x = [datetime.strptime(' '.join(row.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S") for row in data]
	y = [row.split(' ')[3] for row in data]


## Load data from DB

def get_data(interval):

    conn=sqlite3.connect('/home/nacre/kastelu/temp.db')
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT timestamp,temperature FROM temps WHERE timestamp>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()

    # fetch statistics
    curs.execute("""SELECT 1,DATETIME(datetime('now', '+3 hours')),avg(temperature)
                    FROM temps
                    WHERE timestamp>datetime('now','-24 hours')
                    UNION
                    SELECT 2,*
                    FROM (
                         SELECT timestamp,temperature
                         FROM temps
                         ORDER BY timestamp DESC
                         LIMIT 1
                    )
                    ORDER BY 1""")
    stats=curs.fetchall()
    write_stats(stats)

    conn.close()

    return rows


data = get_data(24) # last 24h

x = [datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S") for row in data]
y = zip(*data)[1]

## Print data

plt.ioff()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title(u'Parvekelämpötila')
ax1.set_xlabel('Aika')
ax1.set_ylabel(u'Lampotila °C')

#ax1.set_xticks(x) # Tickmark + label at every plotted point
ax1.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,3)))
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('\n%d/%m/%Y'))

ax1.plot_date(x, y, ls='-', marker="")

ax1.grid(b=True, which='major')
ax1.grid(b=True, which='minor', linestyle='--')

#fig.autofmt_xdate(rotation=70)
fig.tight_layout()

#plt.setp(ax1.get_xticklabels(), rotation=45)

#fig.show()
#plt.show()

fig.savefig("/var/www/html/data/kuvaaja.png")
