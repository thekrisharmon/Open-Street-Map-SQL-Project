# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 21:19:24 2018
Sources:
    https://discussions.udacity.com/t/wrangle-openstreet-data-sql-queries/310013/2
    https://gist.github.com/carlward/54ec1c91b62a5f911c42#file-sample_project-md
    https://discussions.udacity.com/t/validating-a-complex-query-how-to-find-ids-with-a-missing-key/180994
    https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
    https://discussions.udacity.com/t/creating-db-file-from-csv-files-with-non-ascii-unicode-characters/174958
    https://discussions.udacity.com/t/difficulty-with-inserting-csv-file-and-sql-query/186125/3
    https://discussions.udacity.com/t/datatype-mismatch-issue-with-sql-import/199907
    https://discussions.udacity.com/t/osm-project-importing-csv-to-tables/177405
    https://discussions.udacity.com/t/final-project-data-wrangling-p3/195936/32
    https://docs.python.org/2.5/lib/sqlite3-Cursor-Objects.html
    
@author: Kris
"""

import csv, sqlite3

con = sqlite3.connect("kcmap.db")
con.text_factory = str
cur = con.cursor()

# Creating the nodes table here
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rb') as t:
    dictRead = csv.DictReader(t) 
    intoDB = [(e['id'], e['lat'], e['lon'], e['user'], e['uid'], e['version'], e['changeset'], e['timestamp']) \
             for e in dictRead]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", intoDB)
con.commit()

#Creating the nodes_tags table here
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as t:
    dictRead = csv.DictReader(t) 
    intoDB = [(e['id'], e['key'], e['value'], e['type']) for e in dictRead]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", intoDB)
con.commit()

#Creating the ways table here
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as t:
    dictRead = csv.DictReader(t) 
    intoDB = [(e['id'], e['user'], e['uid'], e['version'], e['changeset'], e['timestamp']) for e in dictRead]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", intoDB)
con.commit()

#Creating the ways_nodes table here
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as t:
    dictRead = csv.DictReader(t) 
    intoDB = [(e['id'], e['node_id'], e['position']) for e in dictRead]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", intoDB)
con.commit()

#Create the ways_tags table here
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as t:
    dictRead = csv.DictReader(t) 
    intoDB = [(e['id'], e['key'], e['value'], e['type']) for e in dictRead]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", intoDB)
con.commit()
con.close()