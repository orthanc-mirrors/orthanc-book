import json
import orthanc

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:
        tags = {
            'SOPClassUID' : '1.2.840.10008.5.1.4.1.1.1',
            'PatientID' : 'HELLO',
            'PatientName' : 'WORLD',
        }

        with open('Lena.png', 'rb') as f:
            img = orthanc.UncompressImage(f.read(), orthanc.ImageFormat.PNG)

        s = orthanc.CreateDicom(json.dumps(tags), img, orthanc.CreateDicomFlags.GENERATE_IDENTIFIERS)

        with open('/tmp/sample.dcm', 'wb') as f:
            f.write(s)

        dicom = orthanc.CreateDicomInstance(s)
        frame = dicom.GetInstanceDecodedFrame(0)
        print('Size of the frame: %dx%d' % (frame.GetImageWidth(), frame.GetImageHeight()))

orthanc.RegisterOnChangeCallback(OnChange)
