# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:44:23 2018
I UTILIZED MY StreetNameClean.py FILE TO BUILD THIS ONE OUT
@author: Kris
"""

import xml.etree.cElementTree as ET
import re


county_type_re = re.compile(r'\D+\.?$', re.IGNORECASE)

# convert all "bad" county information to better ones using the dictionary below.
county_mapping = { 
                  "Atchison":"Atchison, KS",
                  "Atchison, K":"Atchison, KS",
                  "Bates, M":"Bates, MO",
                  "Benton, M":"Benton, MO",
                  "Buchanan, ":"Buchanan, MO",
                  "Buchanan, M":"Buchanan, MO",
                  "Caldwell, ":"Caldwell, MO",
                  "Caldwell, M":"Caldwell, MO",
                  "Carroll, ":"Carroll, MO",
                  "Carroll, M":"Carroll, MO",
                  "Cass, ":"Cass, MO",
                  "Cass, M":"Cass, MO",
                  "Clay, ":"Clay, MO",
                  "Clay, M":"Clay, MO",
                  "Clinton, ":"Clinton, MO",
                  "Clinton, M":"Clinton, MO",
                  "Cooper, M":"Cooper, MO",
                  "Douglas County, ":"Douglas, KS",
                  "Douglas, ":"Douglas, KS",
                  "Douglas, K":"Douglas, KS",
                  "Franklin, ":"Franklin, KS",
                  "Franklin, K":"Franklin, KS",
                  "Howard, M":"Howard, MO",
                  "Jackson, K":"Jackson, KS",
                  "Jackson, ":"Jackson, KS",
                  "Jackson, M":"Jackson, MO",
                  "Jefferson, ":"Jefferson, KS",
                  "Jefferson, K":"Jefferson, KS",
                  "Johnson, ":"Johnson, KS",
                  "Johnson, K":"Johnson, KS",
                  "Johnson, M":"Johnson, MO",
                  "Lafayette, ":"Lafayette, MO",
                  "Lafayette, M":"Lafayette, MO",
                  "Leavenworth, ":"Leavenworth, KS",
                  "Leavenworth, K":"Leavenworth, KS",
                  "Miami, ":"Miami, KS",
                  "Miami, K":"Miami, KS",
                  "Osage, K":"Osage, KS",
                  "Platte, ":"Platte, MO",
                  "Platte, M":"Platte, MO",
                  "Ray, ":"Ray, MO",
                  "Ray, M":"Ray, MO",
                  "Shawnee, K":"Shawnee, KS",
                  "Wyandotte, ":"Wyandotte, KS",
                  "Wyandotte, K":"Wyandotte, KS",
                  }

def isCountyName(element):
    return (element.tag == "tag") and (element.attrib['k'] == "tiger:county")
    
def betterName(name):
    countySearch = county_type_re.search(name)
    
    if countySearch:
        pattern = countySearch.group()
        if pattern in county_mapping:
            start_index = countySearch.start()
            name = name[:start_index] + county_mapping[pattern] 
        return name
    else:
        return name

   
def getElement(osm_file, tags=('node', 'way', 'relation')):
    """ Source:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, element in context:
        if event == 'end' and element.tag in tags:
            yield element
            root.clear()
        
def cleanCounties(filename,newfilename):   
    """Create a new xml file with all tag keys of street names and postcode updated"""
    with open(filename, "rb") as infile, open(newfilename, "wb") as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<osm>\n  ')
        for element in getElement(infile):
            if element.tag == "node" or element.tag == "way": #only check way and node
                if element.find("tag") != -1:
                    for tag in element.iter("tag"): 
                        if isCountyName(tag):
                            countyName = tag.attrib['v']
                            countyName = betterName(countyName)
                            tag.attrib['v'] = countyName                             
            outfile.write(ET.tostring(element, encoding='utf-8')) 
        outfile.write('</osm>')
        