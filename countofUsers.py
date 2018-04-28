# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:45:04 2018

@author: kharmon
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
from operator import itemgetter # soure: https://stackoverflow.com/questions/11228812/print-a-dict-sorted-by-values

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!
The function process_map should return a set of unique user IDs ("uid")
"""

osmfile = "kcsample.osm"

def get_user(element):
    if element.tag in ["node", "way", "relation"]:
        return element.attrib["user"]
    else:
        return None

def get_all_users(filename):
    users = defaultdict(int)
    for _, element in ET.iterparse(filename):
        uid = get_user(element)
        if(uid):
            users[uid] += 1
    for k, v in sorted(users.items(), key=itemgetter(1), reverse=True):
        if v >= 50: #there are a ton of users listed, so looking for those who make 50 or more changes in the data
            print k, v
#    return users


print(get_all_users(osmfile))