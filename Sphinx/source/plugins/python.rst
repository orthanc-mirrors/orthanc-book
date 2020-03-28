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


Rendering a thumbnail using PIL/Pillow
......................................

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


Performance and concurrency
---------------------------

.. highlight:: python

Let us consider the following sample Python script that makes a
CPU-intensive computation on a REST callback::

  import math
  import orthanc
  import time

  # CPU-intensive computation taking about 4 seconds
  def SlowComputation():
      start = time.time()
      for i in range(1000):
          for j in range(30000):
              math.sqrt(float(j))
      end = time.time()
      duration = (end - start)
      return 'computation done in %.03f seconds\n' % duration

  def OnRest(output, uri, **request):
      answer = SlowComputation()
      output.AnswerBuffer(answer, 'text/plain')

  orthanc.RegisterRestCallback('/computation', OnRest)


.. highlight:: text

Calling this REST route from the command-line returns the time that is
needed to compute 30 million times a squared root on your CPU::

  $ curl http://localhost:8042/computation
  computation done in 4.208 seconds

Now, let us call this route three times concurrently (we use bash)::

  $ (curl http://localhost:8042/computation & curl http://localhost:8042/computation & curl http://localhost:8042/computation )
  computation done in 11.262 seconds
  computation done in 12.457 seconds
  computation done in 13.360 seconds

As can be seen, the computation time has tripled. This means that the
computations were not distributed across the available CPU cores.
This might seem surprising, as Orthanc is a threaded server (in
Orthanc, a pool of C++ threads serves concurrent requests).

The explanation is that the Python interpreter (`CPython
<https://en.wikipedia.org/wiki/CPython>`__ actually) is built on the
top of a so-called `Global Interpreter Lock (GIL)
<https://en.wikipedia.org/wiki/Global_interpreter_lock>`__. The GIL is
basically a mutex that protects all the calls to the Python
interpreter. If multiple C++ threads from Orthanc call a Python
callback, only one can proceed at any given time.

.. highlight:: python

The solution is to use the `multiprocessing primitives
<https://docs.python.org/3/library/multiprocessing.html>`__ of Python.
The "master" Python interpreter that is initially started by the
Orthanc plugin, can start several `children processes
<https://en.wikipedia.org/wiki/Process_(computing)>`__, each of these
processes running a separate Python interpreter. This allows to
offload intensive computations from the "master" Python interpreter of
Orthanc onto those "slave" interpreters. The ``multiprocessing``
library is actually quite straightforward to use::

  import math
  import multiprocessing
  import orthanc
  import signal
  import time

  # CPU-intensive computation taking about 4 seconds
  # (same code as above)
  def SlowComputation():
      start = time.time()
      for i in range(1000):
          for j in range(30000):
              math.sqrt(float(j))
      end = time.time()
      duration = (end - start)
      return 'computation done in %.03f seconds\n' % duration

  # Ignore CTRL+C in the slave processes
  def Initializer():
      signal.signal(signal.SIGINT, signal.SIG_IGN)

  # Create a pool of 4 slave Python interpreters
  POOL = multiprocessing.Pool(4, initializer = Initializer)

  def OnRest(output, uri, **request):
      # Offload the call to "SlowComputation" onto one slave process.
      # The GIL is unlocked until the slave sends its answer back.
      answer = POOL.apply(SlowComputation)
      output.AnswerBuffer(answer, 'text/plain')

  orthanc.RegisterRestCallback('/computation', OnRest)

.. highlight:: text

Here is now the result of calling this route three times concurrently::

  $ (curl http://localhost:8042/computation & curl http://localhost:8042/computation & curl http://localhost:8042/computation )
  computation done in 4.211 seconds
  computation done in 4.215 seconds
  computation done in 4.225 seconds

As can be seen, the calls to the Python computation now fully run in
parallel (the time is cut down from 12 seconds to 4 seconds, the same
as for one isolated request).

Note also how the ``multiprocessing`` library allows to make a fine
control over the computational resources that are available to the
Python script: The number of "slave" interpreters can be easily
changed in the constructor of the ``multiprocessing.Pool`` object, and
are fully independent of the threads used by the Orthanc server.

.. highlight:: python

Very importantly, pay attention to the fact that only the "master"
Python interpreter has access to the Orthanc SDK. For instance, here
is how you would parse a DICOM file in a slave process::

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
      
Communication primitives such as ``multiprocessing.Queue`` are
available to exchange messages from the "slave" Python interpreters to
the "master" Python interpreter if further calls to the Orthanc SDK
are required.

Obviously, an in-depth discussion about the ``multiprocessing``
library is out of the scope of this document. There are many
references available on Internet. Also, note that ``multithreading``
is not useful here, as Python multithreading is also limited by the
GIL, and is more targeted at dealing with costly I/O operations.
