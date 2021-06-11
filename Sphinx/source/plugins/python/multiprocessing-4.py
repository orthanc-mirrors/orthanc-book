import json
import multiprocessing
import orthanc
import requests
import signal

TOKEN = orthanc.GenerateRestApiAuthorizationToken()

def SlaveProcess():
    r = requests.get('http://localhost:8042/instances',
                     headers = { 'Authorization' : TOKEN })
    return json.dumps(r.json())

def Initializer():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

POOL = multiprocessing.Pool(4, initializer = Initializer)

def OnRest(output, uri, **request):
    answer = POOL.apply(SlaveProcess)
    output.AnswerBuffer(answer, 'text/plain')

orthanc.RegisterRestCallback('/computation', OnRest)
