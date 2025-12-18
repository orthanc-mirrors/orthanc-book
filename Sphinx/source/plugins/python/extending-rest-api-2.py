import orthanc
import pprint
import json

# override the /instances POST route
def OnInstances(output, uri, **request):
    
    # for POST, replace the core API route by your own implementation
    if request['method'] == 'POST':
        orthanc.LogWarning('I have received an instance')
        # implement your own logic here
        output.AnswerBuffer(json.dumps({"MyAnswer": "Instance Ignored"}), "application/json")
    else:
        # for GET, simply forward the call to the core API.
        # Note that you should not use RestApiGetAfterPlugins here since
        # this would call the /instances route from this python plugin
        # and end up in an infinite loop.
        instances = orthanc.RestApiGet(uri)
        output.AnswerBuffer(instances, "application/json")

# reimplement a DICOMweb /studies/../metadata route
def OnDicomWebStudiesMetadata(output, uri, **request):
    
    orthanc.LogWarning("My DICOMWEB /studies/../metadata")

    # since we are calling a route from a plugin, we must use RestApiGetAfterPlugins
    metadata = json.loads(orthanc.RestApiGetAfterPlugins(uri.replace('/my-dicom-web/', '/dicom-web/')))
    
    # transform the metadata (remove all tags from group 0009)
    for m in metadata:
        tags_to_remove = [k for k in m if k.startswith('0009')]
        for k in tags_to_remove:
            del m[k]

    output.AnswerBuffer(json.dumps(metadata), "application/json")


# override the /instances route from the core API
orthanc.RegisterRestCallback('/instances', OnInstances)

# The code below should be avoided since you actually don't know which route will finally be called:
# the one from the DICOMweb plugin or the one from this python plugin
# orthanc.RegisterRestCallback('/dicom-web/studies/(.*)/metadata', OnDicomWebStudiesMetadata)

# Therefore, you should use another base route to differentiate it from the DICOMweb plugin route
orthanc.RegisterRestCallback('/my-dicom-web/studies/(.*)/metadata', OnDicomWebStudiesMetadata)
