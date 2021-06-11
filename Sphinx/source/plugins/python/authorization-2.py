import json
import orthanc
import requests

def Filter(uri, **request):
    body = {
        'uri' : uri,
        'headers' : request['headers']
    }
    r = requests.post('http://localhost:8000/authorize',
                      data = json.dumps(body))
    return r.json() ['granted']  # Must be a Boolean

orthanc.RegisterIncomingHttpRequestFilter(Filter)
