.. _docker-orthancteam:
.. highlight:: bash


orthancteam/orthanc Docker images
=================================

.. contents::
   :depth: 3

.. warning:: 
  Starting from February 2024, the ``osimis/orthanc`` Docker images have been renamed
  into ``orthancteam/orthanc``.  The ``osimis/orthanc`` images won't be updated anymore
  therefore you should switch to the ``orthancteam/orthanc`` images.

  Note that all old tags released prior to February 2024 have been copied into ``orthancteam/orthanc``
  as well so, even if you are using an old version, you should update the name in your setup.
  The name is the only thing that has changed.  The content and build procedure are identical.

The ``orthancteam/orthanc`` images are updated regularly.  The release notes are available `here <https://github.com/orthanc-server/orthanc-builder/blob/master/release-notes-docker-images.md>`__.

.. warning:: 

  Starting from the ``22.6.1`` release, we are providing 2 types of images:
  
  - the default image with the usual tag: e.g ``22.6.1``
  - the full image with a e.g ``22.6.1-full`` tag

  The default image is suitable for 99.9% of users.

  You should use the full image only if you need to use one of these:

  - the Azure Blob storage plugin
  - the Google Cloud storage plugin
  - the ODBC plugin with SQL Server (msodbcsql18 is preinstalled)


Introduction
------------

Our commercial partner `Orthanc Team <https://orthanc.team>`__ 
`publishes separated Docker images
<https://hub.docker.com/r/orthancteam/orthanc>`__.
These images have been designed to be used with ``docker-compose`` and 
provide a configuration system through:

- environment variables
- Docker secrets
- classical configuration files
- a mix of these options

This `repository <https://github.com/orthanc-server/orthanc-setup-samples/src>`__
contains lots of examples on how to use these images.  In particular,
`this example <https://github.com/orthanc-server/orthanc-setup-samples/tree/master/docker/all-usages/docker-compose.yml>`__ 
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
Orthanc settings.  Therefore, there are some `exceptions <https://github.com/orthanc-server/orthanc-builder/blob/master/docker/orthanc/env-var-non-standards.json>`__ to this rule 
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
- ``LOGDIR=/logs`` will start Orthanc with the ``--logdir=/logs`` option (introduced in 21.9.1)
- ``LOGFILE=/logs`` will start Orthanc with the ``--logfile=/logs/orthanc.log`` option (introduced in 21.9.1)
- ``MALLOC_ARENA_MAX=10`` will :ref:`control memory usage <scalability-memory>`
- ``ORTHANC_JSON`` can be used to pass a JSON "root" configuration (see below).
- ``BEFORE_ORTHANC_STARTUP_SCRIPT`` can be used to `run a custom script <https://groups.google.com/g/orthanc-users/c/EXjTq2ZU1vw/m/02CwW1jzAQAJ>`__ before starting Orthanc.
- ``FORCE_HOST_ID`` and ``GENERATE_HOST_ID_IF_MISSING`` can be used to control the content of /etc/hostid (introduced in 22.9.1). 
  DCMTK calls gethostid() when generating DICOM UIDs (used, e.g, in modifications/anonymizations).
  When /etc/hostid is missing, the system tries to generate it from the IP of the system.
  On some system, in particular circumstances, we have observed that the system performs a DNS query
  to get the IP of the system.  This DNS can timeout (after multiple with retries) and, in particular cases,
  we have observed a delay of 40 seconds to generate a single DICOM UID in Orthanc.
  Therefore, if /etc/hostid is missing, the startup script creates it and fill it with a random number (default behaviour).  
  This behaviour can still be deactivated by defining ``GENERATE_HOST_ID_IF_MISSING=false``.  
  The host id can also be forced by defining ``FORCE_HOST_ID``.



Configuration files
-------------------

.. highlight:: yaml

Configuration files should be stored in the ``/etc/orthanc/`` folder inside the Docker image.  
This is done by building an image thanks to a ``Dockerfile``::

  FROM orthancteam/orthanc
  COPY orthanc.json /etc/orthanc/


Configuration files can also be passed as secrets as shown in this ``docker-compose.yml``::

  version: "3.3"
    services:
      orthanc-file-in-secrets:
        image: orthancteam/orthanc
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
        image: orthancteam/orthanc
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
        image: orthancteam/orthanc
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

`/lua-scripts/filter-http-tools-reset.lua <https://github.com/orthanc-server/orthanc-builder/blob/master/docker/orthanc/filter-http-tools-reset.lua>`__ 
can be used to regenerate the ``/tmp/orthanc.json`` configuration file that is loaded by Orthanc every time
you POST to ``/tools/reset``.  Note that it declares an ``IncomingHttpRequestFilter`` 
callback that might conflict with your scripts.

Healthcheck probe
-----------------

In version 21.10.0, the `/probes/test-aliveness.py <https://github.com/orthanc-server/orthanc-builder/blob/master/docker/orthanc/test-aliveness.py>`__ 
script has been added in order to perform healthchecks.  Check the doc in the script itself for more details.
A sample configuration is also available in `this sample <https://github.com/orthanc-server/orthanc-setup-samples/tree/master/docker/health-check>`__


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
| **Housekeeper**                                  | ``HOUSEKEEPER_PLUGIN_ENABLED``                   | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Housekeeper": {                                                                               |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **DelayedDeletion**                              | ``DELAYED_DELETION_PLUGIN_ENABLED``              | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "DelayedDeletion": {                                                                           |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **MultitenantDicom**                             | ``MULTITENANT_DICOM_PLUGIN_ENABLED``             |                                                                                                    |
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
| **Neuro**                                        | ``NEURO_PLUGIN_ENABLED``                         | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "Neuro": {                                                                                     |
|                                                  |                                                  |       "Enable": true                                                                               |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **AzureBlobStorage**                             | ``AZURE_BLOB_STORAGE_PLUGIN_ENABLED``            | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "AzureBlobStorage": {                                                                          |
|                                                  |                                                  |       "ConnectionString": "MUST BE DEFINED BY YOU",                                                |
|                                                  |                                                  |       "ContainerName": "MUST BE DEFINED BY YOU"                                                    |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **AwsS3Storage**                                 | ``AWS_S3_STORAGE_PLUGIN_ENABLED``                | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "AwsS3Storage": {                                                                              |
|                                                  |                                                  |       "BucketName": "MUST BE DEFINED BY YOU",                                                      |
|                                                  |                                                  |       "Region": "MUST BE DEFINED BY YOU"                                                           |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **GoogleCloudStorage**                           | ``GOOGLE_CLOUD_STORAGE_PLUGIN_ENABLED``          | .. code-block:: json                                                                               |
|                                                  |                                                  |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "GoogleCloudStorage": {                                                                        |
|                                                  |                                                  |       "ServiceAccountFile": "MUST BE DEFINED BY YOU",                                              |
|                                                  |                                                  |       "BucketName": "MUST BE DEFINED BY YOU"                                                       |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **OrthancExplorer2**                             | ``ORTHANC_EXPLORER_2_ENABLED``                   | .. code-block:: json                                                                               |
|                                                  | Note: enabled by default                         |                                                                                                    |
|                                                  |                                                  |   {                                                                                                |
|                                                  |                                                  |     "OrthancExplorer2": {                                                                          |
|                                                  |                                                  |       "Enable": true,                                                                              |
|                                                  |                                                  |       "IsDefaultOrthancUI": false                                                                  |
|                                                  |                                                  |     }                                                                                              |
|                                                  |                                                  |   }                                                                                                |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **VolView**                                      | ``VOLVIEW_PLUGIN_ENABLED``                       |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **Ohif**                                         | ``OHIF_PLUGIN_ENABLED``                          |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+
| **STL**                                          | ``STL_PLUGIN_ENABLED``                           |                                                                                                    |
+--------------------------------------------------+--------------------------------------------------+----------------------------------------------------------------------------------------------------+


Under the hood
--------------

The source code that is used to generate the image can be found `here <https://github.com/orthanc-server/orthanc-builder/blob/master/docker/orthanc/Dockerfile>`__.

The Python script that is used at startup can be found `here <https://github.com/orthanc-server/orthanc-builder/blob/master/docker/orthanc/generateConfiguration.py>`__
