from pycitibike import Citibike
import time
import psycopg2
import sys
import signal

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        con.close()
        sys.exit(0)

con = None

try:
     
    con = psycopg2.connect(host='localhost', database='citibike', user='citibike', password=sys.argv[1]) 
    cur = con.cursor()
    con.autocommit = True
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver    
    
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)

client = Citibike()

stations = {}
oldStations = {}

lastTime = 0

signal.signal(signal.SIGINT, signal_handler)

while True:

    
        start = time.time()
        
        try:
            stations = client.stations()
        except Exception as e:
            print e
            continue

        timestamp = psycopg2.TimestampFromTicks(time.time())
        print "Updating %s" % timestamp

        for station in stations:
                sid = station['id']
                if sid not in oldStations:
                        pass
                elif station['availableDocks'] != oldStations[sid]['availableDocks'] or station['availableBikes'] != oldStations[sid]['availableBikes']:
                        
                        sql = "insert into log(stationid, timestamp, availableBikes, availableDocks) values (%i, %s, %i, %i)" % (sid, timestamp, station['availableBikes'], station['availableDocks'])
                        # print sql
                        cur.execute(sql)

                oldStations[sid] = station

        end = time.time()
        runlength = int(end - start)
        cur.execute("insert into runlog(runlength) values(%i)" % runlength)



        time.sleep(30)