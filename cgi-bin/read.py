#!/home/squalaob/virtualenv/kaori.squarepotato.com/2.7/bin/python
import sqlite3
import json

db = sqlite3.connect('math.db')
cursor = db.cursor()

query = "SELECT * FROM answers"
cursor.execute(query)
rows = cursor.fetchall()
db.close()

jsonData = json.dumps(rows)
print "Status: 200 OK"
print "Content-Type: application/json"
print "Length:", len(jsonData)
print
print jsonData
