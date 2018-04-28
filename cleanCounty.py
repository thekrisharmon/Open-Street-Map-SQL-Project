
import xml.etree.cElementTree as ET


def isCountyName(elem):
    """check if elem is a county name"""
    return (elem.attrib['k'] == "tiger:county")

def getElement(osm_file, tags=('node', 'way', 'relation')):
#Source:http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python

    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for row, element in context:
        if row == 'end' and element.tag in tags:
            yield element
            root.clear()
        
def cleanCounties(filename,newfilename):   
#Sources: https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/files.html

    with open(filename, "rb") as infile, open(newfilename, "wb") as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<osm>\n  ')
        for element in getElement(infile):
            if element.tag == "node" or element.tag == "way": #only check way and node
                if element.find("tag") != -1:
                    for tag in element.iter("tag"): 
                        if isCountyName(tag):
                            countyName = tag.attrib['v']
                            if countyName.find(":"):
                                countyPos = countyName.find(":")
                                tag.attrib['v'] = countyName[:countyPos]

                     
            outfile.write(ET.tostring(element, encoding='utf-8')) 
        outfile.write('</osm>')
        