# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 12:09:05 2018
My goal for this python file is to size up the counties listed in my data sample. I'm curious how many counties are covered and
if any data clean-up is needed at this point. I utilized my code from the StreetNameAudit.py file and modified it to look for
the county information.
@author: kharmon
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osmFile = open("kcsample.osm", "r")
# changed the 'S' to a 'D' to pull in the entire string from the tiger:county attribute
county_type_re = re.compile(r'\D+\.?$', re.IGNORECASE)
countyTypes = defaultdict(int)

def auditCountyType(countyTypes, countyName):
    counties = county_type_re.search(countyName)
    if counties:
        countyType = counties.group()

        countyTypes[countyType] += 1

def printSortedDict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)
#Looking for tags that have the attribute of 'tiger:county' so I can see the counties listed in my data sample
def is_county_name(element):
    return (element.tag == "tag") and (element.attrib['k'] == "tiger:county") #changed the focus to county instead of street name

def audit():
    for row, element in ET.iterparse(osmFile):
        if is_county_name(element):
            auditCountyType(countyTypes, element.attrib['v'])
    printSortedDict(countyTypes)

if __name__ == '__main__':
    audit()