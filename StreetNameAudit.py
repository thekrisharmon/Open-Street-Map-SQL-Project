
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
'''
    SOURCES:
        https://discussions.udacity.com/t/auditing-street-names-unicode-problem/351420/9
        https://docs.python.org/2/library/xml.etree.elementtree.html
        https://www.python-course.eu/lambda.php
        https://stackoverflow.com/questions/13669252/what-is-key-lambda
        
'''
osmFile = open("kcsample.osm", "r")

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
streetTypes = defaultdict(int)

#Finding and counting the street names or "types"
def audit_street_type(streetTypes, streetName):
    streets = street_type_re.search(streetName)
    if streets:
        street_type = streets.group()
        streetTypes[street_type] += 1

#using this to print the sorted dictionary
def printSortedDict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda word: word.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)

#Using this to verify if the tag is actually the street name attribute
def isStreetName(element):
    return (element.tag == "tag") and (element.attrib['k'] == "addr:street")

#doing the actual auditing here
def audit():
    for row, element in ET.iterparse(osmFile):
        if isStreetName(element):
            audit_street_type(streetTypes, element.attrib['v'])
    printSortedDict(streetTypes)

if __name__ == '__main__':
    audit()