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
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.9.3/OrthancServer/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.

As of release 2.0 of the plugin, the coverage of the C SDK is about
75% (119 functions are automatically wrapped in Python out of a total
of 157 functions in the Orthanc SDK 1.7.2).


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

.. highlight:: python

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

**Note for OS X:** As indicated by `Stephen Douglas Scotti
<https://groups.google.com/g/orthanc-users/c/RnmZKFv8FaY/m/HhvOD2A2CAAJ>`__,
here is a sample invocation of CMake to force the version of Python to
be used on OS X::

  $ cmake .. -DPYTHON_VERSION=3.8 -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release \
          -DPYTHON_LIBRARY=/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/lib/libpython3.8.dylib \
          -DPYTHON_INCLUDE_DIR=/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/include/python3.8/
  
  
Microsoft Windows
.................

Pre-compiled binaries for Microsoft Windows `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-python>`__.

Beware that one version of the Python plugin can only be run against
one version of the Python interpreter. This version is clearly
indicated in the filename of the precompiled binaries.

.. highlight:: text

You are of course free to compile the plugin from sources. You'll have
to explicitly specify the path to your Python installation while
invoking CMake. For instance::

  C:\orthanc-python\Build> cmake .. -DPYTHON_VERSION=2.7 -DPYTHON_WINDOWS_ROOT=C:/Python27 \
                                    -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release -G "Visual Studio 15 2017"

**Note about debug builds**: Usually, building Python modules such as the Python 
plugin for Orthanc in debug mode (where ``_DEBUG`` is defined) leads to a module 
(``.exe`` or ``.dll``) that requires a debug build of Python, and debug versions of all
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

The precompiled binaries all use release (i.e. non-debug) versions of Python.


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


.. _python-changes:
  
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



.. warning::
   In releases <= 3.0 of the Python plugin, deadlocks might emerge if
   you call other core primitives of Orthanc (such as the REST API) in
   your callback function. This issue has been `fixed in release 3.1
   <https://hg.orthanc-server.com/orthanc-python/rev/46fe70776d61>`__.

As a **temporary workaround** against such deadlocks in releases <=
3.0, if you have to call other primitives of Orthanc, you should make
these calls in a separate thread, passing the pending events to be
processed through a message queue. Here is the template of a possible
solution to postpone such deadlocks as much as possible by relying on
the multithreading primitives of Python::

  import orthanc
  import threading

  def OnChange(changeType, level, resource):
      # One can safely invoke the "orthanc" module in this function
      orthanc.LogWarning("Hello world")
  
  def _OnChange(changeType, level, resource):
      # Invoke the actual "OnChange()" function in a separate thread
      t = threading.Timer(0, function = OnChange, args = (changeType, level, resource))
      t.start()

  orthanc.RegisterOnChangeCallback(_OnChange)


Beware that **this workaround is imperfect** and deadlocks have been
observed even if using it! Make sure to upgrade your plugin to solve
this issue for good. Note that this temporary workaround is not needed
in releases >= 3.1 of the plugin.

   

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


.. warning::
   Your callback function will be called synchronously with
   the core of Orthanc. This implies that deadlocks might emerge if
   you call other core primitives of Orthanc in your callback (such
   deadlocks are particular visible in the presence of other plugins
   or Lua scripts). It is thus strongly advised to avoid any call to
   the REST API of Orthanc in the callback. If you have to call other
   primitives of Orthanc, you should make these calls in a separate
   thread, passing the pending events to be processed through a
   message queue.
  

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
<stable-resources>` to a modality named ``samples`` (as declared in the
``DicomModalities`` configuration option)::
  
  import orthanc

  def OnChange(changeType, level, resourceId):
      if changeType == orthanc.ChangeType.STABLE_STUDY:
          print('Stable study: %s' % resourceId)
          orthanc.RestApiPost('/modalities/sample/store', resourceId)

  orthanc.RegisterOnChangeCallback(OnChange)


Note that, if you want to use an orthanc plugin to transfer the study,
you should use the ``RestApiPostAfterPlugins()`` method::

  import orthanc

  def OnChange(changeType, level, resourceId):
      if changeType == orthanc.ChangeType.STABLE_STUDY:
          print('Stable study: %s' % resourceId)
          orthanc.RestApiPostAfterPlugins('/dicom-web/servers/sample/store', resourceId)

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

.. highlight:: bash

Here is a sample call to retrieve all the studies that were last
updated in 2019 thanks to this Python script::

  $ curl http://localhost:8042/tools/find -d '{"Level":"Study","Query":{},"Expand":true,"Metadata":{"LastUpdate":"^2019.*$"}}'


.. _python-paging:

Implementing basic paging
.........................

.. highlight:: python

As explained in the FAQ, the :ref:`Orthanc Explorer interface is
low-level <improving-interface>`, and is not adapted for
end-users. One common need is to implement paging of studies, which
calls for server-side sorting of studies. This can be done using the
following sample Python plugin that registers a new route
``/sort-studies`` in the REST API of Orthanc::

 import json
 import orthanc

 def GetStudyDate(study):
     if 'StudyDate' in study['MainDicomTags']:
         return study['MainDicomTags']['StudyDate']
     else:
         return ''

 def SortStudiesByDate(output, uri, **request):
     if request['method'] == 'GET':
         # Retrieve all the studies
         studies = json.loads(orthanc.RestApiGet('/studies?expand'))

         # Sort the studies according to the "StudyDate" DICOM tag
         studies = sorted(studies, key = GetStudyDate)

         # Read the limit/offset arguments provided by the user
         offset = 0
         if 'offset' in request['get']:
             offset = int(request['get']['offset'])

         limit = 0
         if 'limit' in request['get']:
             limit = int(request['get']['limit'])

         # Truncate the list of studies
         if limit == 0:
             studies = studies[offset : ]
         else:
             studies = studies[offset : offset + limit]

         # Return the truncated list of studies
         output.AnswerBuffer(json.dumps(studies), 'application/json')
     else:
         output.SendMethodNotAllowed('GET')

 orthanc.RegisterRestCallback('/sort-studies', SortStudiesByDate)


.. highlight:: bash

Here is a sample call to this new REST route, that could be issued by
any JavaScript framework (the ``json_pp`` command-line pretty-prints a
JSON file)::

  $ curl http://localhost:8042/sort-studies | json_pp

This route also implement paging (i.e. it can limit and offset the
returned studies)::
  
  $ curl 'http://localhost:8042/sort-studies?offset=2&limit=2' | json_pp

Obviously, this basic sample can be improved in many ways. To improve
performance, one could for instance cache the result of
``/studies?expand`` in memory by :ref:`listening to changes
<python-changes>` in the list of studies
(cf. ``orthanc.ChangeType.NEW_STUDY`` and
``orthanc.ChangeType.DELETED``).


.. _python_excel:

Creating a Microsoft Excel report
.................................

.. highlight:: python

As Orthanc plugins have access to any installed Python module, it is
very easy to implement a server-side plugin that generates a report in
the Microsoft Excel ``.xls`` format. Here is a working example::

 import StringIO
 import json
 import orthanc
 import xlwt 
 
 def CreateExcelReport(output, uri, **request):
     if request['method'] != 'GET' :
         output.SendMethodNotAllowed('GET')
     else:
         # Create an Excel writer
         excel = xlwt.Workbook()
         sheet = excel.add_sheet('Studies')
 
         # Loop over the studies stored in Orthanc
         row = 0
         studies = orthanc.RestApiGet('/studies?expand')
         for study in json.loads(studies):
             sheet.write(row, 0, study['PatientMainDicomTags'].get('PatientID'))
             sheet.write(row, 1, study['PatientMainDicomTags'].get('PatientName'))
             sheet.write(row, 2, study['MainDicomTags'].get('StudyDescription'))
             row += 1
 
         # Serialize the Excel workbook to a string, and return it to the caller
         # https://stackoverflow.com/a/15649139/881731
         b = StringIO.StringIO()
         excel.save(b)       
         output.AnswerBuffer(b.getvalue(), 'application/vnd.ms-excel')

 orthanc.RegisterRestCallback('/report.xls', CreateExcelReport)

If opening the ``http://localhost:8042/report.xls`` URI, this Python
will generate a workbook with one sheet that contains the list of
studies, with the patient ID, the patient name and the study
description.


.. _python_authorization:

Forbid or allow access to REST resources (authorization, new in 3.0)
....................................................................

.. highlight:: python

The following Python script installs a callback that is triggered
whenever the HTTP server of Orthanc is accessed::

  import orthanc
  import pprint

  def Filter(uri, **request):
      print('User trying to access URI: %s' % uri)
      pprint.pprint(request)
      return True  # False to forbid access

  orthanc.RegisterIncomingHttpRequestFilter(Filter)

If access is not granted, the ``Filter`` callback must return
``False``. As a consequence, the HTTP status code would be set to
``403 Forbidden``. If access is granted, the ``Filter`` must return
``true``. The ``request`` argument contains more information about the
request (such as the HTTP headers, the IP address of the caller and
the GET arguments).

Note that this is similar to the ``IncomingHttpRequestFilter()``
callback that is available in :ref:`Lua scripts <lua-filter-rest>`.

Thanks to Python, it is extremely easy to call remote Web services for
authorization. Here is an example using the ``requests`` library::

  import json
  import orthanc
  import requests

  def Filter(uri, **request):
      body = {
          'uri' : uri,
          'headers' : request['headers']
      }
      r = requests.post('http://localhost:8000/authorize',
                        data = json.dumps(body))
      return r.json() ['granted']  # Must be a Boolean

  orthanc.RegisterIncomingHttpRequestFilter(Filter)

.. highlight:: javascript

This filter could be used together with the following Web service
implemented using `Node.js
<https://en.wikipedia.org/wiki/Node.js>`__::

  const http = require('http');

  const requestListener = function(req, res) {
    let body = '';
      req.on('data', function(chunk) {
      body += chunk;
    });
    req.on('end', function() {
      console.log(JSON.parse(body));
      var answer = {
        'granted' : false  // Forbid access
      };
      res.writeHead(200);
      res.end(JSON.stringify(answer));
    });
  }

  http.createServer(requestListener).listen(8000);

  
.. _python_create_dicom:

Creating DICOM instances (new in 3.2)
.....................................

.. highlight:: python

The following sample Python script will write on the disk a new DICOM
instance including the traditional Lena sample image, and will decode
the single frame of this DICOM instance::

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


.. _python_dicom_scp:

Handling DICOM SCP requests (new in 3.2)
........................................

.. highlight:: python

Starting with release 3.2 of the Python plugin, it is possible to
replace the C-FIND SCP and C-MOVE SCP of Orthanc by a Python
script. This feature can notably be used to create a custom DICOM
proxy. Here is a minimal example::

  import json
  import orthanc
  import pprint
  
  def OnFind(answers, query, issuerAet, calledAet):
      print('Received incoming C-FIND request from %s:' % issuerAet)
  
      answer = {}
      for i in range(query.GetFindQuerySize()):
          print('  %s (%04x,%04x) = [%s]' % (query.GetFindQueryTagName(i),
                                             query.GetFindQueryTagGroup(i),
                                             query.GetFindQueryTagElement(i),
                                             query.GetFindQueryValue(i)))
          answer[query.GetFindQueryTagName(i)] = ('HELLO%d-%s' % (i, query.GetFindQueryValue(i)))
  
      answers.FindAddAnswer(orthanc.CreateDicom(
          json.dumps(answer), None, orthanc.CreateDicomFlags.NONE))
  
  def OnMove(**request):
      orthanc.LogWarning('C-MOVE request to be handled in Python: %s' %
                         json.dumps(request, indent = 4, sort_keys = True))
  
  orthanc.RegisterFindCallback(OnFind)
  orthanc.RegisterMoveCallback(OnMove)

.. highlight:: text
  
In this sample, the C-FIND SCP will send one single answer that
reproduces the values provided by the SCU::

  $ findscu localhost 4242 -aet ORTHANC -S -k QueryRetrieveLevel=STUDY -k PatientName=TEST -k SeriesDescription=
  I: ---------------------------
  I: Find Response: 1 (Pending)
  I: 
  I: # Dicom-Data-Set
  I: # Used TransferSyntax: Little Endian Explicit
  I: (0008,0005) CS [ISO_IR 100]                             #  10, 1 SpecificCharacterSet
  I: (0008,0052) CS [HELLO0-STUDY]                           #  12, 1 QueryRetrieveLevel
  I: (0008,103e) LO [HELLO1- ]                               #   8, 1 SeriesDescription
  I: (0010,0010) PN [HELLO2-TEST ]                           #  12, 1 PatientName
  I: 

A more realistic Python script could for instance call the route
``/modalities/{...}/query`` in the :ref:`REST API <rest-find-scu>` of
Orthanc using ``orthanc.RestApiPost()``, in order to query the content
a remote modality through a second C-FIND SCU request (this time
issued by Orthanc as a SCU).
  
The C-MOVE SCP can be invoked as follows::
  
  $ movescu localhost 4242 -aem TARGET -aec LL -aet ORTHANC -S -k QueryRetrieveLevel=IMAGE -k StudyInstanceUID=1.2.3.4

The C-MOVE request above would print the following information in the
Orthanc logs::

  W0610 18:30:36.840865 PluginsManager.cpp:168] C-MOVE request to be handled in Python: {
      "AccessionNumber": "", 
      "Level": "INSTANCE", 
      "OriginatorAET": "ORTHANC", 
      "OriginatorID": 1, 
      "PatientID": "", 
      "SOPInstanceUID": "", 
      "SeriesInstanceUID": "", 
      "SourceAET": "LL", 
      "StudyInstanceUID": "1.2.3.4", 
      "TargetAET": "TARGET"
  }

It is now up to your Python callback to proces the C-MOVE SCU request,
for instance by calling the route ``/modalities/{...}/store`` in the
:ref:`REST API <rest-store-scu>` of Orthanc using
``orthanc.RestApiPost()``.
  
  

Performance and concurrency
---------------------------

**Important:** This section only applies to UNIX-like systems. The
``multiprocessing`` package will not work on Microsoft Windows as the
latter OS has a different model for `forking processes
<https://en.wikipedia.org/wiki/Fork_(system_call)>`__.

Using slave processes
.....................

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

Obviously, an in-depth discussion about the ``multiprocessing``
library is out of the scope of this document. There are many
references available on Internet. Also, note that ``threading`` is not
useful here, as Python multithreading is also limited by the GIL, and
is more targeted at dealing with costly I/O operations or with the
:ref:`scheduling of commands <python-scheduler>`.


Slave processes and the "orthanc" module
........................................

.. highlight:: python

Very importantly, pay attention to the fact that **only the "master"
Python interpreter has access to the Orthanc SDK**. The "slave"
processes have no access to the ``orthanc`` module.

You must write your Python plugin so as that all the calls to
``orthanc`` are moved from the slaves process to the master
process. For instance, here is how you would parse a DICOM file in a
slave process::

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
the "master" Python interpreter for more advanced scenarios.

NB: Starting with release 3.0 of the Python plugin, it is possible to
call the REST API of Orthanc from a slave process in a more direct
way. The function ``orthanc.GenerateRestApiAuthorizationToken()`` can
be used to create an authorization token that provides full access to
the REST API of Orthanc (without have to set credentials in your
plugin). Any HTTP client library for Python, such as `requests
<https://requests.readthedocs.io/en/master/>`__, can then be used to
access the REST API of Orthanc. Here is a minimal example::

  import json
  import multiprocessing
  import orthanc
  import requests
  import signal
  
  TOKEN = orthanc.GenerateRestApiAuthorizationToken()
  
  def SlaveProcess():
      r = requests.get('http://localhost:8042/instances',
                       headers = { 'Authorization' : TOKEN })
      return json.dumps(r.json())
  
  def Initializer():
      signal.signal(signal.SIGINT, signal.SIG_IGN)
  
  POOL = multiprocessing.Pool(4, initializer = Initializer)
  
  def OnRest(output, uri, **request):
      answer = POOL.apply(SlaveProcess)
      output.AnswerBuffer(answer, 'text/plain')
  
  orthanc.RegisterRestCallback('/computation', OnRest)
