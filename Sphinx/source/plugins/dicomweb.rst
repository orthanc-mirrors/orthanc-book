.. _dicomweb:


DICOMweb plugin
===============

.. contents::

This **official** plugin extends Orthanc with support of the `DICOMweb
protocols <https://en.wikipedia.org/wiki/DICOMweb>`__. More precisely,
the plugin introduces a basic, reference implementation of WADO-URI,
WADO-RS, QIDO-RS and STOW-RS, following `DICOM PS3.18
<http://dicom.nema.org/medical/dicom/current/output/html/part18.html>`__.

For general information, check out the `official homepage of the
plugins <http://www.orthanc-server.com/static.php?page=dicomweb>`__.

The full standard is not implemented yet, the supported features are
`tracked in the repository
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Status.txt>`__.


Compilation
-----------

.. highlight:: text

The procedure to compile these plugins is similar of that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancDicomWeb`` that
contains the DICOMweb plugin. Pre-compiled binaries for Microsoft
Windows `are also available
<http://www.orthanc-server.com/browse.php?path=/plugin-dicom-web>`__.
A package for `Apple's Mac OS X
<http://localhost/~jodogne/orthanc/static.php?page=download-mac>`__ is
available courtesy of `Osimis <http://osimis.io/>`__.

*Remark:* Some older build instructions are also available in the
`source distribution
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Resources/BuildInstructions.txt>`__.


Usage
-----

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
      "Host" : "localhost",       // Hard-codes the name of the host for subsequent WADO-RS requests
      "Ssl" : false,              // Whether HTTPS should be used for subsequent WADO-RS requests
      "StowMaxInstances" : 10,    // For STOW-RS client, the maximum number of instances in one single HTTP query (0 = no limit)
      "StowMaxSize" : 10,         // For STOW-RS client, the maximum size of the body in one single HTTP query (in MB, 0 = no limit)
      "QidoCaseSensitive" : true  // For QIDO-RS server, whether search is case sensitive (since release 0.5)
    }
  }


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

If the DICOMweb server is protected with HTTPS client authentication,
you must provide your client certificate (in the `PEM format
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

Finally, it is also possible to use client authentication with
hardware security modules and smart cards through `PKCS#11
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

**Important remark:** When querying a DICOMweb server, Orthanc will
automatically use the global configuration options ``HttpProxy``,
``HttpTimeout``, ``HttpsVerifyPeers``, ``HttpsCACertificates``, and
``Pkcs11``. Make sure to adapt them if need be.


Quickstart
----------

Once your Orthanc is properly configured (see above), you can make
REST calls to the DICOMweb API. For demonstration purpose, this
section makes the assumption that the ``VIX`` dataset provided by
`OsiriX <http://www.osirix-viewer.com/datasets/>`__ has been uploaded
to Orthanc.

WADO-URI
^^^^^^^^

.. highlight:: text

Here is a proper WADO-URI (previously known simply as WADO) request to
render one slice of the VIX dataset as a JPEG image::

  http://localhost:8042/wado?objectUID=1.3.12.2.1107.5.1.4.54693.30000006100507010800000005466&requestType=WADO

The ``objectUID`` corresponds to the ``SOPInstanceUID`` DICOM tag of
some instance in the ``VIX`` dataset. Given the Orthanc identifier of
an instance from VIX
(e.g. ``14b4db2c-065edecb-6a767936-7068293a-92fcb080``), the latter
tag can be obtained from the ``MainDicomTags`` field::

  # curl http://localhost:8042/instances/14b4db2c-065edecb-6a767936-7068293a-92fcb080


WADO-RS
^^^^^^^

.. highlight:: text

Regarding WADO-RS (i.e. DICOMweb RESTful services), here is how to
obtain the tags of all the instances stored by Orthanc::

  # curl http://localhost:8042/dicom-web/instances

Note that, as the MIME type of this answer is a multipart
``application/dicom+xml``, a Web browser will not be able to display
it. You will have to use either AJAX (JavaScript) or a command-line
tool (such as curl).

Here is how to generate a JPEG preview of one instance with WADO-RS
(through the RetrieveFrames primitive)::

  # curl http://localhost:8042/dicom-web/studies/2.16.840.1.113669.632.20.1211.10000315526/series/1.3.12.2.1107.5.1.4.54693.30000006100507010800000005268/instances/1.3.12.2.1107.5.1.4.54693.30000006100507010800000005466/frames/1 -H 'accept: multipart/related; type=image/dicom+jpeg'



Querying a remote DICOMweb server with Orthanc
----------------------------------------------

Listing the available servers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

The list of the remote DICOMweb servers that are known to the DICOMweb
plugin can be obtained as follows::

  # curl http://localhost:8042/dicom-web/servers/
  [ "sample" ]

Here, a single server called ``sample`` is configured.


Making a call to QIDO-RS or WADO-RS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

In Orthanc, the URI ``/{dicom-web-root}/servers/{name}/get`` allows to
make a HTTP GET call against a DICOMweb server. This can be used to
issue a QIDO-RS or WADO-RS command. Orthanc will take care of properly
encoding the URL and authenticating the client.

For instance, here is a sample QIDO-RS search to query all the studies
(using a bash command-line)::

  # curl http://localhost:8042/dicom-web/servers/sample/get -d @- << EOF
  {
    "Uri" : "/studies"
  }
  EOF

You do not have to specify the base URL of the remote DICOMweb server,
as it is encoded in the configuration file.

The result of the command above is a multipart
``application/dicom+xml`` document.  It is possible to request a more
human-friendly JSON answer by adding the ``Accept`` HTTP header. Here
is how to search for a given patient name, while requesting a JSON
answer and pretty-printing through the ``json_pp`` command-line tool::

  # curl http://localhost:8042/dicom-web/servers/sample/get -d @- << EOF | json_pp 
  {
    "Uri" : "/studies",
    "HttpHeaders" : {
      "Accept" : "application/json"
    },
    "Arguments" : {
      "00100010" : "*JODOGNE*"
    }
  }
  EOF

Note how all the GET arguments for the QIDO-RS request must be
specified in the ``Arguments`` field. Orthanc will take care of
properly encoding it to a URL.

An user-friendly reference of the features available in QIDO-RS and
WADO-RS `can be found on this site <http://www.dicomweb.org/>`__.


Sending DICOM resources to a STOW-RS server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

STOW-RS allows to send local DICOM resources to a remote DICOMweb
server. In Orthanc, the STOW-RS client primitive is available at URI
``/{dicom-web-root}/servers/{name}/stow``. Here is a sample call::

  # curl http://localhost:8042/dicom-web/servers/sample/stow -X POST -d @- << EOF
  {
    "Resources" : [
      "6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228"
    ]
  }
  EOF

Note that this primitive takes as its input a list of :ref:`Orthanc
identifiers <orthanc-ids>` corresponding to the resources (patients,
studies, series and/or instances) to be exported.

Remark 1: Additional HTTP headers can be added with an optional
``HttpHeaders" argument`` as for QIDO-RS and WADO-RS. This might be
useful e.g. for cookie-based session management.

Remark 2: One call to this ``.../stow`` primitive will possibly result
in several HTTP requests to the DICOMweb server, in order to limit the
size of the HTTP messages. The configuration options
``DicomWeb.StowMaxInstances`` and ``DicomWeb.StowMaxSize`` can be used
to tune this behavior (set both options to 0 to send one single
request).


Retrieving DICOM resources from a WADO-RS server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

Once DICOM resources of interest have been identified through a
QIDO-RS call to a remote DICOMweb server (cf. above), it is
interesting to download them locally with a WADO-RS call. You could do
it manually with a second call to the
``/{dicom-web-root}/servers/{name}/get`` URI, but Orthanc provides
another primitive ``.../retrieve`` to automate this process.

Here is how you would download one study, one series and one instance
whose StudyInstanceUID (0020,000d), SeriesInstanceUID (0020,000e) are
SOPInstanceUID (0008,0018) have been identified through a former
QIDO-RS call::

  # curl http://localhost:8042/dicom-web/servers/sample/retrieve -X POST -d @- << EOF
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
available, as for QIDO-RS.



Additional samples
------------------

Samples of how to call DICOMweb services from standalone applications
are available for `Python
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Resources/Samples/Python/>`__
and for `JavaScript
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Resources/Samples/JavaScript>`__.

Some integration tests are also `available separately
<https://bitbucket.org/sjodogne/orthanc-tests/src/default/Plugins/DicomWeb/Run.py>`__
(work in progress).
