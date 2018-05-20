import serial
from time import gmtime, strftime
import sqlite3
import urllib2


# store the temperature in the database
def log_temperature(temp):
	conn=sqlite3.connect('/home/nacre/Documents/tempPlotter/templog.db')
	curs=conn.cursor()

	curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))

	# commit the changes
	conn.commit()
	conn.close()

def log_temperature2(temp):
	time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	f = open('plotdata.txt', 'a')
	f.write('{} {}'.format(time, temp))
	f.close()

def log_temp_online(temp):
    try:
		urllib2.urlopen("https://api.thingspeak.com/update?api_key=2FVNENYFI6ZKYG3G&field1={}".format(temp)).read()
    except urllib2.URLError:
        print "Connection failure"
    except:
    	print "General connection failure"


ser = serial.Serial('/dev/ttyACM0', 9600)

counter = 0
total   = 0

while True:

	a = ser.readline().split(' ')
	if len(a) > 2:
		temp = a[1]


		if temp != '' and temp.lstrip('-').replace('.','',1).isdigit():
			counter += 1
			total   += float(temp)

		if counter >= 286: # every 5 minutes #59:
			avg = round(total / counter, 2)
			counter = 0
			total   = 0

			log_temperature(avg)
			log_temp_online(avg)
			# log_temperature2(temp)

	else:
		print "incorrect data: " + " ".join(a)
