import base64
import json
import requests

with open('sample.png', 'rb') as f:
    content = f.read()

pixelData = base64.b64encode(content).decode('ascii')

r = requests.post('http://localhost:8042/tools/create-dicom',
                  json.dumps({
                      'Content' : 'data:image/png;base64,%s' % pixelData,
                      'Tags' : {
                          'PatientName' : 'TEST',
                          'StudyDescription' : 'MY^STUDY',
                      }
                  }),
                  auth = requests.auth.HTTPBasicAuth('orthanc', 'orthanc'))
r.raise_for_status()

instanceId = r.json() ['ID']
print('ID of the newly created DICOM instance: %s' % instanceId)
