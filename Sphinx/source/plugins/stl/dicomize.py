import base64
import json
import requests

with open('liver.stl', 'rb') as f:
    stl = f.read()

r = requests.post('http://localhost:8042/tools/create-dicom', json.dumps({
    'Content' : 'data:model/stl;base64,%s' % base64.b64encode(stl).decode('ascii'),
    'Parent' : '6ed7e8a4-60deff42-5e22a424-2128629f-158d0b3a',
    'Tags' : {
        'SeriesDescription' : 'Liver'
    }
}))

r.raise_for_status()
instanceId = r.json() ['ID']
