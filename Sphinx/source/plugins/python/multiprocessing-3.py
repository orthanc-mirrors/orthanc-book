import pydicom
import io

def OffloadedDicomParsing(dicom):
    # No access to the "orthanc" library here, as we are in the slave process
    dataset = pydicom.dcmread(io.BytesIO(dicom))
    return str(dataset)

def OnRest(output, uri, **request):
    # The call to "orthanc.RestApiGet()" is only possible in the master process
    dicom = orthanc.RestApiGet('/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/file')
    answer = POOL.apply(OffloadedDicomParsing, args = (dicom, ))
    output.AnswerBuffer(answer, 'text/plain')
