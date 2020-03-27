.. _python-plugin:


Python plugin for Orthanc
=========================

.. contents::

Work-in-progress.

Being a plugin, the Python API has access to more features than
:ref:`Lua scripts <lua>`.

The Python API is automatically generated from the `Orthanc plugin SDK
in C
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.5.7/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.  The coverage of the C SDK is about 75% (105 functions are
automatically wrapped in Python out of a total of 139 functions in C).


Samples
-------

Extending the REST API
......................

.. highlight:: python

Here is a basic Python script that registers two new routes in the
REST API::

  import orthanc
  import pprint

  def OnRest(output, uri, **request):
      pprint.pprint(request)
      print('Accessing uri: %s' % uri)
      output.AnswerBuffer('ok\n', 'text/plain')
    
  orthanc.RegisterRestCallback('/(to)(t)o', OnRest)
  orthanc.RegisterRestCallback('/tata', OnRest)

.. highlight:: json

Here is the associated minimal configuration file for Orthanc
(provided the Python script is saved as ``rest.py``)::

  {
    "Plugins" : [ "." ],
    "PythonScript" : "rest.py",
    "PythonVerbose" : false
  }

.. highlight:: bash

The route can then be accessed as::

  $ curl http://localhost:8042/toto
  ok

  
Listening to changes
....................

.. highlight:: python

This sample uploads a DICOM file as soon as Orthanc is started::

   import orthanc

   def OnChange(changeType, level, resource):
       if changeType == orthanc.ChangeType.ORTHANC_STARTED:
           print('Started')

           with open('/tmp/sample.dcm', 'rb') as f:
               orthanc.RestApiPost('/instances', f.read())
        
        elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:
            print('Stopped')

        elif changeType == orthanc.ChangeType.NEW_INSTANCE:
            print('A new instance was uploaded: %s' % resource)

    orthanc.RegisterOnChangeCallback(OnChange)


Accessing the content of a new instance
.......................................

.. highlight:: python

::
   
  import orthanc
  import json
  import pprint

  def OnStoredInstance(dicom, instanceId):
      print('Received instance %s of size %d (transfer syntax %s, SOP class UID %s)' % (
          instanceId, dicom.GetInstanceSize(),
          dicom.GetInstanceMetadata('TransferSyntax'),
          dicom.GetInstanceMetadata('SopClassUid')))

      # Print the origin information
      if dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.DICOM_PROTOCOL:
          print('This instance was received through the DICOM protocol')
      elif dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.REST_API:
          print('This instance was received through the REST API')

      # Print the DICOM tags
      pprint.pprint(json.loads(dicom.GetInstanceSimplifiedJson()))

  orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)


Calling pydicom
...............

.. highlight:: python

Here is a sample Python plugin that registers a REST callback to dump
the content of the dataset of one given DICOM instance stored in
Orthanc, using `pydicom <https://pydicom.github.io/>`__::
  
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

.. highlight:: bash

This can be called as follows::
  
  $ curl http://localhost:8042/pydicom/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5
  

Auto-routing studies
....................

.. highlight:: python

Here is a sample Python plugin that routes any :ref:`stable study
<lua-callbacks>` to a modality named ``samples`` (as declared in the
``DicomModalities`` configuration option)::
  
  import orthanc

  def OnChange(changeType, level, resourceId):
      if changeType == orthanc.ChangeType.STABLE_STUDY:
          print('Stable study: %s' % resourceId)
          orthanc.RestApiPost('/modalities/sample/store', resourceId)

  orthanc.RegisterOnChangeCallback(OnChange)


Render a thumbnail using PIL/Pillow
...................................

.. highlight:: python

::
   
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
