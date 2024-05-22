import base64
import json
import requests

with open('/tmp/model.nxz', 'rb') as f:
    nexus = f.read()

r = requests.post('http://localhost:8042/stl/create-nexus', json.dumps({
    'Content' : base64.b64encode(nexus).decode('ascii'),
    'Parent' : '66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e',
    'Tags' : {
        'SeriesDescription' : 'Nexus',

        # Some additional tags to make the DICOM file compliant according to dciodvfy
        'AcquisitionContextSequence' : [],
        'InstanceNumber' : '1',
        'Laterality' : '',
        'SeriesNumber' : '1',
    }
}))

r.raise_for_status()
instanceId = r.json() ['ID']
