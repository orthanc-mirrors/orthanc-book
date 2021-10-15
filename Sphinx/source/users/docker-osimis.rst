.. _docker-osimis:
.. highlight:: bash


Osimis Orthanc Docker images
============================

.. contents::
   :depth: 3


.. warning:: This documentation applies to ``osimis/orthanc`` images from the ``20.4.2`` version.  
  
  Note that these images have been re-written in April 2020.  The documentation
  for older images is still available `here <https://osimis.atlassian.net/wiki/spaces/OKB/pages/26738689/How+to+use+osimis+orthanc+Docker+images#Howtouseosimis/orthancDockerimages>`__
  
  The new images are backward compatible with the previous images except for the
  Google Cloud Platform configuration.  
  
  However, if you're still using legacy environment variables, you'll get some warning
  encouraging you to update to the new namings since the backward compatibility
  might be removed one day (currently planed in June 2021).


Introduction
------------

Our commercial partner `Osimis <https://www.osimis.io>`__ 
`publishes separated Docker images
<https://hub.docker.com/r/osimis/orthanc>`__
that are used by their technical team in order to provide professional 
support to their customers.

These images have been designed to be used with ``docker-compose`` and 
provide a configuration system through:

- environment variables
- Docker secrets
- classical configuration files
- a mix of these options

This `repository <https://bitbucket.org/osimis/orthanc-setup-samples/src>`__
contains lots of examples on how to use these images.  In particular,
`this example <https://bitbucket.org/osimis/orthanc-setup-samples/src/master/docker/all-usages/docker-compose.yml>`__ 
shows all the way that can be used to generate the same
configuration in Orthanc.


Environment variables
---------------------

Any part of the Orthanc configuration file can be configured through an
environment variable.  Now that Orthanc and its plugins have hundreds of
configuration parameter, listing all these environment variable would be
too long.  That's why we have defined a standard way of naming the variable:

+---------------------------+----------------------------------------------+----------------------------------------------------------------+
| Orthanc configuration     | Environment variable                         | Sample value                                                   |
+===========================+==============================================+================================================================+
| StableAge                 | ORTHANC__STABLE_AGE                          | ``30``                                                         |
+---------------------------+----------------------------------------------+----------------------------------------------------------------+
| DicomWeb.Root             | ORTHANC__DICOM_WEB__ROOT                     | ``/dicom-web/``                                                |
+---------------------------+----------------------------------------------+----------------------------------------------------------------+
| DicomWeb.Servers          | ORTHANC__DICOM_WEB__SERVERS                  | ``{"sample": [ "http://127.0.0.1/dicom-web/"]}``               |
+---------------------------+----------------------------------------------+----------------------------------------------------------------+

To find out an environment variable name from an Orthanc setting
(i.e. ``DicomWeb.StudiesMetadata`` is the ``path`` to a setting):

- whenever a word contains a capital letter, insert an underscore ``_`` in front.
  ``DicomWeb.StudiesMetadata`` now becomes ``Dicom_Web.Studies_Metadata``
- whenever you go down one level in the JSON configuration, insert
  a double underscore ``__``.  ``Dicom_Web.Studies_Metadata`` now becomes
  ``Dicom_Web__Studies_Metadata``
- capitalize all letters.  ``Dicom_Web__Studies_Metadata`` now becomes
  ``DICOM_WEB__STUDIES_METADATA``
- add ``ORTHANC__`` in front.  ``DICOM_WEB__STUDIES_METADATA`` now becomes
  ``ORTHANC__DICOM_WEB__STUDIES_METADATA``

Note that, this automatic rule might fail because of 2 capital letters one after each other in some
Orthanc settings.  Therefore, there are some `exceptions <https://bitbucket.org/osimis/orthanc-builder/src/master/docker/orthanc/env-var-non-standards.json>`__ to this rule 
that are however quite intuitive.

Special environment variables
-----------------------------

Other environment variables are not related to the Orthanc configuration file
but can be specified to control the way Orthanc is run.

- ``VERBOSE_STARTUP=true`` will allow you to debug the startup process and see
  the configuration that has been provided to Orthanc.  This setup should be
  disabled in production since it might display secret information like passwords
  in your logs
- ``VERBOSE_ENABLED=true`` will start Orthanc with the ``--verbose`` option
- ``TRACE_ENABLED=true`` will start Orthanc with the ``--trace`` option
- ``NO_JOBS=true`` will start Orthanc with the ``--no-jobs`` option
- ``UNLOCK=true`` will start Orthanc with the ``--unlock`` option
- ``LOGDIR=/logs`` will start Orthanc with the ``--logdir=/logs`` option (introduced in 21.9.1)
- ``LOGFILE=/logs`` will start Orthanc with the ``--logfile=/logs/orthanc.log`` option (introduced in 21.9.1)
- ``MALLOC_ARENA_MAX=10`` will :ref:`control memory usage <scalability-memory>`
- ``ORTHANC_JSON`` can be used to pass a JSON "root" configuration (see below).
- ``BEFORE_ORTHANC_STARTUP_SCRIPT`` can be used to `run a custom script <https://groups.google.com/g/orthanc-users/c/EXjTq2ZU1vw/m/02CwW1jzAQAJ>`__ before starting Orthanc.
  
Configuration files
-------------------

.. highlight:: yaml

Configuration files should be stored in the ``/etc/orthanc/`` folder inside the Docker image.  
This is done by building an image thanks to a ``Dockerfile``::

  FROM osimis/orthanc
  COPY orthanc.json /etc/orthanc/


Configuration files can also be passed as secrets as shown in this ``docker-compose.yml``::

  version: "3.3"
    services:
      orthanc-file-in-secrets:
        image: osimis/orthanc
        depends_on: [index-db]
        ports: ["8201:8042"]
        environment:
          VERBOSE_STARTUP: "true"

        secrets:
          - orthanc.secret.json
    
    secrets:
      orthanc.secret.json:
        file: orthanc.secret.json

Finally, a whole configuration file can be passed as a JSON through the ``ORTHANC_JSON`` environment variable::

  version: "3.3"
    services:
      orthanc-file-in-env-var:
        image: osimis/orthanc
        depends_on: [index-db]
        ports: ["8200:8042"]
        environment:
          VERBOSE_ENABLED: "true"
          OSIMIS_WEB_VIEWER1_PLUGIN_ENABLED: "true"

          ORTHANC_JSON: |
            {
              "Name": "orthanc-file-in-env-var",
              "PostgreSQL" : {
                "Host": "index-db",
                "Password": "pg-password"
              },
              "RegisteredUsers": {
                "demo": "demo"
              }
            }


Docker secrets
--------------

.. highlight:: yaml

When using your container in a ``Docker Swarm`` or ``Kubernetes`` environment,
it is usually advised to pass sensitive information through ``Docker Secrets``.
For this purpose, any secret whose name is similar to the name of an 
environment variable is considered as an environment variable::

  version: "3.3"
    services:
      orthanc-with-direct-secret:
        image: osimis/orthanc
        depends_on: [index-db]
        ports: ["8003:8042"]
        environment:
          ORTHANC__NAME: "orthanc-with-direct-secret"
          VERBOSE_ENABLED: "true"

          OSIMIS_WEB_VIEWER1_PLUGIN_ENABLED: "true"

          ORTHANC__POSTGRESQL__HOST: "index-db"
          ORTHANC__REGISTERED_USERS: |
            {"demo": "demo"}

      secrets:
        - ORTHANC__POSTGRESQL__PASSWORD
    secrets:
      ORTHANC__POSTGRESQL__PASSWORD:
        file: ORTHANC__POSTGRESQL__PASSWORD


Mixing configuration
--------------------

Parts of your configuration can be defined in a configuration file, 
another part in an environment variable and yet another in a secret.
If the same setting is defined in multiple location, the latest one
will overwrite the first.  Settings are evaluated in this order:

- JSON files from ``/etc/orthanc/``
- JSON files from ``/run/secrets`` (Docker secrets are copied there
  by Docker)
- environment variables
- secret environment variables

At this point, if some settings have not been defined yet, some defaults
are applied (see below).


Default configuration
---------------------

.. highlight:: json

Orthanc and each plugin might have some default settings that might
eventually be different from the defaults included in the Orthanc 
executable or the plugin library.  

.. below json is copied from orthanc-builder/docker/orthanc/orthanc-defaults.json

Orthanc non-standard defaults::

  {
    "StorageDirectory" : "/var/lib/orthanc/db",

    "RemoteAccessAllowed": true,
    "AuthenticationEnabled": true,
    
    "HttpsCACertificates" : "/etc/ssl/certs/ca-certificates.crt",

    "Plugins" : ["/usr/share/orthanc/plugins/"]
  }
  

Default Lua scripts
-------------------

Some Lua scripts are already loaded in the image but are not configured to 
be loaded by Orthanc automatically.  You'll have to add them to the ``"LuaScripts"`` 
configuration if you want to use them.

`/lua-scripts/filter-http-tools-reset.lua <https://bitbucket.org/osimis/orthanc-builder/src/master/docker/orthanc/filter-http-tools-reset.lua>`__ 
can be used to regenerate the ``/tmp/orthanc.json`` configuration file that is loaded by Orthanc every time
you POST to ``/tools/reset``.  Note that it declares an ``IncomingHttpRequestFilter`` 
callback that might conflict with your scripts.

Healthcheck probe
-----------------

In version 21.10.0, the `/probes/test-aliveness.py <https://bitbucket.org/osimis/orthanc-builder/src/master/docker/orthanc/test-aliveness.py>`__ 
script has been added in order to perform healthchecks.  Check the doc in the script itself for more details.
A sample configuration is also available in `this sample <https://bitbucket.org/osimis/orthanc-setup-samples/src/8016d140a237a892db703aac4782307c46732847/docker/tls-mutual-auth/docker-compose.yml#lines-51>`__


Plugins
-------

Plugins are automatically enabled as soon as you define a setting
in their JSON section or as soon as you define to ``true`` their
specific environment variable.

Below is a list of all plugins, their environment variable and their default configuration 
(only when their default configuration is different from the plugin defaults):


.. below table is obtained by running orthanc-builder/docker/orthanc/generatePluginDoc.py


+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| Plugin                                           | Environment variable                             | Default configuration                                                                              |
+==================================================+==================================================+====================================================================================================+
| **Authorization**                                | ``AUTHORIZATION_PLUGIN_ENABLED``                 |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **ConnectivityChecks**                           | ``CONNECTIVITY_CHECKS_PLUGIN_ENABLED``           |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **DicomWeb**                                     | ``DICOM_WEB_PLUGIN_ENABLED``                     | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "DicomWeb": {                                                                                  |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Gdcm**                                         | ``GDCM_PLUGIN_ENABLED``                          | .. code-block:: json                                                                               |
|                                                  | Note: enabled by default                         |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Gdcm": {                                                                                      |
|                                                  |                                                  |       "Throttling": 4,                                                                             |
|                                                  |                                                  |       "RestrictTransferSyntaxes": [                                                                |
|                                                  |                                                  |         "1.2.840.10008.1.2.4.90",                                                                  |
|                                                  |                                                  |         "1.2.840.10008.1.2.4.91",                                                                  |
|                                                  |                                                  |         "1.2.840.10008.1.2.4.92",                                                                  |
|                                                  |                                                  |         "1.2.840.10008.1.2.4.93"                                                                   |
|                                                  |                                                  |       ]                                                                                            |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **OrthancWebViewer**                             | ``ORTHANC_WEB_VIEWER_PLUGIN_ENABLED``            |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **StoneWebViewer**                               | ``STONE_WEB_VIEWER_PLUGIN_ENABLED``              |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **OsimisWebViewerBasic**                         | ``OSIMIS_WEB_VIEWER1_PLUGIN_ENABLED``            |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **OsimisWebViewerBasicAlpha**                    | ``OSIMIS_WEB_VIEWER1_ALPHA_PLUGIN_ENABLED``      |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **PostgreSQL**                                   | ``POSTGRESQL_PLUGIN_ENABLED``                    | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "PostgreSQL": {                                                                                |
|                                                  |                                                  |       "EnableIndex": true,                                                                         |
|                                                  |                                                  |       "EnableStorage": false,                                                                      |
|                                                  |                                                  |       "Port": 5432,                                                                                |
|                                                  |                                                  |       "Host": "HOST MUST BE DEFINED",                                                              |
|                                                  |                                                  |       "Database": "postgres",                                                                      |
|                                                  |                                                  |       "Username": "postgres",                                                                      |
|                                                  |                                                  |       "Password": "postgres",                                                                      |
|                                                  |                                                  |       "EnableSsl": false,                                                                          |
|                                                  |                                                  |       "Lock": false                                                                                |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **MySQL**                                        | ``MYSQL_PLUGIN_ENABLED``                         | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "MySQL": {                                                                                     |
|                                                  |                                                  |       "EnableIndex": true,                                                                         |
|                                                  |                                                  |       "EnableStorage": false,                                                                      |
|                                                  |                                                  |       "Port": 3306,                                                                                |
|                                                  |                                                  |       "Host": "HOST MUST BE DEFINED",                                                              |
|                                                  |                                                  |       "Database": "mysql",                                                                         |
|                                                  |                                                  |       "Username": "root",                                                                          |
|                                                  |                                                  |       "Password": "mysql",                                                                         |
|                                                  |                                                  |       "Lock": false                                                                                |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Python**                                       | ``PYTHON_PLUGIN_ENABLED``                        |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **ServeFolders**                                 | ``SERVE_FOLDERS_PLUGIN_ENABLED``                 |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Transfers**                                    | ``TRANSFERS_PLUGIN_ENABLED``                     |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Worklists**                                    | ``WORKLISTS_PLUGIN_ENABLED``                     | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Worklists": {                                                                                 |
|                                                  |                                                  |       "Enable": true,                                                                              |
|                                                  |                                                  |       "Database": "/var/lib/orthanc/worklists"                                                     |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Wsi**                                          | ``WSI_PLUGIN_ENABLED``                           |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Odbc**                                         | ``ODBC_PLUGIN_ENABLED``                          | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Odbc": {                                                                                      |
|                                                  |                                                  |       "EnableIndex": true,                                                                         |
|                                                  |                                                  |       "EnableStorage": false,                                                                      |
|                                                  |                                                  |       "IndexConnectionString": "MUST BE DEFINED",                                                  |
|                                                  |                                                  |       "StorageConnectionString": "MUST BE DEFINED"                                                 |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Tcia**                                         | ``TCIA_PLUGIN_ENABLED``                          | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Tcia": {                                                                                      |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Indexer**                                      | ``INDEXER_PLUGIN_ENABLED``                       | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Indexer": {                                                                                   |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+

Under the hood
--------------

The source code that is used to generate the image can be found `here <https://bitbucket.org/osimis/orthanc-builder/src/master/docker/orthanc/Dockerfile>`__.

The Python script that is used at startup can be found `here <https://bitbucket.org/osimis/orthanc-builder/src/master/docker/orthanc/generateConfiguration.py>`__
