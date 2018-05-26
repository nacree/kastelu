import serial
from time import gmtime, strftime
import sqlite3
import urllib2


# store the temperature in the database
def log_temperature(temp):
	conn=sqlite3.connect('/home/nacre/kastelu/temp.db')
	curs=conn.cursor()

	curs.execute("INSERT INTO temps values(DATETIME(datetime('now', '+3 hours')), (?))", (temp,))

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


ser = serial.Serial('/dev/ttyAMA0', 9600) #ttyACM0

counter = -1
total   = 0

while True:

	a = ser.readline().split(' ')

	if len(a) > 2:
		temp = a[1]
                saveTemp = -1

		if temp != '' and temp.lstrip('-').replace('.','',1).isdigit():
			counter += 1
			total   += float(temp)

                	if counter == 0: # first run
                		saveTemp = round(total, 2)
			elif counter >= 200: # every 5 minutes
				saveTemp = round(total / counter, 2)

                	if saveTemp > -1:
				counter = 0
				total   = 0

				log_temperature(saveTemp)
				#log_temp_online(saveTemp)
				# log_temperature2(saveTemp)

	else:
		print "incorrect data: " + " ".join(a)
