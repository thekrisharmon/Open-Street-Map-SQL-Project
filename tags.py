# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 22:11:02 2018
SOURCES:
    https://classroom.udacity.com/nanodegrees/nd002/parts/0021345404/modules/316820862075461/lessons/5436095827/concepts/54456296460923
    
@author: kris
"""
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter("tag"):
            k = tag.attrib['k']
            if lower.match(k):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.match(k):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.match(k):
                keys['problemchars'] = keys['problemchars'] + 1
                print k
            else:
                keys['other'] = keys['other'] + 1
        pass

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('kcsample.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    test()
