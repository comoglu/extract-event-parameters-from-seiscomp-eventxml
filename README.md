```markdown
# SeisComP XML Parser

This Python script parses Seiscomp XML files and extracts relevant data into a pandas DataFrame. The DataFrame is then sorted based on the 'creationInfo_creationTime' field and saved as a CSV file.

## Dependencies

The script requires the following Python libraries:
- xml.etree.ElementTree
- pandas
- numpy
- sys
- os

## Usage

The script takes one command-line argument, which is the path to the Seiscomp XML file to be parsed. 

```bash
python parse_seiscomp_xml.py /path/to/your/file.xml
```

The script will output a CSV file in the same directory as the input XML file. The output file will have the same base name as the input file, but with a '.csv' extension.

## Data

The script extracts the following data from the XML file:

- Quality parameters
- Magnitude parameters (including type, value, uncertainty, methodID, stationCount, creationInfo_author, creationInfo_creationTime)
- CreationInfo parameters (including author, creationTime, modificationTime)

Each of these parameters is saved as a column in the output DataFrame.

## Note

This script is designed to work with Seiscomp XML files that conform to the 'http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.12' namespace.
```
