import json
import pprint
import requests

INSTANCE = '19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5'
OVERWRITE_INSTANCES = True   # Whether the "OverwriteInstance" is set to "true" in the Orthanc config

r = requests.post('http://localhost:8042/instances/%s/modify' % INSTANCE, json.dumps({
    'Replace' : {
        'PatientName' : 'Hello'
    },
    'Keep' : [ 'SOPInstanceUID' ],  # Don't generate a new SOPInstanceUID
    'Force' : True                  # Mandatory if SOPInstanceUID must be kept constant
    }))

r.raise_for_status()

dicom = r.content

if not OVERWRITE_INSTANCES:
    r = requests.delete('http://localhost:8042/instances/%s' % INSTANCE)
    r.raise_for_status()

r = requests.post('http://localhost:8042/instances', dicom)
r.raise_for_status()
pprint.pprint(r.json())
