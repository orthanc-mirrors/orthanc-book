import json
import requests

r = requests.post('http://localhost:8042/stl/encode-rtstruct', json.dumps({
    'Instance' : 'f0dc2345-8f627774-f66083ae-a14d781e-1187b513',  # ID of the RT-STRUCT DICOM instance
    'RoiNames' : [ 'Lung_L', 'Lung_R' ],
    'Smooth' : True,
    'Resolution' : 256
}))

r.raise_for_status()
instanceId = r.json() ['ID']
