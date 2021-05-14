# discovery-api-python-sample
Sample script for using the JDisc Discovery API using Python

## JDisc library

Library that contains some common functions required for connecting and logon in directory jdisc

cd jdisc
python setup.py build
python setup.py install


## Use Cases

### extract-sbom.py

Get list of applications for the devices of a given network and generate a software bill of material (SBOM) 
in the form of a CylconeDX file

### extract-rmon-log.py

Get RMON logfile using custom SNMP data collection and output to stdout or file

### upload-device.py

Upload device using upload API
