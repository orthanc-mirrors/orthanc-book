.. _python-plugin:


Python plugin for Orthanc
=========================

.. contents::

Work-in-progress.

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
---------------------------------------

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
