from flask import Flask, g
import sys
import json
import time
import psycopg2
from datetime import datetime
import pytz

app = Flask(__name__)

DBHOST = "localhost"
PORT = 8080

def connect_db():

	try:
	     
	    con = psycopg2.connect(host=DBHOST, database='citibike', user='citibike', password=sys.argv[1]) 
	    # cur = con.cursor()
	    con.autocommit = True
	    return con, con.cursor()
	    
	except psycopg2.DatabaseError, e:
	    print 'Error %s' % e    
	    sys.exit(1)

@app.before_request
def before_request():
	g.db, g.cur = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# def query_db(query, args=(), one=False):
# 	cur = get_db().execute(query, args)
# 	rv = cur.fetchall()
# 	cur.close()
# 	return (rv[0] if rv else None) if one else rv

# def getKnownStations():
# 	sql = "select id from stations"
# 	result = query_db(sql)

# 	knownStations = getattr(g, "_knownStations", None)
# 	if knownStations is None:
# 		knownStations = g._knownStations = []

# 		for entry in result:
# 			sid = int(entry['id'])
# 			knownStations.append(sid)
# 	return knownStations


# @app.route("/v0/timeline/<station>")
# def getTimeline(station):
	
# 	try: station = int(station)
# 	except: return "Station ID is invalid."

# 	if station not in getKnownStations():
# 		return "Station ID is invalid."

# 	outDict = {}

# 	sql = "select timestamp, availableBikes, availableDocks from stationlog where id = ? order by timestamp asc"
# 	try:
# 		result = query_db(sql, (str(station), ))
# 	except sqlite3.OperationalError, e:
# 		print "SQLite3 OperationalError:", e
# 		return "Error querying the database :("

# 	jout = json.dumps(result)
# 	return jout

@app.route("/v0/lastrun")
def getLastRun():

	sql = "select distinct timestamp from log order by timestamp desc limit 1"
	
	try:

		g.cur.execute(sql)
		result = g.cur.fetchone()[0]
		delta = datetime.now(pytz.utc) - result

		# result = query_db(sql)[0]['timestamp']
	except Exception, e:
		print "Exception: %s" % e
		return "Error"

	# timestamp = int(result)
	# delta = int(time.time() - timestamp)
	return "Last ran %s seconds ago" % delta

@app.route("/ver")
def version():
	sql = "SELECT version()"
	g.cur.execute(sql)
	ver = g.cur.fetchone()
	return ver

if __name__ == "__main__":


	app.debug = True
	app.run(host='0.0.0.0', port=PORT)
