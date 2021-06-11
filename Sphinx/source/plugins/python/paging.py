import json
import orthanc

def GetStudyDate(study):
    if 'StudyDate' in study['MainDicomTags']:
        return study['MainDicomTags']['StudyDate']
    else:
        return ''

def SortStudiesByDate(output, uri, **request):
    if request['method'] == 'GET':
        # Retrieve all the studies
        studies = json.loads(orthanc.RestApiGet('/studies?expand'))

        # Sort the studies according to the "StudyDate" DICOM tag
        studies = sorted(studies, key = GetStudyDate)

        # Read the limit/offset arguments provided by the user
        offset = 0
        if 'offset' in request['get']:
            offset = int(request['get']['offset'])

        limit = 0
        if 'limit' in request['get']:
            limit = int(request['get']['limit'])

        # Truncate the list of studies
        if limit == 0:
            studies = studies[offset : ]
        else:
            studies = studies[offset : offset + limit]

        # Return the truncated list of studies
        output.AnswerBuffer(json.dumps(studies), 'application/json')
    else:
        output.SendMethodNotAllowed('GET')

orthanc.RegisterRestCallback('/sort-studies', SortStudiesByDate)
