# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:08:07 2018
SOURCES:
    https://classroom.udacity.com/nanodegrees/nd002/parts/0021345404/modules/316820862075461/lessons/5436095827/concepts/54411202700923
@author: kris
"""

import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!
The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    userID = set()
    
    for _, element in ET.iterparse(filename):

        for tag in element.iter():
            if 'uid' in tag.attrib.keys():
                userID.add(tag.attrib['uid'])


    return len(userID)


def test():

    userID = process_map('kcsample.osm')
    pprint.pprint(userID)




if __name__ == "__main__":
    test()