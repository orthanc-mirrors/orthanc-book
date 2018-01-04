.. _postgresql:


PostgreSQL plugins
==================

.. contents::

The Orthanc project provides two **official** plugins to replace the
default storage area (on the filesystem) and the default SQLite index
by a PostgreSQL database.

For general information, check out the `official homepage of the
plugins <http://www.orthanc-server.com/static.php?page=postgresql>`__.



Compilation
-----------

Static linking
^^^^^^^^^^^^^^

.. highlight:: text

The procedure to compile these plugins is similar of that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce 2 shared libraries, each containing one plugin for Orthanc:

* ``OrthancPostgreSQLIndex`` replaces the default SQLite index of Orthanc by PostgreSQL. 
* ``OrthancPostgreSQLStorage`` makes Orthanc store the DICOM files it receives into PostgreSQL. 

  
Microsoft Windows and Apple OS X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pre-compiled binaries for Microsoft Windows `are also available
<http://www.orthanc-server.com/browse.php?path=/plugin-postgresql>`__.
A package for `Apple's Mac OS X
<http://www.osimis.io/en/download.html>`__
is available courtesy of `Osimis <http://osimis.io/>`__.


Dynamic linking on Ubuntu 16.04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

If static linking is not desired, here are build instructions for
Ubuntu 16.04 (provided build dependencies for the :ref:`core of
Orthanc <compiling>` have already been installed)::

  $ sudo apt-get install libpq-dev postgresql-server-dev-all
  $ cmake .. -DCMAKE_BUILD_TYPE=Release \
             -DALLOW_DOWNLOADS=ON \
             -DUSE_SYSTEM_GOOGLE_TEST=OFF \
             -DUSE_SYSTEM_ORTHANC_SDK=OFF
  $ make

  
Usage
-----

.. highlight:: json

You of course first have to :ref:`install Orthanc <binaries>`, with a
version above 0.9.1. You then have to **create a database** dedicated
to Orthanc on some PostgreSQL server. Please refer to the `PostgreSQL
documentation
<https://www.postgresql.org/docs/current/static/tutorial-createdb.html>`__.

Once Orthanc is installed and the database is created, you must add a
section in the :ref:`configuration file <configuration>` that
specifies the address of the **PostgreSQL server together with your
credentials**. You also have to tell Orthanc in which path it can find
the plugins: This is done by properly modifying the ``Plugins``
option. You could for instance adapt the following configuration
file::

  {
    "Name" : "MyOrthanc",
    [...]
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "Host" : "localhost",
      "Port" : 5432,
      "Database" : "orthanc",
      "Username" : "orthanc",
      "Password" : "orthanc"
    },
    "Plugins" : [
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLIndex.so",
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLStorage.so"
    ]
  }

Note that ``EnableIndex`` and ``EnableStorage`` must be explicitly set
to true, otherwise Orthanc will continue to use its default SQLite
back-end.

**Remark:** When using the ``Storage`` PostgreSQL plugin, the DICOM files are stored as large objects in the database.  This might actually consume more space than the DICOM file itself.  We have observed overhead up to 40%.  However, it seems this overhead is temporary and comes from Write-Ahead Logging.  Check this `discussion <https://groups.google.com/d/msg/orthanc-users/pPzHOpb--iw/QkKZ808gIgAJ>`__ on the Orthanc Users group for more info).  

Note that a typical usage of the PostgreSQL plugin is to enable only the ``Index`` and continue using the default filesystem storage for DICOM files.



.. highlight:: text

Orthanc must of course be **restarted** after the modification of its
configuration file. The log will contain an output similar to::

  $ ./Orthanc Configuration.json
  W0212 16:30:34.576972 11285 main.cpp:632] Orthanc version: 0.8.6
  W0212 16:30:34.577386 11285 OrthancInitialization.cpp:80] Using the configuration from: Configuration.json
  [...]
  W0212 16:30:34.598053 11285 main.cpp:379] Registering a plugin from: /home/jodogne/Subversion/OrthancPostgreSQL/Build/libOrthancPostgreSQLIndex.so
  W0212 16:30:34.598470 11285 PluginsManager.cpp:258] Registering plugin 'postgresql-index' (version 1.0)
  W0212 16:30:34.598491 11285 PluginsManager.cpp:148] Using PostgreSQL index
  W0212 16:30:34.608289 11285 main.cpp:379] Registering a plugin from: /home/jodogne/Subversion/OrthancPostgreSQL/Build/libOrthancPostgreSQLStorage.so
  W0212 16:30:34.608916 11285 PluginsManager.cpp:258] Registering plugin 'postgresql-storage' (version 1.0)
  W0212 16:30:34.608947 11285 PluginsManager.cpp:148] Using PostgreSQL storage area
  [...]
  W0212 16:30:34.674648 11285 main.cpp:530] Orthanc has started


.. highlight:: json

Instead of specifying explicit authentication parameters, you can also
use the `PostgreSQL connection URIs syntax
<https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING>`__. For
instance::

  {
    "Name" : "MyOrthanc",
    [...]
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "ConnectionUri" : "postgresql://username:password@localhost:5432/database"
    },
    "Plugins" : [
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLIndex.so",
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLStorage.so"
    ]
  }


**Remark:** The Debian Med project maintains `another useful set of
instructions
<https://anonscm.debian.org/viewvc/debian-med/trunk/packages/orthanc-postgresql/trunk/debian/README.Debian?view=markup>`__.


Advanced options
----------------

Several advanced options are available as well to fine-tune the
configuration of the PostgreSQL plugins. They are documented below.


Locking
^^^^^^^

.. highlight:: json

By default, the plugins lock the database (using `PostgreSQL advisory
locks
<https://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS>`__)
to prevent other instances of Orthanc from using the same PostgreSQL
database. If you want several instances of Orthanc to share the same
database, set the ``Lock`` option to ``false`` in the configuration
file::

  {
    "Name" : "MyOrthanc",
    [...]
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "Lock" : false,
      "ConnectionUri" : "postgresql://username:password@localhost:5432/database"
    },
    "Plugins" : [
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLIndex.so",
      "/home/user/OrthancPostgreSQL/Build/libOrthancPostgreSQLStorage.so"
    ]
  }

Obviously, one must be very cautious when sharing the same database
between instances of Orthanc. In particular, all these instances
should share the same configuration.


Keep-alive
^^^^^^^^^^

.. highlight:: text

After some period of inactivity (users have reported 10 hours), you
might `experience an error
<https://bitbucket.org/sjodogne/orthanc/issues/15/postgresql-exceptions-after-time>`__
such as::

  E0220 03:20:51.562601 PluginsManager.cpp:163] Exception in database back-end: Error in PostgreSQL: server closed the connection unexpectedly.
  This probably means the server terminated abnormally before or while processing the request.
  E0220 06:51:03.924868 PluginsManager.cpp:163] Exception in database back-end: Error in PostgreSQL: no connection to the server

This is due to a timeout in the PostgreSQL server. Please make sure to
`enable keep-alive
<http://dba.stackexchange.com/questions/97534/is-there-a-timeout-option-for-remote-access-to-postgresql-database>`__
in the configuration of your PostgreSQL server
