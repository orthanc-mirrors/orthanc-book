.. _authorization:


Advanced authorization plugin
=============================

.. contents::

This **official plugin** extends Orthanc with an advanced
authorization mechanism. For each incoming REST request to some URI,
the plugin will query a Web service to know whether the access is
granted to the user. If access is not granted, the HTTP status code is
set to ``403`` (Forbidden).

**Status:** This plugin was `deprecated
<https://discourse.orthanc-server.org/t/advanced-authorization-plugin-vs-remote-access/1859/5?u=jodogne>`__
between 2020 and 2022, but its active development has been resumed
since May 2022.


How to get it ?
---------------

The source code is available on `Mercurial <https://orthanc.uclouvain.be/hg/orthanc-authorization/>`__.

Binaries are included in:

- The `osimis/orthanc Docker image <https://hub.docker.com/r/osimis/orthanc>`__
- The `Windows Installer <https://www.orthanc-server.com/download-windows.php>`__
- The `MacOS packages <https://www.orthanc-server.com/static.php?page=download-mac>`__

Release notes are available `here <https://orthanc.uclouvain.be/hg/orthanc-authorization/file/tip/NEWS>`__.

Compilation instructions are available below.


Usage
-----

.. highlight:: json

Once Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancAuthorization/Build/libOrthancAuthorization.so"
    ],
    "Authorization" : {
      "WebServiceRootUrl" : "http://localhost:8000/",
      "WebServiceUsername": "my-user",
      "WebServicePassword": "my-password"
    }
  }

Orthanc must of course be restarted after the modification of its
configuration file.


Web Service
-----------

This section describes how a Web service suitable for the
authorization plugin can be designed.


Incoming request
^^^^^^^^^^^^^^^^

For each HTTP/REST request that Orthanc receives, the plugin will
issue a set of HTTP ``POST`` requests against the Web service that is
specified in the configuration file (in the basic configuration file
above, the Web service listening at ``http://localhost:8000/tokens/validate`` is
used). The body of each of those ``POST`` requests is a JSON file
similar to the following one::

  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8",
    "server-id": null,
    "uri": null
  }

In this example, the user is accessing an URI that is related to some
DICOM resource, namely a patient whose DICOM identifier is
``123ABC``. In such a case, the following fields will be set in the
JSON body:
 
* The ``level`` field specifies which type of resource the user is
  accessing, according to the :ref:`DICOM model of the real world
  <model-world>`. This field can be set to ``patient``, ``study``,
  ``series``, or ``instance``.
* The ``method`` field specifies which HTTP method is used by the
  to-be-authorized request. It can be set to ``get``, ``post``,
  ``delete``, or ``put``.
* The ``dicom-uid`` field gives the :ref:`DICOM identifier
  <dicom-identifiers>` of the resource that is accessed. If the
  resource is a patient, this field contains the ``PatientID`` DICOM
  tag. For a study, it contains its ``StudyInstanceUID``.  For a
  series, it contains its ``SeriesInstanceUID``. For an instance, it
  contains its ``SOPInstanceUID``.
* The ``orthanc-id`` field gives the :ref:`Orthanc identifier
  <orthanc-ids>` of the resource.
* The ``server-id`` field contains the value of the ``WebServiceIdentifier``
  configuration or ``null`` if this configuration is not defined.  This allows
  the WebService to identity which Orthanc instance is calling it (new in v 0.3.0).

When the user accesses a lower-level resource in the DICOM hierarchy
(a study, a series or an instance), the authorization plugin will
issue one separate call to the Web service for each level of the
hierarchy.  For instance, here are the 3 successive requests that are
issued when accessing some series::

  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8"
  }
  {
    "dicom-uid" : "1.3.51.0.1.1.192.168.29.133.1681753.1681732",
    "level" : "study",
    "method" : "get",
    "orthanc-id" : "6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12"
  }
  {
    "dicom-uid" : "1.3.12.2.1107.5.2.33.37097.2012041612474981424569674.0.0.0",
    "level" : "series",
    "method" : "get",
    "orthanc-id" : "6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228"
  }

It the user is accessing a URI that is not directly related to an
individual DICOM resource, the JSON body will look as follows::
 
  {
    "level" : "system",
    "method" : "get",
    "uri" : "/changes"
  }

In such a situation, the following fields are set:

* The ``level`` field is always set to ``system``.
* The ``method`` field is the same as above.
* The ``uri`` field provides the URI that was accessed by the user.
  
**Important note:** The plugin will transparently parse the URIs of
the core :ref:`REST API of Orthanc <rest>`, of the :ref:`Web viewer
plugin <webviewer>`, of the :ref:`DICOMweb plugin <dicomweb>`, and of
the :ref:`whole-slide imaging plugin <wsi>`. Unrecognized URIs (such
as those introduced by other plugins) will be handled as a ``system``
call. It is possible to introduce parsing support for more plugins by
modifying the ``DefaultAuthorizationParser`` C++ class in the source
code of the plugin.
  

Expected answer
^^^^^^^^^^^^^^^

The Web service must answer by sending a JSON file that tells whether
the access is granted or not to the user. Here is a sample answer::

  {
    "granted": true,
    "validity" : 5
  }

Here is a description of these two fields:

* ``granted`` tells whether access to the resource is granted
  (``true``) or not granted (``false``). In the case the user is
  accessing a DICOM resource, the access to *all* the levels of the
  hierarchy above this resource must be granted (logical conjunction
  over the levels).
* ``validity`` tells the authorization plugin for how many seconds the
  result of the Web service must be cached. If set to ``0`` second,
  the cache entry will never expire.

**Note:** The source code of the plugin contains a `basic example
<https://orthanc.uclouvain.be/hg/orthanc-authorization/file/default/Resources/TestService.js>`__
of such a Web service written in node.js.


Authentication tokens
^^^^^^^^^^^^^^^^^^^^^

It is obviously desirable to limit access to the resources depending
on the user that is logged in. Real-life Web framework such as Django
would send the identity of the authenticated user either as an HTTP
header, or as an additional argument for ``GET`` requests. The
authorization plugin allows to forward these authentication tokens to
the Web service.

To configure the authentication plugin to use some HTTP header, one
must provide the option ``TokenHttpHeaders`` the configuration file of
Orthanc as follows::

  {
    "Name" : "MyOrthanc",
    [...]
    "Authorization" : {
      "WebService" : "http://localhost:8000/",
      "TokenHttpHeaders" : [ "token" ]
    }
  }

.. highlight:: text

In such a situation, if some HTTP client issues the following call::

  # curl -H 'token: my-token' http://localhost:8042/patients/6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8

.. highlight:: json

Here is the JSON body the Web service would receive::

  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8",
    "token-key" : "token",
    "token-value" : "my-token"
  }

.. highlight:: text

Note how the key and the value of the authentication token stored as a
HTTP header are forwarded to the Web service.

The same mechanism can be used if the authentication token is provided
as some ``GET`` argument by setting the ``TokenGetArguments``
configuration option::

  # curl http://localhost:8042/patients/6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8?token=my-token
  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8",
    "token-key" : "token",
    "token-value" : "my-token"
  }

**Note 1:** It is allowed to provide a list of HTTP tokens or a list
of ``GET`` arguments in the configuration options. In this case, the
authorization plugin will loop over all the available authentication
tokens, until it finds one for which the access is granted (logical
disjunction over the authentication tokens).

**Note 2:** The cache entry that remembers whether some access was
granted in the past, depends on the value of the token.

**Note 3:** The support of authentication tokens provided as ``GET``
arguments requires a version of Orthanc that is above 1.2.1.


Full configuration
------------------

.. highlight:: json

The full list of configuration is available `here <https://orthanc.uclouvain.be/hg/orthanc-authorization/file/tip/Plugin/DefaultConfiguration.json>`__.

Here is the list of all the configuration options::

  {
    "Authorization" : {
        // The Base URL of the auth webservice.  This is an alias for all 3 next configurations:
        // // "WebServiceUserProfileUrl" : " ROOT /user/get-profile",
        // // "WebServiceTokenValidationUrl" : " ROOT /tokens/validate",
        // // "WebServiceTokenCreationBaseUrl" : " ROOT /tokens/",
        // // "WebServiceTokenDecoderUrl" : " ROOT /tokens/decode",
        // You should define it only if your auth webservice implements all 3 routes !
        // "WebServiceRootUrl" : "http://change-me:8000/",

        // The URL of the auth webservice route implementing user profile (optional)
        // (this configuration was previously named "WebService" and its old name is still accepted
        //  for backward compatibility)
        // "WebServiceUserProfileUrl" : "http://change-me:8000/user/profile",

        // The URL of the auth webservice route implementing resource level authorization (optional)
        // "WebServiceTokenValidationUrl" : "http://change-me:8000/tokens/validate",

        // The Base URL of the auth webservice route to create tokens (optional)
        // "WebServiceTokenCreationBaseUrl" : "http://change-me:8000/tokens/",

        // The URL of the auth webservice route implementing token decoding (optional)
        // "WebServiceTokenDecoderUrl": "http://change-me:8000/tokens/decode"

        // The username and password to connect to the webservice (optional)
        //"WebServiceUsername": "change-me",
        //"WebServicePassword": "change-me",
        
        // An identifier added to the payload of each request to the auth webservice (optional)
        //"WebServiceIdentifier": "change-me"

        // The name of the HTTP headers that may contain auth tokens
        //"TokenHttpHeaders" : [],
        
        // The name of the GET arguments that may contain auth tokens
        //"TokenGetArguments" : [],

        // A list of predefined configurations for well-known plugins
        // "StandardConfigurations": [               // new in v 0.4.0
        //     "osimis-web-viewer",
        //     "stone-webviewer",
        //     "orthanc-explorer-2"
        // ],

        //"UncheckedResources" : [],
        //"UncheckedFolders" : [],
        //"CheckedLevel" : "studies",
        //"UncheckedLevels" : [],

        // Definition of required "user-permissions".  This can be fully customized.
        // You may define other permissions yourself as long as they match the permissions
        // provided in the user-profile route implemented by the auth-service.
        // You may test your regex in https://regex101.com/ by selecting .NET (C#) and removing the leading ^ and trailing $
        // The default configuration is suitable for Orthanc-Explorer-2 (see https://github.com/orthanc-team/orthanc-auth-service)
        "Permissions" : [
            ["post", "^/auth/tokens/decode$", ""],
            ["post", "^/tools/lookup$", ""], 

            // elemental browsing in OE2
            ["post", "^/tools/find$", "all|view"],
            ["get" , "^/(patients|studies|series|instances)/([a-f0-9-]+)$", "all|view"],
            ...
        ]
    }
  }

The following options have been described above: ``WebServiceRootUrl``,
``TokenGetArguments``, and ``TokenHttpHeaders``. Here are the
remaining options:

* ``StandardConfigurations`` is a helper configuration to pre-populate
  ``UncheckedResources``, ``UncheckedFolders``, ``TokenGetArguments``,
  and ``TokenHttpHeaders`` of well-known plugins.
  Allowed values are ``osimis-web-viewer``, ``stone-webviewer``.

* ``CheckedLevel`` may replace ``UncheckedLevels`` when authorization
  is checked only at one level of the DICOM hierarchy.  This is the most
  common use-case.

* ``UncheckedResources`` specifies a list of resources for which the
  authentication plugin is not triggered, and to which access is
  always granted.

* ``UncheckedFolders`` is similar to ``UncheckedResources`` for folders:
  Access to all the URIs below the unchecked folders is always granted.

* ``UncheckedLevels`` allows to specify which levels of the
  :ref:`DICOM hierarchy <model-world>` are ignored by the authorization
  plugin. This can be used to reduce the number of calls to the Web
  service. Think for instance about an authorization mechanism that
  simply associates its studies to a set of granted users: In this case,
  the series and instance levels can be ignored.


Here is a minimal configuration for the :ref:`Stone Web viewer <stone_webviewer>`::

  {
    // disable basic authentication since it is replaced by the authorization plugin
    "AuthenticationEnabled": false,

    "Authorization" : {
      "WebServiceTokenValidationUrl" : "http://localhost:8000/shares/validate",
      "StandardConfigurations": [
        "stone-webviewer"
      ],
      "CheckedLevel" : "studies"
    }
  }

.. _orthanc-explorer-2-authorization:

Integration with the Orthanc Explorer 2
---------------------------------------

This project contains a `complete example <https://github.com/orthanc-team/orthanc-auth-service>`__ 
of a Web services integrating with :ref:`Orthanc Explorer 2 <orthanc-explorer-2>` to implement
user level permissions and sharing of single studies.

This sample also shows how to implement all routes that the webservice might provide:

- ``/tokens/validate`` to validate tokens identifying either a user or granting access to a single resource
- ``/tokens/{token_type}`` to generate tokens granting access to specific DICOM resources.
- ``/tokens/decode`` to extract the info from a token
- ``/user/get-profile`` to return the user profile linked to a given token.  This profile
  includes a list of permissions.


.. _orthanc-explorer-authorization:

Integration with the Orthanc Explorer
-------------------------------------

Starting from Orthanc 1.5.8, you can pass authorization tokens in the
url search params when opening the Orthanc explorer, i.e.
``http://localhost:8042/app/explorer.html?token=1234``.  This token
will be included as an HTTP header in every request sent to the
Orthanc Rest API. It will also be included in the URL search params
when opening the Orthanc or :ref:`Osimis Web viewer
<osimis_webviewer>`.

Only 3 tokens name will be recognized and forwarded: ``token``, ``auth-token``
and ``authorization``.

Please note that the Orthanc Explorer has not been designed to handle
the authorization so, when an authorization is not granted, it will simply 
display an empty page or an error message.  


Compilation
-----------

.. highlight:: bash

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancAuthorization``
that contains the authorization plugin.
