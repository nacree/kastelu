import time
import sqlite3
import RPi.GPIO as GPIO
import sys

PIN=13

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)

def write_log(type,msg):
    conn=sqlite3.connect('/home/nacre/kastelu/temp.db')
    curs=conn.cursor()

    curs.execute("INSERT INTO log values(datetime('now', '+3 hours'), (?), (?))", (type, msg))
    print "{}: {}".format(type, msg)

    conn.commit()
    conn.close()

def get_stats():
    conn=sqlite3.connect('/home/nacre/kastelu/temp.db')
    curs=conn.cursor()

    curs.execute("""SELECT 1,datetime('now'),avg(temperature)
                    FROM temps
                    WHERE timestamp>datetime('now','-21 hours')
                    UNION
                    SELECT 2,*
                    FROM (
                         SELECT timestamp,temperature
                         FROM temps
                         ORDER BY timestamp DESC
                         LIMIT 1
                    )
                    ORDER BY 1""") # -21h because +3h difference in stored timestamp
    stats=curs.fetchall()
    conn.close()

    return stats

def use_pump(secs):
    # use pump for x seconds

    write_log("START","pump started for {} seconds".format(secs))
    GPIO.output(PIN, GPIO.HIGH)

    for i in range(secs):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    else:
        print

    write_log("STOP","pump stopped");
    GPIO.output(PIN, GPIO.LOW)

def get_pumptime(avg, last):

    Tmin = 15 # minimum temp
    Tmax = 30 # maxmimum temp

    xmin = 30 # minimum time to run
    xmax = 60 # maximum time to run

#   x-xmin    ( T - Tmin)
# --------- = ----------
# xmax-xmin   (Tmax-Tmin)

    T = avg
    x = (T-Tmin)*(xmax-xmin)/(Tmax-Tmin) + xmin

    return int(x)

def main(argv):

    if argv[0] == 'start':
        write_log("START","pump started manually")
        GPIO.output(PIN, GPIO.HIGH)

    elif argv[0] == 'stop':
        write_log("STOP","pump stopped manually")
        GPIO.output(PIN, GPIO.LOW)

    else:

        stats = get_stats()
        avg   = stats[0][1]
        last  = stats[1][1]

        write_log("STATS","avg={} last={}".format(avg,last))

        # control pump time

        secs = get_pumptime(avg, last)
        use_pump(secs)

if __name__ == "__main__":
   main(sys.argv[1:])
