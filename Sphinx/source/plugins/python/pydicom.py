import io
import orthanc
import pydicom

def DecodeInstance(output, uri, **request):
    if request['method'] == 'GET':
        # Retrieve the instance ID from the regular expression (*)
        instanceId = request['groups'][0]
        # Get the content of the DICOM file
        f = orthanc.GetDicomForInstance(instanceId)
        # Parse it using pydicom
        dicom = pydicom.dcmread(io.BytesIO(f))
        # Return a string representation the dataset to the caller
        output.AnswerBuffer(str(dicom), 'text/plain')
    else:
        output.SendMethodNotAllowed('GET')

orthanc.RegisterRestCallback('/pydicom/(.*)', DecodeInstance)  # (*)
