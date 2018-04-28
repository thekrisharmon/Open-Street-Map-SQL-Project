# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 21:08:13 2018
SOURCES:
    https://discussions.udacity.com/t/validating-a-complex-query-how-to-find-ids-with-a-missing-key/180994
    https://discussions.udacity.com/t/wrangle-openstreet-data-sql-queries/310013/3
    https://discussions.udacity.com/t/sqlite-number-of-user-contributions-query/198564
    https://www.systutorials.com/241542/how-to-get-file-size-in-python/
    http://thepythonguru.com/fetching-results/
    https://docs.python.org/2/library/sqlite3.html
    https://stackoverflow.com/questions/9545637/sql-order-by-count
@author: Kris
"""

"""
Queries
"""

import sqlite3
import os
from hurry.filesize import size

con = sqlite3.connect("kcmap.db")
cur = con.cursor()


def fileSizes():
    filesToUse = ['kcmap.osm','kcmap.db','nodes.csv','nodes_tags.csv','ways.csv','ways_tags.csv','ways_nodes.csv']
    for f in filesToUse:
        print(f+" file is " + size(os.path.getsize(f)) + ".")

def grabaRow():
    rows = []
    for row in cur.execute('SELECT * FROM nodes \
                           LIMIT 10'):
        rows.append(row)
    return rows

def countCounties():
    counties =[]
    for row in cur.execute('SELECT value, COUNT(*) from ways_tags \
                         WHERE key="county" \
                         GROUP BY value \
                         ORDER BY COUNT(*) DESC'):
        counties.append(row)
    return counties

def topStreet():
	streets = []
	for row in cur.execute('SELECT value, COUNT(*) FROM nodes_tags \
                        WHERE key="street" \
                        GROUP BY value \
                        ORDER BY COUNT(*) DESC'):
		streets.append(row)
	return streets[:11]

def countCities():
    cities = []
    for row in cur.execute('SELECT value, COUNT(*) from ways_tags \
            WHERE key="city" AND type="addr" \
            GROUP BY value \
            ORDER BY COUNT(*) DESC \
            LIMIT 10'):
		cities.append(row)
    return cities

def numberUniqueStreets():
    result = cur.execute('SELECT COUNT(DISTINCT(value)) \
                         FROM nodes_tags \
                         WHERE key="street"')
    return result.fetchone()[0]

def numberOfNodes():
	result = cur.execute('SELECT COUNT(*) FROM nodes')
	return result.fetchone()[0]

def numberOfWays():
	result = cur.execute('SELECT COUNT(*) FROM ways')
	return result.fetchone()[0]
    
def topUsers():
	users = []
	for row in cur.execute('SELECT top.user, COUNT(*) as number \
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) top \
            GROUP BY top.user \
            ORDER BY number DESC \
            LIMIT 10'):
		users.append(row)
	return users

def trafficTech():
    traffic = []
    for row in cur.execute('SELECT value, COUNT(*) FROM nodes_tags \
            WHERE key="highway" \
            GROUP BY value \
            ORDER BY COUNT(*) DESC \
            LIMIT 10'):
        traffic.append(row)
    return traffic
