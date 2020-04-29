.. _python-plugin:


Python plugin for Orthanc
=========================

.. contents::

   
Overview
--------
   
This plugin can be used to write :ref:`Orthanc plugins
<creating-plugins>` using the `Python programming language
<https://en.wikipedia.org/wiki/Python_(programming_language)>`__
instead of the more complex C/C++ programming languages.

Python plugins have access to more features and a more consistent SDK
than :ref:`Lua scripts <lua>`. The Python API is automatically
generated from the `Orthanc plugin SDK in C
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.5.7/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.

As of initial release 1.0 of the plugin, the coverage of the C SDK is
about 75% (105 functions are automatically wrapped in Python out of a
total of 139 functions in the Orthanc SDK 1.5.7).


Source code
-----------
   
* Link to the `official releases of this plugin
  <https://www.orthanc-server.com/browse.php?path=/plugin-python>`__.

* Link to the `code repository
  <https://hg.orthanc-server.com/orthanc-python/>`__.

  
Licensing
---------

Pay attention to the fact that this plugin is licensed under the terms
of the `AGPL license
<https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License>`__.

This has an important consequence: If you distribute Orthanc to
clients together with one Python script, or if you put an Orthanc
server equipped with one Python script on a Web portal, you **must**
disclose the source code of your Python script to the Orthanc
community under the terms of the AGPL license.

We suggest you to put the source code of your Python scripts on the
dedicated `"OrthancContributed" repository on GitHub
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__,
and/or to send it to the `Orthanc Users
<https://groups.google.com/forum/#!forum/orthanc-users>`__ discussion
group.

Check out the :ref:`FAQ about licensing <licensing>` for more context.


Usage
-----

Docker
......

.. highlight:: json

The most direct way of starting Orthanc together with the Python
plugin is through :ref:`Docker <docker>`. Let's create the file
``/tmp/hello.py`` that contains the following basic Python script::

  print('Hello world!')

.. highlight:: json

Let's also create the file ``/tmp/orthanc.json`` that contains the
following minimal :ref:`configuration for Orthanc <configuration>`::
                 
  {
    "StorageDirectory" : "/var/lib/orthanc/db",
    "RemoteAccessAllowed" : true,
    "Plugins" : [ 
      "/usr/local/share/orthanc/plugins"
    ],
    "PythonScript" : "/etc/orthanc/hello.py"
  }
    
.. highlight:: bash

Given these two files, Orthanc can be started as follows::
               
  $ docker run -p 4242:4242 -p 8042:8042 --rm \
    -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro \
    -v /tmp/hello.py:/etc/orthanc/hello.py:ro \
    jodogne/orthanc-python

.. highlight:: text

You'll see the following excerpt in the log, which indicates that the Python plugin is properly loaded::

  W0331 15:48:12.990661 PluginsManager.cpp:269] Registering plugin 'python' (version mainline)
  W0331 15:48:12.990691 PluginsManager.cpp:168] Python plugin is initializing
  W0331 15:48:12.990743 PluginsManager.cpp:168] Using Python script "hello.py" from directory: /etc/orthanc
  W0331 15:48:12.990819 PluginsManager.cpp:168] Program name: /usr/local/sbin/Orthanc
  Hello world!


`Here <https://bitbucket.org/osimis/orthanc-setup-samples/src/master/docker/python/>`__ is a full example
of a more complex setup using the :ref:`osimis/orthanc <docker-osimis>` images.

Compiling from source
.....................

.. highlight:: bash

The procedure to compile this plugin from source is similar to that
for the :ref:`core of Orthanc <compiling>`. The following commands
should work for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DPYTHON_VERSION=3.7 -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

Before running CMake, make sure that the Python interpreter and its
associated development library are installed. On Ubuntu 18.04 LTS, you
would for instance install packages ``libpython3.7-dev`` and
``python3.7``.
   
The compilation will produce the shared library ``OrthancPython``,
that can be loaded by properly setting the ``Plugins``
:ref:`configuration option <configuration>` of Orthanc.

**Warning:** The shared library is only compatible with the Python
interpreter whose version corresponds to the value of the
``PYTHON_VERSION`` argument that was given to CMake.
     
  
Microsoft Windows
.................

Pre-compiled binaries for Microsoft Windows `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-python>`__.

Beware that one version of the Python plugin can only be run against
one version of the Python interpreter. This version is clearly
indicated in the name of the folder.

As of release 1.0, the Orthanc project only provides pre-compiled
binaries for Microsoft Windows 32bit and Python 2.7. Even though this
version of Python is not supported anymore, it can still run on all
the versions of Microsoft Windows that have been released for more
than 10 years.

.. highlight:: text

You are of course free to compile the plugin from sources if you need
a more recent version. You'll have to explicitly specify the path to
your Python installation while invoking CMake. For instance::

  C:\orthanc-python\Build> cmake .. -DPYTHON_VERSION=2.7 -DPYTHON_WINDOWS_ROOT=C:/Python27 \
                                    -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release -G "Visual Studio 15 2017"

**Note about debug builds**: usually, building Python modules such as the Python 
plugin for Orthanc in debug mode (where ``_DEBUG`` is defined) leads to a module 
(.exe or .dll) that requires a debug build of Python, and debug versions of all
the Python libraries. This is quite cumbersome, for it requires building Python
on your own or downloading additional debug files.

Since using a debug build of Python is only necessary in very specific cases 
(such as the debugging of code at the boundary between Python and an extension),
we have changed the default behavior to use the release Python library by default.

This means that you are able to build this plugin in debug mode with the 
standard Python distribution.

In case you need to use the Python debug libraries, you can instruct the build
system to do so by setting the ``PYTHON_WINDOWS_USE_RELEASE_LIBS`` CMake option,
that is ``ON`` by default, to ``OFF``. The previous build example would then be,
should you require a full debug build::

  C:\orthanc-python\Build> cmake .. -DPYTHON_VERSION=2.7 -DPYTHON_WINDOWS_ROOT=C:/Python27 \
                                    -DSTATIC_BUILD=ON -DPYTHON_WINDOWS_USE_RELEASE_LIBS=OFF \
                                    -DCMAKE_BUILD_TYPE=Debug -G "Visual Studio 15 2017"

Please note that this CMake option only impacts **debug** builds under Windows, 
when using (any version of) the Microsoft Visual Studio compiler.

Configuration options
---------------------

The only two configuration options that are available for this plugin
are the following:

* ``PythonScript`` indicates where the Python script is located.  If
  this configuration option is not provided, the Python plugin is not
  started.

* ``PythonVerbose`` is a Boolean value to make the Python interpreter
  verbose.
  

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


.. _python-introspection:

Inspecting the available API
............................

.. highlight:: python

Thanks to Python's introspection primitives, it is possible to inspect
the API of the ``orthanc`` module in order to dump all the available
features::

  import inspect
  import numbers
  import orthanc

  # Loop over the members of the "orthanc" module
  for (name, obj) in inspect.getmembers(orthanc):
      if inspect.isroutine(obj):
          print('Function %s():\n  Documentation: %s\n' % (name, inspect.getdoc(obj)))

      elif inspect.isclass(obj):
          print('Class %s:\n  Documentation: %s' % (name, inspect.getdoc(obj)))

          # Loop over the members of the class
          for (subname, subobj) in inspect.getmembers(obj):
              if isinstance(subobj, numbers.Number):
                  print('  - Enumeration value %s: %s' % (subname, subobj))
              elif (not subname.startswith('_') and
                    inspect.ismethoddescriptor(subobj)):
                  print('  - Method %s(): %s' % (subname, inspect.getdoc(subobj)))
          print('')


.. _python-scheduler:

Scheduling a task for periodic execution
........................................

.. highlight:: python

The following Python script will periodically (every second) run the
function ``Hello()`` thanks to the ``threading`` module::

  import orthanc
  import threading

  TIMER = None

  def Hello():
      global TIMER
      TIMER = None
      orthanc.LogWarning("In Hello()")
      # Do stuff...
      TIMER = threading.Timer(1, Hello)  # Re-schedule after 1 second
      TIMER.start()

  def OnChange(changeType, level, resource):
      if changeType == orthanc.ChangeType.ORTHANC_STARTED:
          orthanc.LogWarning("Starting the scheduler")
          Hello()

      elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:
          if TIMER != None:
              orthanc.LogWarning("Stopping the scheduler")
              TIMER.cancel()

  orthanc.RegisterOnChangeCallback(OnChange)


.. _python-metadata:

Filtering and returning metadata
................................

Besides the main DICOM tags, Orthanc associates some metadata to each
resource it stores (this includes the date of last update, the
transfer syntax, the remote AET...). People are often interested in
getting such metadata while calling the ``/tools/find`` route in the
:ref:`REST API <rest-find>`, or even in filtering this metadata the
same way they look for DICOM tags.

This feature is not built in the core of Orthanc, as metadata is not
indexed in the Orthanc database, contrarily to the main DICOM
tags. Filtering metadata requires a linear search over all the
matching resources, which induces a cost in the performance.

.. highlight:: python

Nevertheless, here is a full sample Python script that overwrites the
``/tools/find`` route in order to give access to metadata::

  import json
  import orthanc
  import re

  # Get the path in the REST API to the given resource that was returned
  # by a call to "/tools/find"
  def GetPath(resource):
      if resource['Type'] == 'Patient':
          return '/patients/%s' % resource['ID']
      elif resource['Type'] == 'Study':
          return '/studies/%s' % resource['ID']
      elif resource['Type'] == 'Series':
          return '/series/%s' % resource['ID']
      elif resource['Type'] == 'Instance':
          return '/instances/%s' % resource['ID']
      else:
          raise Exception('Unknown resource level')

  def FindWithMetadata(output, uri, **request):
      # The "/tools/find" route expects a POST method
      if request['method'] != 'POST':
          output.SendMethodNotAllowed('POST')
      else:
          # Parse the query provided by the user, and backup the "Expand" field
          query = json.loads(request['body'])       

          if 'Expand' in query:
              originalExpand = query['Expand']
          else:
              originalExpand = False

          # Call the core "/tools/find" route
          query['Expand'] = True
          answers = orthanc.RestApiPost('/tools/find', json.dumps(query))

          # Loop over the matching resources
          filteredAnswers = []
          for answer in json.loads(answers):
              try:
                  # Read the metadata that is associated with the resource
                  metadata = json.loads(orthanc.RestApiGet('%s/metadata?expand' % GetPath(answer)))

                  # Check whether the metadata matches the regular expressions
                  # that were provided in the "Metadata" field of the user request
                  isMetadataMatch = True
                  if 'Metadata' in query:
                      for (name, pattern) in query['Metadata'].items():
                          if name in metadata:
                              value = metadata[name]
                          else:
                              value = ''

                          if re.match(pattern, value) == None:
                              isMetadataMatch = False
                              break

                  # If all the metadata matches the provided regular
                  # expressions, add the resource to the filtered answers
                  if isMetadataMatch:
                      if originalExpand:
                          answer['Metadata'] = metadata
                          filteredAnswers.append(answer)
                      else:
                          filteredAnswers.append(answer['ID'])
              except:
                  # The resource was deleted since the call to "/tools/find"
                  pass

          # Return the filtered answers in the JSON format
          output.AnswerBuffer(json.dumps(filteredAnswers, indent = 3), 'application/json')

  orthanc.RegisterRestCallback('/tools/find', FindWithMetadata)


**Warning:** In the sample above, the filtering of the metadata is
done using Python's `library for regular expressions
<https://docs.python.org/3/library/re.html>`__. It is evidently
possible to adapt this script in order to use the DICOM conventions
about `attribute matching
<http://dicom.nema.org/medical/dicom/2019e/output/chtml/part04/sect_C.2.2.2.html>`__.

.. highlight:: python

Here is a sample call to retrieve all the studies that were last
updated in 2019 thanks to this Python script::

  $ curl http://localhost:8042/tools/find -d '{"Level":"Study","Query":{},"Expand":true,"Metadata":{"LastUpdate":"^2019.*$"}}'


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
callback, only one can proceed at any given time. Note however that
the GIL only applies to the Python script: The baseline REST API of
Orthanc is not affected by the GIL.

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
references available on Internet. Also, note that ``threading`` is not
useful here, as Python multithreading is also limited by the GIL, and
is more targeted at dealing with costly I/O operations or with the
:ref:`scheduling of commands <python-scheduler>`.
