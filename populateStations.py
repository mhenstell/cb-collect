import psycopg2
from pycitibike import Citibike
import sys
import datetime

con = None

try:
     
    con = psycopg2.connect(host='107.170.20.187', database='citibike', user='citibike', password=sys.argv[1]) 
    cur = con.cursor()
    con.autocommit = True
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver    
    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)


client = Citibike()
stations = client.fullStations()

for station in stations:

        sid = int(station['id'])
        lat = float(station['latitude'])
        longg = float(station['longitude'])
        label = station['label']
        sstatus = station['status']
        if sstatus == "Active": status = "True"
        else: status = "False"

        sql = """insert into stations(id, lat, long, label, status) values(%i, %f, %f, '%s', %s)""" % (sid, lat, longg, label, status)
        
        print sql
        cur.execute(sql)

# sid = int(sys.argv[1])

# sql = "select * from stationlog where id = %i order by timestamp asc" % sid
# cur.execute(sql)
# data = cur.fetchall()

# for point in data:
#         timestamp = point[1]
#         timestamp = datetime.datetime.fromtimestamp(timestamp)
#         bikes = point[2]
#         docks = point[3]

#         print timestamp, bikes, docks