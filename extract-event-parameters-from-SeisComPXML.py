import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sys
import os

def parse_seiscomp_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    namespace = {'seiscomp': 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.12'}

    data = []
    for origin in root.findall('.//seiscomp:origin', namespace):
        origin_data = {}
        for child in origin:
            if child.tag == '{http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.12}quality':
                for quality_child in child:
                    origin_data['quality_' + quality_child.tag.split('}')[-1]] = quality_child.text
            elif child.tag == '{http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.12}magnitude':
                magnitude_type = child.find('seiscomp:type', namespace).text
                magnitude_value = child.find('seiscomp:magnitude/seiscomp:value', namespace)
                if magnitude_value is not None:
                    origin_data[magnitude_type] = magnitude_value.text
                magnitude_uncertainty = child.find('seiscomp:magnitude/seiscomp:uncertainty', namespace)
                if magnitude_uncertainty is not None:
                    origin_data[magnitude_type+'_uncertainty'] = magnitude_uncertainty.text
                methodID_element = child.find('seiscomp:methodID', namespace)
                if methodID_element is not None:
                    origin_data[magnitude_type+'_methodID'] = methodID_element.text
                origin_data[magnitude_type+'_stationCount'] = child.find('seiscomp:stationCount', namespace).text
                creationInfo_author = child.find('seiscomp:creationInfo/seiscomp:author', namespace)
                if creationInfo_author is not None:
                    origin_data[magnitude_type+'_creationInfo_author'] = creationInfo_author.text
                creationInfo_creationTime = child.find('seiscomp:creationInfo/seiscomp:creationTime', namespace)
                if creationInfo_creationTime is not None:
                    origin_data[magnitude_type+'_creationInfo_creationTime'] = creationInfo_creationTime.text
            elif child.tag == '{http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.12}creationInfo':
                origin_data['creationInfo_author'] = child.find('seiscomp:author', namespace).text
                origin_data['creationInfo_creationTime'] = child.find('seiscomp:creationTime', namespace).text
                modificationTime_element = child.find('seiscomp:modificationTime', namespace)
                if modificationTime_element is not None:
                    origin_data['creationInfo_modificationTime'] = modificationTime_element.text
            else:
                value_element = child.find('seiscomp:value', namespace)
                if value_element is not None:
                    origin_data[child.tag.split('}')[-1]] = value_element.text

        data.append(origin_data)

    df = pd.DataFrame(data)

    # Sort the DataFrame based on 'creationInfo_creationTime'
    df = df.sort_values('creationInfo_creationTime')

    # Get the base name of the file (without extension)
    base_name = os.path.splitext(file)[0]
    # Create the output file name by appending '.csv' to the base name
    output_file = base_name + '.csv'

    df.to_csv(output_file, index=False)

# The XML file path is provided as a command-line argument
parse_seiscomp_xml(sys.argv[1])
