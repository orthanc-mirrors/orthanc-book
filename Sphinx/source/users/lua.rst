.. _lua:

Server-side scripting with Lua
==============================

.. contents::

Since release 0.5.2, Orthanc supports server-side scripting through
the `Lua <https://en.wikipedia.org/wiki/Lua_(programming_language)>`__
scripting language. Thanks to this major feature, Orthanc can be tuned
to specific medical workflows without being driven by an external
script. This page summarizes the possibilities of Orthanc server-side
scripting.

Many other examples are `available in the source distribution
<https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Resources/Samples/Lua/>`__.

A more expressive alternative to Lua scripts is provided by
:ref:`Python plugins <python-plugin>` and :ref:`Java plugins
<java-plugin>`.


Installing a Lua script
-----------------------

.. highlight:: bash

A custom Lua script can be installed either by the :ref:`configuration
file <configuration>`, or by uploading it
through the :ref:`REST API <rest-samples>`.

To install it by the **configuration file** method, you just have to
specify the path to the file containing the Lua script in the
``LuaScripts`` variable. A comma-separated list of paths can be
specified to install multiple scripts.

To upload a script stored in the file "``script.lua``" through the
**REST API**, use the following command::

    $ curl -X POST http://localhost:8042/tools/execute-script --data-binary @script.lua

Pay attention to the fact that, contrarily to the scripts installed
from the configuration file, the scripts installed through the REST
API are non-persistent: They are discarded after a restart of Orthanc,
which makes them useful for script prototyping. You can also interpret
a single Lua command through the REST API::

    $ curl -X POST http://localhost:8042/tools/execute-script --data-binary "print(42)"

*Note:* The ``--data-binary`` cURL option is used instead of
``--data`` to prevent the interpretation of newlines by cURL, which is
`mandatory for the proper evaluation
<https://stackoverflow.com/questions/3872427/how-to-send-line-break-with-curl>`__
of the possible comments inside the Lua script.

Lua API
-------


.. _lua-callbacks:

Callbacks to react to events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Lua engine of Orthanc invokes the following callbacks that
are triggered on various events. Here are the **generic events**:

* ``function Initialize()``: Invoked as soon as the Orthanc server is started.
* ``function Finalize()``: Invoked just before the Orthanc server is stopped.

Some **permission-related events** allow to filter incoming requests:

* ``function ReceivedInstanceFilter(dicom, origin, info)``: Invoked to
  known whether an incoming DICOM instance should be
  accepted. :ref:`See this section <lua-filter-dicom>`. The ``origin``
  parameter is :ref:`documented separately <lua-origin>`. The ``info``
  parameter contains additional information and was added in Orthanc
  1.6.1.
* ``function IncomingHttpRequestFilter(method, uri, ip, username,
  httpHeaders)``: Invoked to known whether a REST request should be
  accepted. :ref:`See this section <lua-filter-rest>`.

Some **job-related events** allow to react to :ref:`job <jobs>` completion/failure:

* ``function OnJobSubmitted(jobId)``:
  Invoked when a new job has been submitted.  Note that this does not
  mean the the job execution has started.
* ``function OnJobFailure(jobId)``:
  Invoked when a job has failed.
* ``function OnJobSuccess(jobId)``: 
  Invoked when a job has completed successfully.

Some **DICOM-related events** allow to react to the reception of
new medical images:

* ``function OnStoredInstance(instanceId, tags, metadata, origin)``:
  Invoked whenever a new instance has been stored into Orthanc. 
  This is especially useful for :ref:`lua-auto-routing`. The ``origin``
  parameter is :ref:`documented separately <lua-origin>`.
* ``function OnStablePatient(patientId, tags, metadata)``: Invoked
  whenever a patient has not received any new instance for a certain
  amount of time (cf. :ref:`stable resources <stable-resources>` 
  and the option ``StableAge`` in the
  :ref:`configuration file <configuration>`). The :ref:`identifier
  <orthanc-ids>` of the patient is provided, together with her DICOM
  tags and her :ref:`metadata <metadata>`.
* ``function OnStableSeries(seriesId, tags, metadata)``: Invoked
  whenever a series has not received any new instance for a certain
  amount of time (cf. :ref:`stable resources <stable-resources>` 
  and the option ``StableAge`` in the
  :ref:`configuration file <configuration>`).
* ``function OnStableStudy(studyId, tags, metadata)``: Invoked
  whenever a study has not received any new instance for a certain
  amount of time (cf. :ref:`stable resources <stable-resources>` 
  and the option ``StableAge`` in the
  :ref:`configuration file <configuration>`).
* ``function IncomingFindRequestFilter(source, origin)``: Invoked
  whenever Orthanc receives an incoming C-Find query through the DICOM
  protocol. This allows to inspect the content of the C-Find query,
  and possibly modify it if a patch is needed for some manufacturer. A
  `sample script is available
  <https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Resources/Samples/Lua/IncomingFindRequestFilter.lua>`__.

Some other **resource-related events** are available:

* ``function OnDeletedPatient(patientId)``: Invoked when a patient has
  been removed from the Orthanc database (new in Orthanc 1.6.0).
* ``function OnDeletedStudy(studyId)``: Invoked when a study has been
  removed from the Orthanc database (new in Orthanc 1.6.0).
* ``function OnDeletedSeries(seriesId)``: Invoked when a series has
  been removed from the Orthanc database (new in Orthanc 1.6.0).
* ``function OnDeletedInstance(instanceId)``: Invoked when a instance
  has been removed from the Orthanc database (new in Orthanc 1.6.0).
* ``function OnUpdatedPatient(patientId)``: Invoked when some metadata
  or some attachment associated with the given patient has been
  updated (new in Orthanc 1.6.0).
* ``function OnUpdatedStudy(studyId)``: Invoked when some metadata or
  some attachment associated with the given study has been updated
  (new in Orthanc 1.6.0).
* ``function OnUpdatedSeries(seriesId)``: Invoked when some metadata
  or some attachment associated with the given series has been updated
  (new in Orthanc 1.6.0).
* ``function OnUpdatedInstance(instanceId)``: Invoked when some
  metadata or some attachment associated with the given instance has
  been updated (new in Orthanc 1.6.0).

Furthermore, in versions of Orthanc <= 1.8.2, whenever a DICOM
association is negotiated for C-Store SCP, several callbacks are
successively invoked to specify which **transfer syntaxes** are
accepted for the association. These callbacks are listed in `this
sample script
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.8.2/OrthancServer/Resources/Samples/Lua/TransferSyntaxEnable.lua>`__.
These callbacks were removed in Orthanc 1.9.0.

If a callback is specified multiple times in separate scripts, the
event handler of the latest loaded script is used.

Concurrency and deadlocks
^^^^^^^^^^^^^^^^^^^^^^^^^

Orthanc only implements a single Lua context.  Therefore, all these 
callbacks are guaranteed to be **invoked in mutual exclusion**. 
This implies that Lua scripting in Orthanc does not support any 
kind of concurrency but may also lead to some deadlocks.

If a lua function (e.g. ``OnHeartBeat``) performs an HTTP call to an 
external Rest API (e.g. ``http://myserver.com/orthanc_is_alive.php``)
which, in turn, calls the Orthanc Rest API (e.g. call ``http://orthanc:8042/system``),
odds are high that you meet a deadlock because Orthanc, when handling a
Rest API calls, may try to execute some Lua callbacks (e.g. ``IncomingHttpRequestFilter``) 
while the Lua context is still blocked inside the ``OnHeartBeat`` function.

To avoid deadlocks, always make sure to avoid such back-and-forth communications
or make sure they happen asynchronously: your webservice should call the
Orthanc Rest API after it has returned from the endpoint called by
``OnHeartBeat``.

Note that these deadlocks won't happen when a lua function calls its own
Orthanc Rest API using the ``RestApiGet``, ``RestApiPost``, ... functions.


.. _lua-rest:

Calling the REST API of Orthanc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lua scripts have :ref:`full access to the REST API <rest>` of Orthanc
through the following functions:

* ``RestApiGet(uri, builtin, headers)``
* ``RestApiPost(uri, body, builtin, headers)``
* ``RestApiPut(uri, body, builtin, headers)``
* ``RestApiDelete(uri, builtin, headers)``

Here is a description of the parameters:

* ``uri`` specifies the resource being accessed
  (e.g. ``/instances``). It must not include the URL schema
  (protocol), hostname or port.

* In the context of a POST or PUT request, ``body`` is a string
  containing the body of the request
  (e.g. ``{"Keep":"StudyDate"}``). This string will often correspond
  to a JSON-formatted version of a `Lua table
  <http://lua-users.org/wiki/TablesTutorial>`__. The ``DumpJson()``
  function (see below) is very useful to achieve this conversion from
  a Lua table to a plain string.

* ``builtin`` is an optional Boolean that specifies whether the
  request targets only the built-in REST API of Orthanc (if set to
  ``true``), or the full the REST API after being tainted by plugins
  (if set to ``false``).

* ``headers`` is an optional argument and was added in release
  1.5.7. It allows to provide the REST API endpoint with HTTP headers.

.. highlight:: bash

For instance::

  RestApiPost('/instances/5af318ac-78fb-47ff-b0b0-0df18b0588e0/anonymize', '{}')


Instance modification/routing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Lua engine offers the following special functions to modify and
route DICOM instances:

* ``ModifyInstance(instanceId, replacements, removals, removePrivateTags)``
  modifies an instance.
* ``SendToModality(instanceId, modality)`` performs a synchronous C-Store to the 
  target modality.
* ``SendToPeer(instanceId, peer)`` sends the instance to a remote Orthanc peer synchronously.
* ``Delete(instanceId)`` deletes the instance.

:ref:`See this section <lua-auto-routing>` for examples. As can be
seen in those examples, these special functions can be chained
together, although they return no explicit value.

Note that these special functions should only be used for basic use
cases: Calls to the REST API :ref:`should always be favored for
auto-routing <lua-auto-routing-better>`.


General-purpose functions
^^^^^^^^^^^^^^^^^^^^^^^^^

The Lua engine of Orthanc contain several general-purpose ancillary
functions:

* ``PrintRecursive(v)`` recursively prints the content of a `Lua table
  <http://www.lua.org/pil/2.5.html>`__ to the log file of Orthanc.
* ``ParseJson(s)`` converts a string encoded in the `JSON format
  <https://en.wikipedia.org/wiki/JSON>`__ to a Lua table.
* ``DumpJson(v, keepStrings)`` encodes a Lua table as a JSON string.
  Setting the optional argument ``keepStrings`` (available from
  release 0.9.5) to ``true`` prevents the automatic conversion of
  strings to integers.
* ``GetOrthancConfiguration()`` returns a Lua table containing the
  content of the :ref:`configuration files <configuration>` of
  Orthanc.


Similarly to the functions to :ref:`call the REST API of Orthanc
<lua-rest>`, several functions are available to make generic HTTP
requests to Web services:

* ``HttpGet(url, headers)``
* ``HttpPost(url, body, headers)``
* ``HttpPut(url, body, headers)``
* ``HttpDelete(url, headers)``
* ``SetHttpCredentials(username, password)`` can be used to setup the
  HTTP credentials.
* ``SetHttpTimeout(timeout)`` can be used to configure a timeout (in seconds).
  When contacting an external webservice, it is recommended to configure a very
  short timeout not to lock the Lua context for too long.  No other Lua callbacks
  may be run at the same time which may have a significant impact on Orthanc
  responsivness in general.  This function has been introduced in version 1.11.1.
  

The ``headers`` argument is optional and was added in release
1.2.1. It allows to set the HTTP headers for the HTTP client request.

Example::

   local preview = RestApiGet('/instances/' .. instanceId .. '/preview')
   local headers = {
      ["content-type"] = "image/png",
   }

   SetHttpCredentials('user', 'pwd')
   SetHttpTimeout(1)
   HttpPost("http://localhost/my-web-service/instance-preview", preview, headers)

.. _lua-origin:

Origin of the instances
^^^^^^^^^^^^^^^^^^^^^^^

Whenever Orthanc decides whether it should should store a new instance
(cf. the ``ReceivedInstanceFilter()`` callback), or whenever it has
actually stored a new instance (cf. the ``OnStoredInstance``
callback), an ``origin`` parameter is provided. This parameter is a
`Lua table <http://www.lua.org/pil/2.5.html>`__ that describes from
which Orthanc subsystem the new instance comes from.

There are 4 possible subsystems, that can be distinguished according
to the value of ``origin["RequestOrigin"]``:

* ``RestApi``: The instance originates from some HTTP request to the REST
  API. In this case, the ``RemoteIp`` and ``Username`` fields are
  available in ``origin``. They respectively describe the IP address
  of the HTTP client, and the username that was used for HTTP
  authentication (as defined in the ``RegisteredUsers``
  :ref:`configuration variable <configuration>`).
* ``DicomProtocol``: The instance originates from a DICOM C-Store.
  The fields ``RemoteIp``, ``RemoteAet`` and ``CalledAet``
  respectively provide the IP address of the DICOM SCU (client), the
  application entity title of the DICOM SCU client, and the
  application entity title of the Orthanc SCP server. The
  ``CalledAet`` can be used for :ref:`advanced auto-routing scenarios
  <lua-auto-routing>`, when a single instance of Orthanc acts as a
  proxy for several DICOM SCU clients.
* ``Lua``: The instance originates from a Lua script.
* ``Plugins``: The instance originates from a plugin.


.. _lua-filter-dicom:

Filtering incoming DICOM instances
----------------------------------

.. highlight:: lua

Each time a DICOM instance is received by Orthanc (either through the
DICOM protocol or through the REST API), the
``ReceivedInstanceFilter()`` Lua function is invoked. If this callback
returns ``true``, the instance is accepted for storage. If it returns
``false``, the instance is discarded. This mechanism can be used to
filter the incoming DICOM instances. Here is an example of a Lua
filter that only allows incoming instances of MR modality::

 function ReceivedInstanceFilter(dicom, origin, info) 
    -- Only allow incoming MR images   
    if dicom.Modality == 'MR' then
       return true 
    else
       return false
    end
 end

The argument ``dicom`` corresponds to a `Lua table
<http://www.lua.org/pil/2.5.html>`__ (i.e. an associative array) that
contains the DICOM tags of the incoming instance. For debugging
purpose, you can print this structure as follows::

 function ReceivedInstanceFilter(dicom, origin, info) 
    PrintRecursive(dicom)
    -- Accept all incoming instances (default behavior)
    return true 
 end

The argument ``origin`` is :ref:`documented separately <lua-origin>`.

The argument ``info`` was introduced in Orthanc 1.6.1. It contains
some additional information about the received DICOM instance,
notably:

* ``HasPixelData`` is ``true`` iff. the Pixel Data (7FE0,0010) tag is
  present.
* ``TransferSyntaxUID`` contains the transfer syntax UID of the
  dataset of the instance (if applicable).


.. _lua-filter-rest:

Filtering incoming REST requests
--------------------------------

.. highlight:: lua

Lua scripting can be used to control the access to the various URI of
the REST API. Each time an incoming HTTP request is received, the
``IncomingHttpRequestFilter()`` Lua function is called. The access to
the resource is granted if and only if this callback script returns
``true``.

This mechanism can be used to implement fine-grained `access control
lists <https://en.wikipedia.org/wiki/Access_control_list>`__. Here is
an example of a Lua script that limits POST, PUT and DELETE requests
to an user that is called "admin"::

 function IncomingHttpRequestFilter(method, uri, ip, username, httpHeaders)
    -- Only allow GET requests for non-admin users
 
   if method == 'GET' then
       return true
    elseif username == 'admin' then
       return true
    else
       return false
    end
 end

Here is a description of the arguments of this Lua callback:

* ``method``: The HTTP method (GET, POST, PUT or DELETE).
* ``uri``: The path to the resource (e.g. ``/tools/generate-uid``).
* ``ip``: The IP address of the host that has issued the HTTP request (e.g. ``127.0.0.1``).
* ``username``: If HTTP Basic Authentication is enabled in the
  :ref:`configuration file <configuration>`, the name of the user that
  has issued the HTTP request (as defined in the ``RegisteredUsers``
  configuration variable). If the authentication is disabled, this
  argument is set to the empty string.
* ``httpHeaders``: The HTTP headers of the incoming request. This
  argument is available since Orthanc 1.0.1. It is useful if the
  authentication should be achieved through tokens, for instance
  against a `LDAP
  <https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol>`__
  or `OAuth2 <https://en.wikipedia.org/wiki/OAuth>`__ server.


.. _lua-auto-routing:

Auto-routing of DICOM images
----------------------------

.. highlight:: lua

Since release 0.8.0, the routing of DICOM flows can be very easily
automated with Orthanc. All you have to do is to declare your
destination modality in the :ref:`configuration file <configuration>`
(section ``DicomModalities``), then to create and install a Lua
script. For instance, here is a sample script::

    function OnStoredInstance(instanceId, tags, metadata)
      Delete(SendToModality(instanceId, 'sample'))
    end

If this script is loaded into Orthanc, whenever a new DICOM instance
is received by Orthanc, it will be routed to the modality whose
symbolic name is ``sample`` (through a Store-SCU command), then it
will be removed from Orthanc. In other words, this is a **one-liner
script to implement DICOM auto-routing**.

Very importantly, thanks to this feature, you do not have to use the
REST API or to create external scripts in order to automate simple
imaging flows. The scripting engine is entirely contained inside the
Orthanc core system.

Thanks to Lua expressiveness, you can also implement conditional
auto-routing. For instance, if you wish to route only patients whose
name contains "David", you would simply write::

 function OnStoredInstance(instanceId, tags, metadata)
    -- Extract the value of the "PatientName" DICOM tag
    local patientName = string.lower(tags['PatientName'])
 
   if string.find(patientName, 'david') ~= nil then
       -- Only route patients whose name contains "David"
       Delete(SendToModality(instanceId, 'sample'))
 
   else
       -- Delete the patients that are not called "David"
       Delete(instanceId)
    end
 end

Besides ``SendToModality()``, a mostly identical function with the
same arguments called ``SendToPeer()`` can be used to route instances
to :ref:`Orthanc peers <peers>`.  It is also possible to modify the
received instances before routing them. For instance, here is how you
would replace the ``StationName`` DICOM tag::

 function OnStoredInstance(instanceId, tags, metadata)
    -- Ignore the instances that result from a modification to avoid
    -- infinite loops
    if (metadata['ModifiedFrom'] == nil and
        metadata['AnonymizedFrom'] == nil) then
 
      -- The tags to be replaced
       local replace = {}
       replace['StationName'] = 'My Medical Device'
 
      -- The tags to be removed
       local remove = { 'MilitaryRank' }

      -- Modify the instance, send it, then delete the modified instance
       Delete(SendToModality(ModifyInstance(instanceId, replace, remove, true), 'sample'))

      -- Delete the original instance
       Delete(instanceId)
    end
 end


.. _lua-auto-routing-better:

Important remarks about auto-routing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``SendToModality()``, ``SendToPeer()``, ``ModifyInstance()`` and
``Delete()`` functions are for the most basic cases of auto-routing
(implying a single DICOM instance, and possibly a basic modification
of this instance). The ``ModifyInstance()`` function `could also lead
to problems
<https://groups.google.com/d/msg/orthanc-users/hmv2y-LgKm8/oMAuGJWMBgAJ>`__
if it deals with tags wrongly interpreted as numbers by Lua.

For more evolved auto-routing scenarios, remember that Lua scripts
:ref:`have full access to the REST API of Orthanc <lua-rest>`. This is
illustrated by the ``AutoroutingModification.lua`` sample available in
the source distribution of Orthanc::

 function OnStoredInstance(instanceId, tags, metadata, origin)
    -- Ignore the instances that result from the present Lua script to
    -- avoid infinite loops
    if origin['RequestOrigin'] ~= 'Lua' then
    
       -- The tags to be replaced
       local replace = {}
       replace['StationName'] = 'My Medical Device'
       replace['0031-1020'] = 'Some private tag'
       
       -- The tags to be removed
       local remove = { 'MilitaryRank' }
       
       -- Modify the instance
       local command = {}
       command['Replace'] = replace
       command['Remove'] = remove
       local modifiedFile = RestApiPost('/instances/' .. instanceId .. '/modify', DumpJson(command, true))
       
       -- Upload the modified instance to the Orthanc database so that
       -- it can be sent by Orthanc to other modalities
       local modifiedId = ParseJson(RestApiPost('/instances/', modifiedFile)) ['ID']
       
       -- Send the modified instance to another modality
       RestApiPost('/modalities/sample/store', modifiedId)
              
       -- Delete the original and the modified instances
       RestApiDelete('/instances/' .. instanceId)
       RestApiDelete('/instances/' .. modifiedId)
    end
 end

Also note that :ref:`other callbacks are available <lua-callbacks>`
(``OnStablePatient()``, ``OnStableStudy()`` and ``OnStableSeries()``)
to react to other events than the reception of a single instance 
with ``OnStoredInstance()``.

.. _lua-fix-cfind:

Fixing C-Find requests
----------------------

:ref:`C-Find requests <dicom-find>` are sometimes interpreted
differently by different DICOM servers (e.g. the ``*`` wildcard, as
`reported by users
<https://groups.google.com/d/msg/orthanc-users/3g7V7kqr3g0/IREL88RWAwAJ>`__),
and sometimes a querying modality might set unexpected DICOM tags
(cf. `this real-world example
<https://groups.google.com/d/msg/orthanc-users/PLWKqVVaXLs/n_0x4vKhAgAJ>`__). In
such situations, it is possible to dynamically fix incoming or
outgoing C-Find queries using a Lua script.

Sanitizing incoming C-Find requests can be done by implementing the
``IncomingFindRequestFilter(query, origin)`` callback that is called
whenever the Orthanc C-Find SCP is queried by a remote modality. For
instance, here is Lua script to remove a private tag that is specified
by some manufacturer::

  function IncomingFindRequestFilter(query, origin)
    -- First display the content of the C-Find query
    PrintRecursive(query)
    PrintRecursive(origin)

    -- Remove the "PrivateCreator" tag from the query
    local v = query
    v['5555,0010'] = nil

    return v
  end

The ``origin`` argument contains information about which modality has
issued the request.

Note that this callback allows you to modify the incoming request
but will not modify the list of tags that Orthanc will return.

Also note that the ``IncomingFindRequestFilter`` callback is not applied to
C-Find requests targeting :ref:`modality worklists
<worklists-plugin>`. Since Orthanc 1.4.2, the corresponding
``IncomingWorklistRequestFilter`` callback can be used to sanitize
C-FIND requests against worklists::

  function IncomingWorklistRequestFilter(query, origin)
    PrintRecursive(query)
    PrintRecursive(origin)

    -- Implements the same behavior as the "FilterIssuerAet"
    -- option of the sample worklist plugin
    query['0040,0100'][1]['0040,0001'] = origin['RemoteAet']

    return query
  end


Similarly, the callback ``OutgoingFindRequestFilter(query, modality)``
is invoked whenever Orthanc acts as a C-Find SCU, which gives the
opportunity to dynamically fix outgoing C-Find requests before they
are actually sent to the queried modality. For instance, here is a
sample Lua callback that would replace asterisk wildcards (i.e. ``*``)
by an empty string for any query/retrieve issued by Orthanc (including
from Orthanc Explorer)::

  function OutgoingFindRequestFilter(query, modality)
    for key, value in pairs(query) do
      if value == '*' then
        query[key] = ''
      end
    end

    return query
  end


HeartBeat
---------

.. highlight:: lua

Starting from Orthanc 1.11.1, one can run a Lua callback at regular 
interval.  This interval is defined in the ``LuaHeartBeatPeriod``
configuration::

  function OnHeartBeat() 
    
    -- ping a webservice to notify that Orthanc is still alive
    SetHttpCredentials('user', 'pwd')
    SetHttpTimeout(1)
    HttpPost("http://localhost/my-web-service/still-alive", "my-id", {})

  end


Stabilizing resources
---------------------

.. highlight:: lua

Starting from Orthanc 1.12.9, one can call the ``SetStableStatus(resourceId, newStateIsStable)`` Lua function to
force a resource to get ``Stable`` faster and trigger the 
changes and callbacks::

  function OnStoredInstance(instanceId, tags, metadata)

      PrintRecursive(tags)

      -- let's stability CR series immediately
      if tags['Modality'] == 'CR' then
          local seriesId = ParseJson(RestApiGet('/instances/' .. instanceId)) ['ParentSeries']

          print("LUA: setting a series as stable earlier since this is a CR series")
          SetStableStatus(seriesId, true)  -- true to set the study as Stable, false to set the study as Unstable
      end

  end

.. _lua-external-modules:

Using external modules
----------------------

Starting with Orthanc 1.3.2, it is possible to use external Lua
modules if Orthanc was compiled with the ``-DENABLE_LUA_MODULES=ON``
while invoking CMake.

Importantly, the modules and the Orthanc server must use the same
version of Lua for external modules to be properly loaded.

Check out the Orthanc Users forum for old discussions about this
topic: `reference 1
<https://groups.google.com/g/orthanc-users/c/BXfmwU786B0/m/M47slt5GFwAJ>`__,
`reference 2
<https://groups.google.com/g/orthanc-users/c/BXfmwU786B0/m/qpVe8UvGAwAJ>`__,
`reference 3
<https://groups.google.com/g/orthanc-users/c/LDAN5jA0X8M/m/4zrk0_AaBAAJ>`__.
