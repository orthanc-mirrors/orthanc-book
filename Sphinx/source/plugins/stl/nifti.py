import base64
import json
import requests

with open('colon.nii.gz', 'rb') as f:
    nifti = f.read()

r = requests.post('http://localhost:8042/stl/encode-nifti', json.dumps({
    'Nifti' : 'data:application/octet-stream;base64,' + base64.b64encode(nifti).decode('ascii'),
    'ParentStudy' : '6ed7e8a4-60deff42-5e22a424-2128629f-158d0b3a',
    'Smooth' : True,
    'Resolution' : 256,
}))

r.raise_for_status()
instanceId = r.json() ['ID']
