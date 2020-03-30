.. _google:


Google Cloud Platform plugin
============================

.. contents::

   
Introduction
------------

Osimis freely provides the `source code
<https://bitbucket.org/osimis/orthanc-gcp/src>`__ of a plugin to
interface Orthanc with the Healthcare API of `Google Cloud Platform
(GCP) <https://en.wikipedia.org/wiki/Google_Cloud_Platform>`__ through
`DICOMweb <https://www.dicomstandard.org/dicomweb/>`__.

This GCP plugin turns Orthanc into a DICOMweb client connected to GCP
servers, enabling the upload of DICOM images using STOW-RS, the
querying of the cloud content using QIDO-RS, and the retrieval of
remote content using WADO-RS. These operations can be possibly
:ref:`scripted <dicomweb-client>` thanks to the REST API of Orthanc.

Concretely, the role of the GCP plugin is to `manage the credentials
<https://cloud.google.com/docs/authentication/>`__ to Google Cloud
Platform. It requires the official :ref:`DICOMweb plugin <dicomweb>`
to be installed, as all the user interactions are done through the
latter plugin. As soon as Orthanc is started, the GCP plugin
automatically acquires then periodically refreshes the access tokens,
transparently updating the remote :ref:`DICOMweb servers
<dicomweb-client-config>` that are known to the DICOMweb plugin. The
access tokens can be derived either from service accounts, or from
user accounts.

This page makes the assumption that you have created a Google Cloud
Platform project, in which you have enabled the `Healthcare API
<https://cloud.google.com/healthcare/>`__, and in which you have
created a `DICOM store
<https://cloud.google.com/healthcare/docs/how-tos/dicom>`__.



Compilation
-----------

.. highlight:: text

The procedure to compile the GCP plugin is similar of that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
on any recent UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation produces a shared library
``OrthancGoogleCloudPlatform`` that contains the GCP
plugin. Pre-compiled binaries for Microsoft Windows `are available
<https://www.orthanc-server.com/browse.php?path=/plugin-google-cloud>`__,
and are included in the `Windows installers
<https://www.orthanc-server.com/download-windows.php>`__.

Under the hood, the GCP plugin is built on the top of the official
`Google Cloud Platform C++ Client Libraries
<https://github.com/googleapis/google-cloud-cpp>`__.



Configuration
-------------

Dependencies
^^^^^^^^^^^^

As explained above, the GCP plugin requires Orthanc (with version
above 1.5.4), and the :ref:`official DICOMweb plugin <dicomweb>` to be
installed (with version above 1.0). All the communications with Google
Cloud Platform are done using the DICOMweb plugin, and the
responsibility of the GCP plugin is to aquire and periodically refresh
the access tokens whose lifetime is limited.


Common parameters
^^^^^^^^^^^^^^^^^

There are some common parameters to be set. Firstly, the ``Plugins``
:ref:`configuration option <configuration>` of Orthanc must contain
the path that contains the ``OrthancGoogleCloudPlatform`` shared
library.

Secondly, obtaining the access tokens for Google Cloud Platform
necessitates a sequence of HTTPS requests. As a consequence, the
Orthanc configuration must specify how the authenticity of the Google
servers is verified. You have two possibilities to that end:

1. Disabling the verification of the remote servers (**not recommended
   in production**). This is done by setting option ``HttpsVerifyPeers``
   to ``false``.

2. Providing a list of `trusted Certificate Authorities (CA)
   <https://curl.haxx.se/docs/sslcerts.html>`__ to the HTTPS client
   that is internally used by Orthanc (namely, `cURL
   <https://en.wikipedia.org/wiki/CURL>`__). This is done by properly
   setting ``HttpsCACertificates`` option, so that it points to a file
   containing a store of CA certificates. Depending on your operating
   system, this file can be found as follows:

   * On Debian-based system, the standard file
     ``/etc/ssl/certs/ca-certificates.crt`` can be used.
   * On other systems (including Microsoft Windows), the cURL project
     provides `CA certificates
     <https://curl.haxx.se/docs/caextract.html>`__ that are extracted
     from Mozilla.

Note that to debug HTTPS communications, you have the possibility of
setting the ``HttpVerbose`` configuration option of Orthanc to
``true``. It can also be useful to run Orthanc in ``--verbose`` mode
(check out :ref:`this page <log>`).



Service account
^^^^^^^^^^^^^^^

As explained on the `Google documentation
<https://cloud.google.com/docs/authentication>`__, *"a service account
is a Google account that represents an application, as opposed to
representing an end user"*. This is presumably the most common
situation in the case of Orthanc.

You first have to `create a service account
<https://cloud.google.com/docs/authentication/getting-started>`__ for
your application. This will produce a JSON file (say,
``dicom-osimis.json``) that you have to store securely on the server
that will run Orthanc.

.. highlight:: json

Secondly, you have to modify the :ref:`Orthanc configuration
<configuration>` in order to provide the GCP plugin with your service
account file and with the parameters of your `DICOM store
<https://cloud.google.com/healthcare/docs/how-tos/dicom>`__. Here is a
sample, minimalist configuration of Orthanc::

  {
    "HttpsCACertificates": "/etc/ssl/certs/ca-certificates.crt",
    "Plugins" : [ "." ],
    "GoogleCloudPlatform" : {
      "Accounts": {
        "my-google" : {
          "Project" : "osimis-test",
          "Location" : "europe-west2",
          "Dataset" : "test",
          "DicomStore" : "dicom",
          "ServiceAccountFile" : "dicom-osimis.json"
        }
      }
    }
  }


In this example, once the GCP plugin has succeeded to authenticate
using the service account, the DICOMweb plugin will provide access to
the cloud DICOM store at URI ``/dicom-web/servers/my-google/`` of the
REST API of Orthanc.


User account
^^^^^^^^^^^^

User account is an alternative to service account, and can be used
*"when the application needs to access resources on behalf of an end
user"* (check out the `Google documentation
<https://cloud.google.com/docs/authentication/end-user>`__).

.. highlight:: json

The easiest way of setting up a user account is through the `gcloud
command-line tool <https://cloud.google.com/sdk/gcloud/>`__.
`Google's quick-starts
<https://cloud.google.com/sdk/docs/quickstarts>`__ explain how to
initialize the environment depending on your operating system (check
out the "Initialize the SDK" sections, which essentially boil down to
calling ``gcloud init``).


.. highlight:: bash

Once the ``gcloud init`` command-line has been invoked, you can
extract credentials to be used by Orthanc by typing the following
command::

  $ gcloud auth print-access-token --format json


.. highlight:: json

This command generates a JSON file containing all the required
information, that can be written to a file (say,
``dicom-user.json``). Given this file, here is a sample, minimalist
configuration of Orthanc::

  {
    "HttpsCACertificates": "/etc/ssl/certs/ca-certificates.crt",
    "Plugins" : [ "." ],
    "GoogleCloudPlatform" : {
      "Accounts": {
        "my-google" : {
          "Project" : "osimis-test",
          "Location" : "europe-west2",
          "Dataset" : "test",
          "DicomStore" : "dicom",
          "AuthorizedUserFile" : "dicom-osimis.json"
        }
      }
    }
  }

In this example, once the GCP plugin has succeeded to authenticate
using the user account, the DICOMweb plugin will provide access to the
cloud DICOM store at URI ``/dicom-web/servers/my-google/`` of the REST
API of Orthanc.


.. highlight:: bash

Note that only 3 fields in the JSON file produced by the ``gcloud auth
print-access-token`` command are required: ``client_id``,
``client_secret``, and ``refresh_token``. Instead of using the full
JSON file, you can extract only these fields, e.g. using the `jq
<https://stedolan.github.io/jq/>`__ command-line tool::

  $ gcloud auth print-access-token --format json | jq '{ AuthorizedUserClientId: .client_id, AuthorizedUserClientSecret:.client_secret, AuthorizedUserRefreshToken:.refresh_token }'
  {
    "AuthorizedUserClientId": "XXXXXXXXXX.apps.googleusercontent.com",
    "AuthorizedUserClientSecret": "ZmssLNXXXXXX",
    "AuthorizedUserRefreshToken": "1/e2ngXXXXXX"
  }


.. highlight:: json

These fields can then be copied/pasted as follows in order to create a
configuration for Orthanc that is equivalent to the one using the
separate JSON file::
  
  {
    "HttpsCACertificates": "/etc/ssl/certs/ca-certificates.crt",
    "Plugins" : [ "." ],
    "GoogleCloudPlatform" : {
      "Accounts": {
        "my-google" : {
          "Project" : "osimis-test",
          "Location" : "europe-west2",
          "Dataset" : "test",
          "DicomStore" : "dicom",
          "AuthorizedUserClientId": "XXXXXXXXXX.apps.googleusercontent.com",
          "AuthorizedUserClientSecret": "ZmssLNXXXXXX",
          "AuthorizedUserRefreshToken": "1/e2ngXXXXXX"
        }
      }
    }
  }


Advanced options
^^^^^^^^^^^^^^^^

.. highlight:: json

Some advanced configuration options are available as well, as
summarized in this excerpt::

  {
    ...
    // In seconds, must be large enough to send/receive your largest studies
    // using WADO or STOW, depending on the speed of your Internet connection
    "HttpTimeout" : 600,

    "GoogleCloudPlatform" : {
      ...
       // Path to the URL of the GCP services
      "BaseUrl" : "https://healthcare.googleapis.com/v1beta1/"
    }
  }
