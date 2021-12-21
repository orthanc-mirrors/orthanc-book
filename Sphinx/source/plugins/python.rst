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
than :ref:`Lua scripts <lua>`. The largest part of the Python API is
automatically generated from the `Orthanc plugin SDK in C
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.9.7/OrthancServer/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.

As of release 3.2 of the plugin, the coverage of the C SDK is about
87% (138 functions are automatically wrapped in Python out of a total
of 158 functions from the Orthanc SDK 1.8.1).


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


Microsoft Windows
.................

Pre-compiled binaries for Microsoft Windows `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-python>`__.

Beware that one version of the Python plugin can only be run against
one version of the Python interpreter. This version is clearly
indicated in the filename of the precompiled binaries.  

Pay also attention to pick the right 32/64 bits version.  If you are
running Orthanc 64bits, install Python in 64bits and select the 64bits
Python plugin too.

When you install Python on your Windows machine, make sure to install
Python for ``All Users`` and select the ``Add Python to Path`` option.

Compiling from source
.....................

For GNU/Linux
^^^^^^^^^^^^^

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
  
  
For Microsoft Windows
^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

You are of course free to compile the plugin from sources. You'll have
to explicitly specify the path to your Python installation while
invoking CMake. For instance::

  C:\orthanc-python\Build> cmake .. -DPYTHON_VERSION=3.8 -DPYTHON_WINDOWS_ROOT=C:/Python38 \
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

  C:\orthanc-python\Build> cmake .. -DPYTHON_VERSION=3.8 -DPYTHON_WINDOWS_ROOT=C:/Python38 \
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

Here is a basic Python script that registers two new routes in the
REST API:

.. literalinclude:: python/extending-rest-api.py
                    :language: python

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

This sample uploads a DICOM file as soon as Orthanc is started:

.. literalinclude:: python/listening-changes.py
                    :language: python


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
the multithreading primitives of Python:

.. literalinclude:: python/changes-deadlock-3.0.py
                    :language: python

Beware that **this workaround is imperfect** and deadlocks have been
observed even if using it! Make sure to upgrade your plugin to solve
this issue for good. Note that this temporary workaround is not needed
in releases >= 3.1 of the plugin.

   

Accessing the content of a new instance
.......................................

.. literalinclude:: python/accessing-new-instance.py
                    :language: python

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

Here is a sample Python plugin that registers a REST callback to dump
the content of the dataset of one given DICOM instance stored in
Orthanc, using `pydicom <https://pydicom.github.io/>`__:

.. literalinclude:: python/pydicom.py
                    :language: python

.. highlight:: bash

This callback can be called as follows::
  
  $ curl http://localhost:8042/pydicom/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5
  

Auto-routing studies
....................

Here is a sample Python plugin that routes any :ref:`stable study
<stable-resources>` to a modality named ``samples`` (as declared in the
``DicomModalities`` configuration option):
  
.. literalinclude:: python/autorouting-1.py
                    :language: python

Note that, if you want to use an orthanc plugin to transfer the study,
you should use the ``RestApiPostAfterPlugins()`` method:

.. literalinclude:: python/autorouting-2.py
                    :language: python
                               

Rendering a thumbnail using PIL/Pillow
......................................

.. literalinclude:: python/pil.py
                    :language: python


.. _python-introspection:

Inspecting the available API
............................

Thanks to Python's introspection primitives, it is possible to inspect
the API of the ``orthanc`` module in order to dump all the available
features:

.. literalinclude:: python/inspect-api.py
                    :language: python

                               
.. _python-scheduler:

Scheduling a task for periodic execution
........................................

The following Python script will periodically (every second) run the
function ``Hello()`` thanks to the ``threading`` module:

.. literalinclude:: python/periodic-execution.py
                    :language: python


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

Nevertheless, here is a full sample Python script that overwrites the
``/tools/find`` route in order to give access to metadata:

.. literalinclude:: python/filtering-metadata.py
                    :language: python


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

As explained in the FAQ, the :ref:`Orthanc Explorer interface is
low-level <improving-interface>`, and is not adapted for
end-users. One common need is to implement paging of studies, which
calls for server-side sorting of studies. This can be done using the
following sample Python plugin that registers a new route
``/sort-studies`` in the REST API of Orthanc:

.. literalinclude:: python/paging.py
                    :language: python

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

As Orthanc plugins have access to any installed Python module, it is
very easy to implement a server-side plugin that generates a report in
the Microsoft Excel ``.xls`` format. Here is a working example:

.. literalinclude:: python/excel.py
                    :language: python

If opening the ``http://localhost:8042/report.xls`` URI, this Python
will generate a workbook with one sheet that contains the list of
studies, with the patient ID, the patient name and the study
description.


.. _python_authorization:

Forbid or allow access to REST resources (authorization, new in 3.0)
....................................................................

The following Python script installs a callback that is triggered
whenever the HTTP server of Orthanc is accessed:

.. literalinclude:: python/authorization-1.py
                    :language: python


If access is not granted, the ``Filter`` callback must return
``False``. As a consequence, the HTTP status code would be set to
``403 Forbidden``. If access is granted, the ``Filter`` must return
``true``. The ``request`` argument contains more information about the
request (such as the HTTP headers, the IP address of the caller and
the GET arguments).

Note that this is similar to the ``IncomingHttpRequestFilter()``
callback that is available in :ref:`Lua scripts <lua-filter-rest>`.

Thanks to Python, it is extremely easy to call remote Web services for
authorization. Here is an example using the ``requests`` library:

.. literalinclude:: python/authorization-2.py
                    :language: python

This filter could be used together with the following Web service
implemented using `Node.js
<https://en.wikipedia.org/wiki/Node.js>`__:

.. literalinclude:: python/authorization-node-service.js
                    :language: javascript

  
.. _python_lookup_dictionary:

Lookup DICOM dictionary (new in 3.2)
....................................

Python plugins can access the dictionary of the DICOM tags that are
handled by Orthanc:

.. literalinclude:: python/lookup-dictionary.py
                    :language: python

.. highlight:: text

Note how Python introspection is used in order to map the values in
enumeration ``orthanc.ValueRepresentation`` to a string description of
the value representation. If started, the plugin above would output
the following information in the Orthanc logs::

  W0611 14:04:08.563957 PluginsManager.cpp:168] Entry in the dictionary: {
      "Element": 32, 
      "Group": 16, 
      "MaxMultiplicity": 1, 
      "MinMultiplicity": 1, 
      "ValueRepresentation": 11
  }
  W0611 14:04:08.563975 PluginsManager.cpp:168] Name of the value representation: LO


.. _python_create_dicom:

Creating DICOM instances (new in 3.2)
.....................................

The following sample Python script will write on the disk a new DICOM
instance including the traditional Lena sample image, and will decode
the single frame of this DICOM instance:

.. literalinclude:: python/create-dicom.py
                    :language: python


.. _python_pil_conversions:

Conversions between Orthanc and Python images (new in 3.2)
..........................................................

The Python method ``orthanc.Image.GetImageBuffer()`` returns a copy of
the memory buffer of an image that is handled Orthanc. Conversely, the
Python function ``orthanc.CreateImageFromBuffer()`` can be used to
create an Orthanc image from a Python buffer. Taken together, these
two functions can be used to do bidirectional conversions between
Orthanc images and Python images.

Here is a full working example using PIL/Pillow that shows how to
decode one frame of a DICOM instance using Orthanc, then to modify
this image using PIL, and finally to upload the modified image as a
new DICOM instance:

.. literalinclude:: python/pil-conversions.py
                    :language: python


.. _python_dicom_scp:

Handling DICOM SCP requests (new in 3.2)
........................................

Starting with release 3.2 of the Python plugin, it is possible to
replace the C-FIND SCP and C-MOVE SCP of Orthanc by a Python
script. This feature can notably be used to create a custom DICOM
proxy. Here is a minimal example:

.. literalinclude:: python/dicom-find-move-scp.py
                    :language: python


.. highlight:: text
  
In this sample, the C-FIND SCP will send one single answer that
reproduces the values provided by the SCU::

  $ findscu localhost 4242 -S -k QueryRetrieveLevel=STUDY -k PatientName=TEST -k SeriesDescription=
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
  
  $ movescu localhost 4242 -aem TARGET -aec SOURCE -aet MOVESCU -S -k QueryRetrieveLevel=IMAGE -k StudyInstanceUID=1.2.3.4

The C-MOVE request above would print the following information in the
Orthanc logs::

  W0610 18:30:36.840865 PluginsManager.cpp:168] C-MOVE request to be handled in Python: {
      "AccessionNumber": "", 
      "Level": "INSTANCE", 
      "OriginatorAET": "MOVESCU", 
      "OriginatorID": 1, 
      "PatientID": "", 
      "SOPInstanceUID": "", 
      "SeriesInstanceUID": "", 
      "SourceAET": "SOURCE", 
      "StudyInstanceUID": "1.2.3.4", 
      "TargetAET": "TARGET"
  }

It is now up to your Python callback to process the C-MOVE SCU request,
for instance by calling the route ``/modalities/{...}/store`` in the
:ref:`REST API <rest-store-scu>` of Orthanc using
``orthanc.RestApiPost()``. It is highly advised to create a Python
thread to handle the request, in order to avoid blocking Orthanc as
much as possible.


.. _python_worklists:

Handling worklist SCP requests (new in 3.2)
...........................................

Starting with release 3.2 of the Python plugin, it is possible to
answer :ref:`worklist queries <worklist>` using a Python script. This
is especially useful to easily create a bridge between Orthanc,
HL7/FHIR messages and RIS systems. Indeed, Python provides many tools
to handle HL7 such as `python-hl7 library
<https://python-hl7.readthedocs.io/en/latest/>`__.

The following Python script reproduces features similar to the
:ref:`sample modality worklists plugin <worklists-plugin>`:

.. literalinclude:: python/worklist.py
                    :language: python

.. highlight:: text
  
Here is the result of this plugin on a sample call::

  $ findscu -W -k "ScheduledProcedureStepSequence[0].Modality=MR" 127.0.0.1 4242
  I: ---------------------------
  I: Find Response: 1 (Pending)
  I: 
  I: # Dicom-Data-Set
  I: # Used TransferSyntax: Little Endian Explicit
  I: (0008,0005) CS [ISO_IR 100]                             #  10, 1 SpecificCharacterSet
  I: (0040,0100) SQ (Sequence with explicit length #=1)      #  18, 1 ScheduledProcedureStepSequence
  I:   (fffe,e000) na (Item with explicit length #=1)          #  10, 1 Item
  I:     (0008,0060) CS [MR]                                     #   2, 1 Modality
  I:   (fffe,e00d) na (ItemDelimitationItem for re-encoding)   #   0, 0 ItemDelimitationItem
  I: (fffe,e0dd) na (SequenceDelimitationItem for re-encod.) #   0, 0 SequenceDelimitationItem
  I: 
  I: ---------------------------
  I: Find Response: 2 (Pending)
  I: 
  I: # Dicom-Data-Set
  I: # Used TransferSyntax: Little Endian Explicit
  I: (0008,0005) CS [ISO_IR 100]                             #  10, 1 SpecificCharacterSet
  I: (0040,0100) SQ (Sequence with explicit length #=1)      #  18, 1 ScheduledProcedureStepSequence
  I:   (fffe,e000) na (Item with explicit length #=1)          #  10, 1 Item
  I:     (0008,0060) CS [MR]                                     #   2, 1 Modality
  I:   (fffe,e00d) na (ItemDelimitationItem for re-encoding)   #   0, 0 ItemDelimitationItem
  I: (fffe,e0dd) na (SequenceDelimitationItem for re-encod.) #   0, 0 SequenceDelimitationItem
  I:


.. _pynetdicom:

Replacing DICOM SCP of Orthanc by pynetdicom
............................................

.. highlight:: json

Thanks to Python plugins, it is also possible to replace the built-in
DICOM SCP of Orthanc by `pynetdicom
<https://pydicom.github.io/pynetdicom/stable/examples/storage.html>`__
so as to customize how the DICOM protocol is handled. Firstly, in the
configuration file, make sure to disable the Orthanc SCP by setting
``DicomServerEnabled`` to ``false``::

  {
    "Plugins" : [ "." ],
    "PythonScript" : "pynetdicom.py",
    "DicomServerEnabled" : false
  }

Secondly, here a basic plugin illustrating how to start and stop the
pynetdicom server, and handle incoming C-STORE requests:

.. literalinclude:: python/pynetdicom.py
                    :language: python

As can be seen in this listing, whenever the pynetdicom receives an
incoming C-STORE request, it makes a POST call to the URI
``/instances`` in the REST API of Orthanc in order to store the
embedded DICOM dataset into Orthanc. Obviously, one can build more
complex DICOM servers by handling more messages than C-STORE alone.


.. _python_exception:

Catching exceptions
...................

Starting with release 3.3 of the Python plugin, the plugin generates a
Python exception derived from class ``orthanc.OrthancException`` if an
error is encountered. This exception contains a tuple that provides
the error code and its textual description.

In releases <= 3.2, the Python plugin raised the `built-in exception
<https://docs.python.org/3/library/exceptions.html>`__ ``ValueError``.

Here is an example showing how to catch exceptions:

.. literalinclude:: python/exception.py
                    :language: python


.. _python_storage_area:

Implementing a custom storage area (new in 3.3)
...............................................

Starting with release 3.3 of the Python plugin, it is possible to
replace the built-in storage area of Orthanc (that writes
:ref:`attachments <metadata>` onto the filesystem in the
``OrthancStorage`` folder by default), by providing 3 Python callbacks
to the ``orthanc.RegisterStorageArea()`` function:

* The first callback indicates how to **create** an attachment into
  the storage area.

* The second callback indicates how to **read** an attachment from the
  storage area.

* The third callback indicates how to **remove** an attachment out of
  the storage area.

This feature can be used to quickly and easily interface Orthanc with
any `object-based storage
<https://en.wikipedia.org/wiki/Object_storage>`__ technology available
in Python (such as `Ceph
<https://en.wikipedia.org/wiki/Ceph_(software)>`__ or AWS S3-like
tools). The performance will not be as good as a C/C++ native plugin
(cf. the :ref:`cloud storage <object-storage>`, the :ref:`PostgreSQL
<postgresql>` and the :ref:`MySQL <mysql>` plugins), but it can be
used for prototyping or for basic setups.

Here is a full, self-explaining sample:

.. literalinclude:: python/storage-area.py
                    :language: python

The ``contentType`` can be used to apply a special treatment to some
types of attachments (typically, DICOM instances). This parameter
takes its values from the ``orthanc.ContentType`` enumeration.


.. _python_received_instance:

Modifying received instances (new in 3.5 - not released yet)
...........................................

Starting with release 3.5 of the Python plugin, it is possible to
modify instances received by Orthanc before they are stored in
the storage.  This is usually easier to perform modification at this
stage compared to using the ``/modify`` route once the instances
has been stored.

.. literalinclude:: python/received-instance-callback.py
                    :language: python



Performance and concurrency
---------------------------

**Important:** This section only applies to UNIX-like systems. The
``multiprocessing`` package will not work on Microsoft Windows as the
latter OS has a different model for `forking processes
<https://en.wikipedia.org/wiki/Fork_(system_call)>`__.

Using slave processes
.....................

Let us consider the following sample Python script that makes a
CPU-intensive computation on a REST callback:

.. literalinclude:: python/multiprocessing-1.py
                    :language: python

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

The solution is to use the `multiprocessing primitives
<https://docs.python.org/3/library/multiprocessing.html>`__ of Python.
The "master" Python interpreter that is initially started by the
Orthanc plugin, can start several `children processes
<https://en.wikipedia.org/wiki/Process_(computing)>`__, each of these
processes running a separate Python interpreter. This allows to
offload intensive computations from the "master" Python interpreter of
Orthanc onto those "slave" interpreters. The ``multiprocessing``
library is actually quite straightforward to use:

.. literalinclude:: python/multiprocessing-2.py
                    :language: python

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

Very importantly, pay attention to the fact that **only the "master"
Python interpreter has access to the Orthanc SDK**. The "slave"
processes have no access to the ``orthanc`` module.

You must write your Python plugin so as that all the calls to
``orthanc`` are moved from the slaves process to the master
process. For instance, here is how you would parse a DICOM file in a
slave process:

.. literalinclude:: python/multiprocessing-3.py
                    :language: python

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
access the REST API of Orthanc. Here is a minimal example:

.. literalinclude:: python/multiprocessing-4.py
                    :language: python
