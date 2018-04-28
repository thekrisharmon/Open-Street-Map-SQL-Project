# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
'''
Sources: 
    https://www.debuggex.com/cheatsheet/regex/python 
    https://www.youtube.com/watch?v=sa-TUpSx1JA
    https://docs.python.org/3.2/library/re.html
    https://discussions.udacity.com/t/lesson-3-8-example-using-our-blueprint/158483/2
'''

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# add "Street" to any numbered street names   
street_number_re = re.compile(r'((1\s*st)|(2\s*nd)|(3\s*rd)|([0,4,5,6,7,8,9]\s*th))$')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Alley","Plaza","Commons","Broadway","Expressway","Terrace","Center","Circle",
            "Crescent","Highway","Way"]

# convert all "bad" street names to better ones using the dictionary below.
street_mapping = { 
                  "Ave":"Avenue",
                  "Ave.":"Avenue",
                  "Avene":"Avenue",
                  "Aveneu":"Avenue",
                  "ave":"Avenue",
                  "avenue":"Avenue",
                  "Blv.":"Boulevard",
                  "Blvd":"Boulevard",
                  "blvd":"Boulevard",
                  "Broadway.":"Broadway",
                  "circle":"Circle",
                  "ct":"Court",
                  "cCourt":"Court",
                  "Ctr":"Center",
                  "dr":"Drive",
                  "Dr.":"Drive",
                  "Dr":"Drive",
                  "Pkwy":"Parkway",
                  "Plz":"Plaza",
                  "Rd":"Road",
                  "ST":"Street",
                  "St":"Street",
                  "St.":"Street",
                  "Steet":"Street",
                  "Streeet":"Street",
                  "st":"Street",
                  "street":"Street"
                  }



def isStreetName(element):
    return (element.attrib['k'] == "addr:street")
    
def betterName(name):
    numberSearch = street_number_re.search(name)
    typeSearch = street_type_re.search(name)
    
    if numberSearch and ('street' not in name and 'Street' not in name): # adding "Street" to the end of numbered roads (e.g. - 5th Street)
        pattern = numberSearch.group()
        start_index = numberSearch.start()
        length = len(pattern)
        end_index = start_index + length
        name = name[:end_index] + ' Street'    
        return name
    elif typeSearch:
        pattern = typeSearch.group()
        if pattern in street_mapping:
            start_index = typeSearch.start()
            name = name[:start_index] + street_mapping[pattern] 
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
        
def cleanStreets(filename,newfilename):   
    """Create a new xml file with all tag keys of street names and postcode updated"""
    with open(filename, "rb") as infile, open(newfilename, "wb") as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<osm>\n  ')
        for element in getElement(infile):
            if element.tag == "node" or element.tag == "way": #only check way and node
                if element.find("tag") != -1:
                    for tag in element.iter("tag"): 
                        if isStreetName(tag):
                            streetName = tag.attrib['v']
                            streetName = betterName(streetName)
                            tag.attrib['v'] = streetName                             
            outfile.write(ET.tostring(element, encoding='utf-8')) 
        outfile.write('</osm>')
