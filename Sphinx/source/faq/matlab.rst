Interfacing with Matlab and Octave
==================================

Thanks to the REST API of Orthanc, it is easy to access DICOM images
from Matlab or Octave, as depicted in the following sample image:

.. image:: ../images/Matlab.png
           :align: center
           :width: 470px

Both Matlab and Octave have access to HTTP servers thanks to their
built-in `urlread() function
<http://nl.mathworks.com/help/matlab/ref/urlread.html>`__.  Once must
simply install a Matlab/Octave library to decode JSON files.  The
`JSONLab toolkit <https://github.com/fangq/jsonlab>`__ works perfectly
to this end.

.. highlight:: matlab

Using JSONlab, the following code will download and display a DICOM image::

  SERIES = 'ae164c84-e5bd0366-ba937a6d-65414092-f294d6b6';
  URL = 'http://demo.orthanc-server.com/';

  # Get information about the instances in this DICOM series
  instances = loadjson(urlread([ URL '/series/' SERIES '/instances' ]));

  # Select one slice from the series
  instance = instances(1,1).ID

  # Decode the slice with Orthanc thanks to the "/matlab" URI
  slice = eval(urlread([ URL '/instances/' instance '/matlab' ]));

  # Compute the maximum value in this slice
  max(max(slice))

  # Display the slice
  imagesc(slice)

  # Annotate the graph with the patient name and ID
  tags = loadjson(urlread([ URL '/instances/' instance '/tags?simplify' ]));
  title([ 'This is a slice from patient ' tags.PatientID ' (' tags.PatientName ')' ])
