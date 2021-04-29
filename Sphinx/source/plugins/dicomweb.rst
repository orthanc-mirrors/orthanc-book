.. _dicomweb:


DICOMweb plugin
===============

.. contents::

This **official** plugin extends Orthanc with support of the `DICOMweb
protocols <https://en.wikipedia.org/wiki/DICOMweb>`__. More precisely,
the plugin introduces a basic, reference implementation of WADO-URI,
WADO-RS, QIDO-RS and STOW-RS, following `DICOM PS3.18
<http://dicom.nema.org/medical/dicom/current/output/html/part18.html>`__.
The plugin simultaneously turns Orthanc into a **DICOMweb server** and 
into a **DICOMweb client**.

For general information, check out the `official homepage of the
plugins <https://www.orthanc-server.com/static.php?page=dicomweb>`__.

The full standard is not implemented yet, the supported features are
`tracked in the repository
<https://hg.orthanc-server.com/orthanc-dicomweb/file/default/Status.txt>`__.


Compilation
-----------

.. highlight:: text

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancDicomWeb`` that
contains the DICOMweb plugin. Pre-compiled binaries for Microsoft
Windows `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-dicom-web>`__,
and are included in the `Windows installers
<https://www.orthanc-server.com/download-windows.php>`__.  A package
for `Apple's Mac OS X
<https://www.orthanc-server.com/static.php?page=download-mac>`__ is
available courtesy of `Osimis <https://www.osimis.io/>`__.

*Remark:* Some older build instructions are also available in the
`source distribution
<https://hg.orthanc-server.com/orthanc-dicomweb/file/default/Resources/BuildInstructions.txt>`__.


Installation
------------

.. highlight:: json

You of course first have to :ref:`install Orthanc <binaries>`. Once
Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. For GNU/Linux, you
could for instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancDicomWeb/Build/libOrthancDicomWeb.so"
    ]
  }

Or, for Windows::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "c:/Temp/OrthancDicomWeb.dll"
    ]
  }

Note that the DICOMweb server will share all the parameters of the
Orthanc HTTP server, notably wrt. authentication and HTTPS
encryption. For this reason, you will most probably have to enable the
remote access to the Orthanc HTTP server::

  {
    [...]
    "RemoteAccessEnabled" : true,
    [...]
  }

Once Orthanc has restarted, the root of the DICOMweb REST API is
accessible at ``http://localhost:8042/dicom-web/``.


Options
-------


.. _dicomweb-server-config:

Server-related options
^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: json

There are several configuration options that can be set to fine-tune
the Orthanc DICOMweb server. Here is the full list of the available
options, all of them must be grouped inside the ``DicomWeb`` section of
the Orthanc configuration file::

  {
    [...]
    "DicomWeb" : {
      "Enable" : true,            // Whether DICOMweb support is enabled
      "Root" : "/dicom-web/",     // Root URI of the DICOMweb API (for QIDO-RS, STOW-RS and WADO-RS)
      "EnableWado" : true,        // Whether WADO-URI (previously known as WADO) support is enabled
      "WadoRoot" : "/wado",       // Root URI of the WADO-URI (aka. WADO) API
      "Ssl" : false,              // Whether HTTPS should be used for subsequent WADO-RS requests
      "QidoCaseSensitive" : true, // For QIDO-RS server, whether search is case sensitive (since release 0.5)
      "Host" : "localhost",       // Hard-codes the name of the host for subsequent WADO-RS requests (deprecated)
      "StudiesMetadata" : "Full", // How study-level metadata is retrieved (since release 1.1, cf. section below)
      "SeriesMetadata" : "Full"   // How series-level metadata is retrieved (since release 1.1, cf. section below)
    }
  }

Furthermore, the global option ``DefaultEncoding`` specifies the
encoding (specific character set) that will be used when answering a
QIDO-RS request. It might be a good idea to set this option to
``Utf8`` if you are dealing with an international environment.

**Remark 1:** The following configuration options were present in
releases <= 0.6 of the plugin, but are not used anymore::

  {
    [...]
    "DicomWeb" : {
      "StowMaxInstances" : 10,    // For STOW-RS client, the maximum number of instances in one single HTTP query (0 = no limit)
      "StowMaxSize" : 10,         // For STOW-RS client, the maximum size of the body in one single HTTP query (in MB, 0 = no limit)
    }
  }

These older configuration options were used to limit the size of the
HTTP requests, by issuing multiple calls to STOW-RS (set both options
to 0 to send one single request).


**Remark 2:** The option ``Host`` is deprecated. Starting with release
0.7 of the DICOMweb plugin, its value are computed from the standard
HTTP headers ``Forwarded`` and ``Host``, as provided by the HTTP
clients.


.. _dicomweb-server-metadata-config:

Fine-tuning server for WADO-RS Retrieve Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The options ``StudiesMetadata`` and ``SeriesMetadata`` were introduced
in release 1.1 of the DICOMweb plugin. These options specify how the
calls to ``/dicom-web/studies/.../metadata`` and
``/dicom-web/studies/.../series/.../metadata`` (i.e. `WADO-RS Retrieve
Metadata
<http://dicom.nema.org/medical/dicom/2019a/output/chtml/part18/sect_6.5.6.html>`__)
are processed:

* If ``Full`` mode is used, the plugin will read all the DICOM
  instances of the study/series of interest from the :ref:`storage
  area <orthanc-storage>`, which gives fully accurate results but
  requires all the individual instances to be read and parsed from the
  filesystem, leading to slow performance (cf. `issue 162
  <https://bugs.orthanc-server.com/show_bug.cgi?id=162>`__). This is
  the default mode.

* If ``MainDicomTags`` mode is used, the plugin will only report the
  main DICOM tags that are indexed by the Orthanc database. The DICOM
  files are not read from the disk, which provides best
  performance. However, this is a small subset of all the tags that
  would be retrieved if using the ``Full`` mode: A DICOMweb viewer
  might need more tags.

* If ``Extrapolate`` mode is used, the plugin will read up to 3 DICOM
  instances at random that belong to the study/series of interest. It
  will then test whether the majority of these instances share the
  same value for a predefined subset of DICOM tags. If so, this value
  is added to the metadata response; otherwise, the tag is not
  reported. In other words, this mode extrapolates the value of some
  predefined tags by assuming that these tags should be constant
  across all the instances of the study/series. This mode is a
  compromise between ``MainDicomTags`` (focus on speed) and ``Full``
  (focus on accuracy).

* If you are using a DICOMweb viewer (such as forthcoming Stone Web
  viewer or `OHIF viewer
  <https://groups.google.com/d/msg/orthanc-users/y1N5zOFVk0M/a3YMdhNqBwAJ>`__)
  in a setup where performance and accuracy are both important, you
  should most probably set ``StudiesMetadata`` to ``MainDicomTags``
  and ``SeriesMetadata`` to ``Full``. Forthcoming Stone Web viewer
  will probably specify a value for the
  ``SeriesMetadataExtrapolatedTags`` option to be used for setups
  where performance is extremely important.


If using the ``Extrapolate`` mode, the predefined tags are provided
using the ``StudiesMetadataExtrapolatedTags`` and
``SeriesMetadataExtrapolatedTags`` configuration options as follows::
  
  {
    [...]
    "DicomWeb" : {
      [...]
      "StudiesMetadata" : "Extrapolate",
      "StudiesMetadataExtrapolatedTags" : [
        "AcquisitionDate"
      ],
      "SeriesMetadata" : "Extrapolate",
      "SeriesMetadataExtrapolatedTags" : [
        "BitsAllocated",
        "BitsStored",
        "Columns",
        "HighBit",
        "PhotometricInterpretation",
        "PixelSpacing",
        "PlanarConfiguration",
        "RescaleIntercept",
        "RescaleSlope",
        "Rows",
        "SOPClassUID",
        "SamplesPerPixel",
        "SliceThickness"
      ]
    }
  }


.. _dicomweb-client-config:

Client-related options
^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: json

If you want to connect Orthanc as a client to remote DICOMweb servers
(cf. below), you need to modify the configuration file so as to define
each of them in the option ``DicomWeb.Servers``. The syntax is
identical to the ``OrthancPeers`` option of the :ref:`configuration of
the Orthanc core <configuration>`.

In the most simple case, here is how to instruct Orthanc about the
existence of a password-less DICOMweb server that will be referred to
as "sample" in Orthanc::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : [ "http://192.168.1.1/dicom-web/" ]
      }
    }
  }

You are of course free to add as many DICOMweb servers as you need. If
the DICOMweb server is protected by a password (with `HTTP Basic
access authentication
<https://en.wikipedia.org/wiki/Basic_access_authentication>`__)::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : [ "http://192.168.1.1/dicom-web/", "username", "password" ]
      }
    }
  }

Three important options can be provided for individual remote DICOMweb servers:

* ``HasDelete`` can be set to ``true`` to indicate that the HTTP
  DELETE method can be used to delete remote studies/series/instances.
  This notably adds a "delete" button on the Web interface of the
  DICOMweb client, and creates a route
  ``/dicom-web/servers/sample/delete`` in the REST API.

* ``ChunkedTransfers`` must be set to ``false`` if the remote DICOMweb
  server does not support `HTTP chunked transfer encoding
  <https://en.wikipedia.org/wiki/Chunked_transfer_encoding>`__. Setting
  this option to ``true`` is the best choice to reduce memory
  consumption. However, it must be set to ``false`` if the remote
  DICOMweb server is Orthanc <= 1.5.6, as chunked transfer encoding is
  only supported starting with Orthanc 1.5.7. Beware setting
  ``ChunkedTransfers`` to ``true`` in Orthanc 1.5.7 and 1.5.8 utilizes
  one CPU at 100%, which results in very low throughput: This issue is
  resolved in Orthanc 1.6.0 (cf. `issue 156
  <https://bugs.orthanc-server.com/show_bug.cgi?id=156>`__ for full
  explanation).

* ``HasWadoRsUniversalTransferSyntax`` (new in DICOMweb 1.1) must be
  set to ``false`` if the remote DICOMweb server does not support the
  value ``transfer-syntax=*`` in the ``Accept`` HTTP header for
  WADO-RS requests. This option is notably needed if the remote
  DICOMweb server is Orthanc equipped with DICOMweb plugin <= 1.0. On
  the other hand, setting this option to ``true`` prevents the remote
  DICOMweb server from transcoding to uncompressed transfer syntaxes,
  which gives `much better performance
  <https://groups.google.com/d/msg/orthanc-users/w1Ekrsc6-U8/T2a_DoQ5CwAJ>`__.
  The implicit value of this parameter was ``false`` in DICOMweb
  plugin <= 1.0, and its default value is ``true`` since DICOMweb
  plugin 1.1.
  
You'll have to convert the JSON array into a JSON object to set these
options::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : {
          "Url" : "http://192.168.1.1/dicom-web/", 
          "Username" : "username", 
          "Password" : "password",
          "HasDelete" : true,
          "ChunkedTransfers" : true,                 // Set to "false" if "sample" is Orthanc <= 1.5.6
          "HasWadoRsUniversalTransferSyntax" : true  // Set to "false" if "sample" is Orthanc DICOMweb plugin <= 1.0
        }
      }
    }
  }


Furthermore, if the DICOMweb server is protected with HTTPS client
authentication, you must provide your client certificate (in the `PEM
format
<https://en.wikipedia.org/wiki/Privacy-enhanced_Electronic_Mail>`__),
your client private key (also in the PEM format), together with the
password protecting the private key::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : {
          "Url" : "http://192.168.1.1/dicom-web/", 
          "CertificateFile" : "client.crt",
          "CertificateKeyFile" : "client.key",
          "CertificateKeyPassword" : "password"
        }
      }
    }
  }


The definition of a DICOMweb server can also specify the HTTP headers
to be provided during each request to the remote DICOMweb server. This
can for instance be useful to set authorization tokens::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : {
          "Url" : "http://localhost:8042/dicom-web/",
          "HttpHeaders": {
            "Authorization" : "Bearer HelloWorldToken"
          }
        }
      }
    }
  }


Finally, it is possible to use client authentication with hardware
security modules and smart cards through `PKCS#11
<https://en.wikipedia.org/wiki/PKCS_11>`__ (this feature is only
available is the core of Orthanc was compiled with the
``-DENABLE_PKCS11=ON`` option in CMake, and if the Orthanc
configuration file has a proper ``Pkcs11`` section)::

  {
    [...]
    "DicomWeb" : {
      "Servers" : {
        "sample" : {
          "Url" : "http://192.168.1.1/dicom-web/", 
          "Pkcs11" : true
        }
      }
    }
  }

Starting with release 1.5 of the DICOMweb plugin, the configuration
option ``ServersInDatabase`` can be set to ``true`` in order for the
plugin to **read/write the definitions of the DICOMweb servers
from/into the database of Orthanc**. This makes the modifications to
the DICOMweb servers persistent across successive executions of
Orthanc. If this option is enabled, the REST API must be used on URI
``/dicom-web/servers/`` (with the GET, DELETE or PUT methods) to
:ref:`add/update/remove DICOMweb servers
<dicomweb-additional-samples>`. Here is the syntax to enable this
feature::
  
  {
    [...]
    "DicomWeb" : {
      "ServersInDatabase" : true   // "false" by default
    }
  }
  
In forthcoming release 1.6 of the DICOMweb plugin, the ``Timeout``
field can be added to the definition of a DICOMweb server (in
``DicomWeb.Servers``) in order to specify a separate HTTP timeout when
contacting this DICOMweb server. By default, the global value
``HttpTimeout`` is used.

**Remark:** A :ref:`plugin by Osimis <google>` is available to
dynamically create authenticated connections to Google Cloud Platform.

**Important remark:** When querying a DICOMweb server, Orthanc will
automatically use the global configuration options ``HttpProxy``,
``HttpTimeout``, ``HttpsVerifyPeers``, ``HttpsCACertificates``, and
``Pkcs11``. Make sure to adapt them if need be.


Quickstart - DICOMweb client
----------------------------

Starting with version 1.0 of the DICOMweb plugin, a Web interface is
provided to use Orthanc as a DICOMweb client. Simply click on the
"Open DICOMweb client" button at the bottom of the welcome screen of
:ref:`Orthanc Explorer <orthanc-explorer>`.

Here is a direct link to the DICOMweb client running on our demo
server:
`https://demo.orthanc-server.com/dicom-web/app/client/index.html
<https://demo.orthanc-server.com/dicom-web/app/client/index.html>`__



Quickstart - DICOMweb server
----------------------------

Once your Orthanc server is properly configured (see above), you can
make REST calls to the API of the DICOMweb server. For demonstration
purpose, this section makes the assumption that the ``VIX`` dataset
provided by `OsiriX
<https://www.osirix-viewer.com/resources/dicom-image-library/>`__ has
been uploaded to Orthanc.

WADO-URI
^^^^^^^^

.. highlight:: text

Here is a proper WADO-URI (previously known simply as WADO) request to
render one slice of the VIX dataset as a JPEG image::

  http://localhost:8042/wado?objectUID=1.3.12.2.1107.5.1.4.54693.30000006100507010800000005466&requestType=WADO


.. highlight:: bash

The ``objectUID`` corresponds to the ``SOPInstanceUID`` DICOM tag of
some instance in the ``VIX`` dataset. Given the Orthanc identifier of
an instance from VIX
(e.g. ``14b4db2c-065edecb-6a767936-7068293a-92fcb080``), the latter
tag can be obtained from the ``MainDicomTags`` field::

  $ curl http://localhost:8042/instances/14b4db2c-065edecb-6a767936-7068293a-92fcb080


QIDO-RS
^^^^^^^

.. highlight:: bash

Regarding QIDO-RS (querying the content of a remote DICOMweb server),
here is how to obtain the list of studies stored by Orthanc::

  $ curl http://localhost:8042/dicom-web/studies

Note that the ``/dicom-web/`` prefix comes from the configuration
option ``Root`` of the ``DicomWeb`` section. Filtering the studies is
possible as follows::

  $ curl http://localhost:8042/dicom-web/studies?PatientName=VIX



WADO-RS
^^^^^^^

A study can be retrieved through WADO-RS. Here is a sample using the VIX dataset::

  $ curl http://localhost:8042/dicom-web/studies/2.16.840.1.113669.632.20.1211.10000315526/

This answer is a `multipart stream
<https://en.wikipedia.org/wiki/MIME#Multipart_messages>`__ of
``application/dicom`` DICOM instances, so a Web browser will not be
able to display it (. You will have to use either AJAX (JavaScript) or a
command-line tool (such as cURL).

You can render one individual frame as a plain PNG image as follows::

  $ curl http://localhost:8042/dicom-web/studies/2.16.840.1.113669.632.20.1211.10000315526/series/1.3.12.2.1107.5.1.4.54693.30000006100507010800000005268/instances/1.3.12.2.1107.5.1.4.54693.30000006100507010800000005466/frames/1/rendered -H 'accept: image/png'


Other endpoints
^^^^^^^^^^^^^^^

This page only provides some very basic examples about the use of a
DICOMweb server. Please check out `the full reference of the DICOMweb
API <https://www.dicomstandard.org/dicomweb/>`__ for more information.



.. _dicomweb-client:

REST API of the Orthanc DICOMweb client
---------------------------------------

Listing the available servers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

The list of the remote DICOMweb servers that are known to the DICOMweb
plugin can be obtained as follows::

  $ curl http://localhost:8042/dicom-web/servers/
  [ "sample" ]

In this case, a single server called ``sample`` is configured.


Making a call to QIDO-RS or WADO-RS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

In Orthanc, the URI ``/{dicom-web-root}/servers/{name}/get`` allows to
make a HTTP GET call against a DICOMweb server. This can be used to
issue a QIDO-RS or WADO-RS command. Orthanc will take care of properly
encoding the URL and authenticating the client. For instance, here is
a sample QIDO-RS search to query all the studies (using a bash
command-line)::

  $ curl http://localhost:8042/dicom-web/servers/sample/get -d @- << EOF
  {
    "Uri" : "/studies"
  }
  EOF

The result of this call is a JSON document formatted according to the
DICOMweb standard. You do not have to specify the base URL of the
remote DICOMweb server, as it is encoded in the configuration file.

As a more advanced example, here is how to search all the series
associated with a given patient name, while requesting to use an XML
format::

  $ curl http://localhost:8042/dicom-web/servers/sample/get -d @- << EOF
  {
    "Uri" : "/series",
    "HttpHeaders" : {
      "Accept" : "application/dicom+xml"
    },
    "Arguments" : {
      "00100010" : "KNIX"
    }
  }
  EOF

The result of the command above is a `multipart stream
<https://en.wikipedia.org/wiki/MIME#Multipart_messages>`__ of XML
documents describing each series.

Note how all the GET arguments to the QIDO-RS request must be
specified in the ``Arguments`` field. Orthanc will take care of
`properly encoding it as an URL
<https://en.wikipedia.org/wiki/Percent-encoding>`__.

An user-friendly reference of the features available in QIDO-RS and
WADO-RS `can be found on this site
<https://www.dicomstandard.org/dicomweb/>`__.


Sending DICOM resources to a STOW-RS server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

STOW-RS allows to send local DICOM resources to a remote DICOMweb
server. In Orthanc, the STOW-RS client primitive is available at URI
``/{dicom-web-root}/servers/{name}/stow``. Here is a sample call::

  $ curl http://localhost:8042/dicom-web/servers/sample/stow -X POST -d @- << EOF
  {
    "Resources" : [
      "6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228"
    ]
  }
  EOF

Note that this primitive takes as its input a list of :ref:`Orthanc
identifiers <orthanc-ids>` corresponding to the resources (patients,
studies, series and/or instances) to be exported.

Additional HTTP headers can be added with an optional ``HttpHeaders``
argument as for QIDO-RS and WADO-RS. This might be useful e.g. for
cookie-based session management.

Internally, this call results in creating an :ref:`Orthanc job <jobs>`
that is executed synchronously (the REST call only returns once the 
STOW-RS request is finished). You can run the job in asynchronous 
mode as follows::

  $ curl http://localhost:8042/dicom-web/servers/sample/stow -X POST -d @- << EOF
  {
    "Resources" : [
      "6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228"
    ],
    "Synchronous" : false,
    "Priority" : 10
  }
  EOF

  {
    "ID" : "a7bd2a5c-291d-4ca5-977a-66502cab22a1",
    "Path" : ".././../jobs/a7bd2a5c-291d-4ca5-977a-66502cab22a1"
  }

Such a call ends immediately, and returns the ID of the job created by
Orthanc. The :ref:`status of the job <jobs-monitoring>` can then be
monitored using the Orthanc REST API.



Retrieving DICOM resources from a WADO-RS server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Once DICOM resources of interest have been identified through a
QIDO-RS call to a remote DICOMweb server (cf. above), it is
interesting to download them locally with a WADO-RS call. You could do
it manually with a second call to the
``/{dicom-web-root}/servers/{name}/get`` URI, but Orthanc provides
another primitive ``.../retrieve`` to automate this process, in order
to avoid the manual parsing of the multipart stream.

Here is how you would download one study, one series and one instance
whose StudyInstanceUID (0020,000d), SeriesInstanceUID (0020,000e) are
SOPInstanceUID (0008,0018) have been identified through a former
QIDO-RS call::

  $ curl http://localhost:8042/dicom-web/servers/sample/retrieve -X POST -d @- << EOF
  {
    "Resources" : [
      {
        "Study" : "1.3.51.0.1.1.192.168.29.133.1688840.1688819"
      },
      {
        "Study" : "1.3.51.0.1.1.192.168.29.133.1681753.1681732",
        "Series" : "1.3.12.2.1107.5.2.33.37097.2012041613040617636372171.0.0.0"
      },
      {
        "Study" : "1.3.51.0.1.1.192.168.29.133.1681753.1681732",
        "Series" : "1.3.12.2.1107.5.2.33.37097.2012041612474981424569674.0.0.0",
        "Instance" : "1.3.12.2.1107.5.2.33.37097.2012041612485540185869716"
      }
    ]
  }
  EOF

Orthanc will reply with the list of the Orthanc identifiers of all the
DICOM instances that were downloaded from the remote server.

Remark 1: Contrarily to the ``.../stow`` URI that uses :ref:`Orthanc
identifiers <orthanc-ids>`, the ``.../retrieve`` URI uses DICOM
identifiers.

Remark 2: The ``HttpHeaders`` and ``Arguments`` arguments are also
available, as for QIDO-RS, to fine-tune the parameters of the WADO-RS
request.

Remark 3: As for QIDO-RS, the request is run synchronously by default.
The ``Synchronous`` and ``Priority`` arguments can be used to
asynchronously run the request.


.. _dicomweb-additional-samples:

Additional samples
------------------

Samples of how to call DICOMweb services from standalone applications
are available for `Python
<https://hg.orthanc-server.com/orthanc-dicomweb/file/default/Resources/Samples/Python>`__
and for `JavaScript
<https://hg.orthanc-server.com/orthanc-dicomweb/file/default/Resources/Samples/JavaScript>`__.

Integration tests are `available separately
<https://hg.orthanc-server.com/orthanc-tests/file/default/Plugins/DicomWeb/Run.py>`__,
and provide samples for more advanced features of the REST API (such
as dynamically adding/updating/removing remote DICOMweb servers using
HTTP PUT and DELETE methods).
