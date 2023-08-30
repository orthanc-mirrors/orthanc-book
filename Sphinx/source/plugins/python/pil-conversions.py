import json
import PIL.Image
import PIL.ImageDraw
import orthanc

URL = 'http://hg.orthanc-server.com/orthanc-tests/raw-file/Orthanc-1.11.0/Database/LenaTwiceWithFragments.dcm'
USERNAME = ''
PASSWORD = ''

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:

        # (1) Download a sample DICOM instance and decode it
        orthanc.LogWarning('Downloading: %s' % URL)
        lena = orthanc.HttpGet(URL, USERNAME, PASSWORD)

        dicom = orthanc.CreateDicomInstance(lena)
        orthanc.LogWarning('Number of frames: %d' % dicom.GetInstanceFramesCount())

        # (2) Access the first frame of the instance as a PIL image
        frame = dicom.GetInstanceDecodedFrame(0)
        size = (frame.GetImageWidth(), frame.GetImageHeight())

        if frame.GetImagePixelFormat() == orthanc.PixelFormat.RGB24:
            mode = 'RGB'
        else:
            raise Exception('Unsupported pixel format')

        image = PIL.Image.frombuffer(mode, size, frame.GetImageBuffer(), 'raw', mode, 0, 1)

        # (3) Draw a red cross over the PIL image
        draw = PIL.ImageDraw.Draw(image)
        draw.line((0, 0) + image.size, fill=(255,0,0), width=10)
        draw.line((0, image.size[1], image.size[0], 0), fill=(255,0,0), width=10)

        # (4) Convert back the modified PIL image to an Orthanc image
        buf = image.tobytes()
        a = orthanc.CreateImageFromBuffer(frame.GetImagePixelFormat(), image.size[0], image.size[1],
                                          len(buf) // image.size[1], buf)

        # (5) Create and upload a new DICOM instance with the modified frame
        tags = {
            'SOPClassUID' : '1.2.840.10008.5.1.4.1.1.1',
            'PatientID' : 'HELLO',
            'PatientName' : 'WORLD',
        }

        s = orthanc.CreateDicom(json.dumps(tags), a, orthanc.CreateDicomFlags.GENERATE_IDENTIFIERS)
        orthanc.RestApiPost('/instances', s)
        orthanc.LogWarning('Image successfully modified and uploaded!')

orthanc.RegisterOnChangeCallback(OnChange)
