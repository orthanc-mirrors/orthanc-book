import orthanc
import requests

TOKEN = orthanc.GenerateRestApiAuthorizationToken()

def OnRestArchive(output, uri, **request):
    study_id = request['groups'][0]
    print(f"Accessing archive for study: {study_id}")
    
    # put your business logic here

    with requests.get(f"http://localhost:8043/studies/{study_id}/archive", headers = { 'Authorization' : TOKEN }, stream = True) as r:
        output.StartStreamAnswer('application/zip')

        for buffer in r.iter_content(16*1024, False):
            print(len(buffer))
            output.SendStreamChunk(buffer)
    

orthanc.RegisterRestCallback('/studies/(.*)/my-archive', OnRestArchive)