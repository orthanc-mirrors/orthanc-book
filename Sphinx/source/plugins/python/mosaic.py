import PIL.Image
import io
import json
import math
import orthanc

def generate_mosaic(output, uri, **request):
    # Sort the slices of the series, using the REST API of Orthanc
    seriesId = request['groups'][0]
    slices = json.loads(orthanc.RestApiGet('/series/%s/ordered-slices' % seriesId)) ['Slices']

    # Retrieve the first slice of the mosaic
    firstSliceBytes = orthanc.RestApiGet(slices[0] + '/preview')
    firstSliceDecoded = PIL.Image.open(io.BytesIO(firstSliceBytes))

    # Compute the size of the mosaic
    sliceWidth, sliceHeight = firstSliceDecoded.size
    side = math.ceil(math.sqrt(len(slices)))

    # Create a PIL image to store the mosaic
    image = PIL.Image.new(mode = 'L', size = (side * sliceWidth, side * sliceHeight))

    # Loop over the instances of the series to populate the mosaic
    x = 0
    y = 0
    for i in range(len(slices)):
        sliceBytes = orthanc.RestApiGet(slices[i] + '/preview')
        sliceDecoded = PIL.Image.open(io.BytesIO(sliceBytes))

        image.paste(sliceDecoded, (x * sliceWidth, y * sliceHeight))

        x += 1
        if x == side:
            x = 0
            y += 1

    # Answer with the mosaic encoded as a PNG image
    with io.BytesIO() as png:
        image.save(png, format = 'PNG')
        png.seek(0)
        output.AnswerBuffer(png.read(), 'image/png')

orthanc.RegisterRestCallback('/series/(.*)/mosaic', generate_mosaic)
