import json
import orthanc
import re

# Get the path in the REST API to the given resource that was returned
# by a call to "/tools/find"
def GetPath(resource):
    if resource['Type'] == 'Patient':
        return '/patients/%s' % resource['ID']
    elif resource['Type'] == 'Study':
        return '/studies/%s' % resource['ID']
    elif resource['Type'] == 'Series':
        return '/series/%s' % resource['ID']
    elif resource['Type'] == 'Instance':
        return '/instances/%s' % resource['ID']
    else:
        raise Exception('Unknown resource level')

def FindWithMetadata(output, uri, **request):
    # The "/tools/find" route expects a POST method
    if request['method'] != 'POST':
        output.SendMethodNotAllowed('POST')
    else:
        # Parse the query provided by the user, and backup the "Expand" field
        query = json.loads(request['body'])

        if 'Expand' in query:
            originalExpand = query['Expand']
        else:
            originalExpand = False

        # Call the core "/tools/find" route
        query['Expand'] = True
        answers = orthanc.RestApiPost('/tools/find', json.dumps(query))

        # Loop over the matching resources
        filteredAnswers = []
        for answer in json.loads(answers):
            try:
                # Read the metadata that is associated with the resource
                metadata = json.loads(orthanc.RestApiGet('%s/metadata?expand' % GetPath(answer)))

                # Check whether the metadata matches the regular expressions
                # that were provided in the "Metadata" field of the user request
                isMetadataMatch = True
                if 'Metadata' in query:
                    for (name, pattern) in query['Metadata'].items():
                        if name in metadata:
                            value = metadata[name]
                        else:
                            value = ''

                        if re.match(pattern, value) == None:
                            isMetadataMatch = False
                            break

                # If all the metadata matches the provided regular
                # expressions, add the resource to the filtered answers
                if isMetadataMatch:
                    if originalExpand:
                        answer['Metadata'] = metadata
                        filteredAnswers.append(answer)
                    else:
                        filteredAnswers.append(answer['ID'])
            except:
                # The resource was deleted since the call to "/tools/find"
                pass

        # Return the filtered answers in the JSON format
        output.AnswerBuffer(json.dumps(filteredAnswers, indent = 3), 'application/json')

orthanc.RegisterRestCallback('/tools/find', FindWithMetadata)
