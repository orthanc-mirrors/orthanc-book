from PIL import Image
import io
import orthanc

def DecodeInstance(output, uri, **request):
    if request['method'] == 'GET':
        # Retrieve the instance ID from the regular expression (*)
        instanceId = request['groups'][0]

        # Render the instance, then open it in Python using PIL/Pillow
        png = orthanc.RestApiGet('/instances/%s/rendered' % instanceId)
        image = Image.open(io.BytesIO(png))

        # Downsize the image as a 64x64 thumbnail
        image.thumbnail((64, 64), Image.ANTIALIAS)

        # Save the thumbnail as JPEG, then send the buffer to the caller
        jpeg = io.BytesIO()
        image.save(jpeg, format = "JPEG", quality = 80)
        jpeg.seek(0)
        output.AnswerBuffer(jpeg.read(), 'text/plain')

    else:
        output.SendMethodNotAllowed('GET')

orthanc.RegisterRestCallback('/pydicom/(.*)', DecodeInstance)  # (*)
