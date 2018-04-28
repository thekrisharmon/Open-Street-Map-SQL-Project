# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 21:18:45 2018
#######THIS WAS PULLED FROM THE CASE STUDY / LESSON 13 IN UDACITY########
I also used the following discussion boards from Udacity on the topic to help
me figure out the structure for the section of code I was required to write.
Additionally, I discussed this file at length with my WGU Course Mentors

Sources: https://discussions.udacity.com/t/converting-from-xml-to-csv/322696/6
         https://discussions.udacity.com/t/no-user-and-uid-in-a-node/170245
         https://discussions.udacity.com/t/p3-openstreetmap-overview/172045/5
         https://discussions.udacity.com/t/process-map-function/281683/3
         https://discussions.udacity.com/t/osm-to-csv-into-db/176734/12
         https://www.guru99.com/python-regular-expressions-complete-tutorial.html
@author: Kris
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus
import cleanCounty
import cleanCounty2
import StreetNameClean
import schema

#Below are the files I'll be using / creating to complete the cleaning prior to conversion from XML to CSV's
OSM_PATH = "kcmap.osm"
OSMFILE1 = "kcclean1.osm"
OSMFILE2 = "kcclean2.osm"
OSMFILE3 = "kcclean3.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    
    if element.tag == 'node': #checking out the node tags first
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]
#now I'm going through the attributes within each node tag to find and get them in the right location        
        for child in element: 
            childTags = {}
            if LOWER_COLON.match(child.attrib['k']):
                childTags['type'] = child.attrib['k'].split(':',1)[0]
                childTags['key'] = child.attrib['k'].split(':',1)[1]
                childTags['id'] = element.attrib['id']
                childTags['value'] = child.attrib['v']
                tags.append(childTags)
            elif PROBLEMCHARS.match(child.attrib['k']): #Ignoring problem characters per instructions.
                continue
            else:
                childTags['type'] = 'regular'
                childTags['key'] = child.attrib['k']
                childTags['id'] = element.attrib['id']
                childTags['value'] = child.attrib['v']
                tags.append(childTags)
        
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way': #checking out the way tags next
        for attrib in element.attrib:
            for attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]
        
        position = 0
        for child in element:
            childTags = {}
            childWayNodes = {}
#now I'm going through the attributes within each way tag to find the attributes and get them in the right location            
            if child.tag == 'tag':
                if LOWER_COLON.match(child.attrib['k']):
                    childTags['type'] = child.attrib['k'].split(':',1)[0]
                    childTags['key'] = child.attrib['k'].split(':',1)[1]
                    childTags['id'] = element.attrib['id']
                    childTags['value'] = child.attrib['v']
                    tags.append(childTags)
                elif PROBLEMCHARS.match(child.attrib['k']): #Ignoring problem characters per instructions.
                    continue
                else:
                    childTags['type'] = 'regular'
                    childTags['key'] = child.attrib['k']
                    childTags['id'] = element.attrib['id']
                    childTags['value'] = child.attrib['v']
                    tags.append(childTags)
                    
            elif child.tag == 'nd':
                childWayNodes['id'] = element.attrib['id']
                childWayNodes['node_id'] = child.attrib['ref']
                childWayNodes['position'] = position
                position += 1
                way_nodes.append(childWayNodes)
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    #cleaning the street anc county names first... then onto the process_map function
    StreetNameClean.cleanStreets(OSM_PATH,OSMFILE1)
    cleanCounty.cleanCounties(OSMFILE1,OSMFILE2)
    cleanCounty2.cleanCounties(OSMFILE2,OSMFILE3)
    process_map(OSMFILE3, validate=True)