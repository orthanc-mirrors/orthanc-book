.. _authorization:


Advanced authorization plugin
=============================

.. contents::

This **official plugin by Osimis** extends Orthanc with an advanced
authorization mechanism. For each incoming REST request to some URI,
the plugin will query a Web service to know whether the access is
granted to the user. If access is not granted, the HTTP status code is
set to ``403`` (Forbidden).

The `source code of this plugin
<https://bitbucket.org/osimis/orthanc-authorization>`__ is freely
available under the terms of the AGPLv3 license.


Compilation
-----------

.. highlight:: bash

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancAuthorization``
that contains the authorization plugin.

Usage
-----

.. highlight:: json

You of course first have to :ref:`install Orthanc <compiling>`. Once
Orthanc is installed, you must change the :ref:`configuration file
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
      "WebService" : "http://localhost:8000/"
    }
  }

Orthanc must of course be restarted after the modification of its
configuration file.


Web Service
-----------

This section describes how a Web service suitable for the
authorization plugin can be designed.

**Note:** The behavior described in this section is implemented by the
``AuthorizationWebService`` C++ class in the source code. It is
possible to define a different authorization back-end by deriving
from interface ``IAuthorizationService``.


Incoming request
^^^^^^^^^^^^^^^^

For each HTTP/REST request that Orthanc receives, the plugin will
issue a set of HTTP ``POST`` requests against the Web service that is
specified in the configuration file (in the basic configuration file
above, the Web service listening at ``http://localhost:8000/`` is
used). The body of each of those ``POST`` requests is a JSON file
similar to the following one::

  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8"
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
<https://bitbucket.org/osimis/orthanc-authorization/src/default/Resources/TestService.js>`__
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
      "TokenHttpHeaders" : [ "hello" ]
    }
  }

.. highlight:: text

In such a situation, if some HTTP client issues the following call::

  # curl -H 'hello: world' http://localhost:8042/patients/6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8

.. highlight:: json

Here is the JSON body the Web service would receive::

  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8",
    "token-key" : "hello",
    "token-value" : "world"
  }

.. highlight:: text

Note how the key and the value of the authentication token stored as a
HTTP header are forwarded to the Web service.

The same mechanism can be used if the authentication token is provided
as some ``GET`` argument by setting the ``TokenGetArguments``
configuration option::

  # curl http://localhost:8042/patients/6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8?hello=world
  {
    "dicom-uid" : "123ABC",
    "level" : "patient",
    "method" : "get",
    "orthanc-id" : "6eeded74-75005003-c3ae9738-d4a06a4f-6beedeb8",
    "token-key" : "hello",
    "token-value" : "world"
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

Here is the list of all the configuration options::

  {
    "Name" : "MyOrthanc",
    [...]
    "Authorization" : {
      "WebService" : "http://localhost:8000/",
      "TokenGetArguments" : [ "user" ],
      "TokenHttpHeaders" : [ "hello" ],
      "UncheckedResources" : [
        "/series",
        "/instances",
        "/patients",
        "/studies",
        "/plugins/explorer.js",
        "/system"
      ],
      "UncheckedFolders" : [
        "/app/",
        "/web-viewer/app/",
        "/web-viewer/libs/",
        "/wsi/app/"
      ],
      "UncheckedLevels" : [ "study" ]
    }
  }

The following options have been described above: ``WebService``,
``TokenGetArguments``, and ``TokenHttpHeaders``. Here are the
remaining options:

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
     
