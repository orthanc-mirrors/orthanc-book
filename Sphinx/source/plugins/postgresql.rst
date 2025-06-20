.. _postgresql:


PostgreSQL plugins
==================

.. contents::

The Orthanc project provides two **official** plugins to replace the
default storage area (on the filesystem) and the default SQLite index
by a PostgreSQL database.

For general information, check out the `official homepage of the
plugins <https://www.orthanc-server.com/static.php?page=postgresql>`__.

For information about scalability, make sure to read the section about
:ref:`multiple writers in large-scale deployments <multiple-writers>`.


How to get it ?
---------------

The source code is available on `Mercurial <https://orthanc.uclouvain.be/hg/orthanc-databases/>`__, 
next to the source code of the :ref:`ODBC <odbc>` and :ref:`MySQL/MariaDB <mysql>` plugins.

Binaries are included in:

- The :ref:`orthancteam/orthanc Docker image <docker-orthancteam>`,
- The :ref:`jodogne/orthanc-plugins Docker image <docker>`,
- The `Windows installers <https://orthanc.uclouvain.be/downloads/windows-64/installers/index.html>`__,
- The `macOS packages <https://orthanc.uclouvain.be/downloads/macos/packages/index.html>`__.

Precompiled binaries of the plugin alone are also available for multiple platforms on the `official download site <https://orthanc.uclouvain.be/downloads/index.html>`__.
  
Release notes are available `here <https://orthanc.uclouvain.be/hg/orthanc-databases/file/default/PostgreSQL/NEWS>`__.

  
Usage
-----

.. highlight:: json

You of course first have to :ref:`install Orthanc <binaries>`, with a
version above 0.9.5. You then have to **create a database** dedicated
to Orthanc on some PostgreSQL server. Please refer to the `PostgreSQL
documentation
<https://www.postgresql.org/docs/current/tutorial-createdb.html>`__.

Once Orthanc is installed and the database is created, you must add a
section in the :ref:`configuration file <configuration>` that
specifies the address of the **PostgreSQL server together with your
credentials**. You also have to tell Orthanc in which path it can find
the plugins: This is done by properly modifying the ``Plugins``
option. You could for instance adapt the following configuration
file::

  {
    "Name" : "MyOrthanc",
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : false,               // You likely don't need to enable this option 
      "Host" : "localhost",
      "Port" : 5432,
      "Database" : "orthanc",
      "Username" : "orthanc",
      "Password" : "orthanc",
      "Lock" : true,
      "EnableSsl" : false,                   // New in release 3.0
      "MaximumConnectionRetries" : 10,       // New in release 3.0
      "ConnectionRetryInterval" : 5,         // New in release 3.0
      "IndexConnectionsCount" : 50,          // New in release 4.0 - new default value in 7.0
      "TransactionMode": "ReadCommitted",    // New in release 6.0 - new default value in 7.0
      "EnableVerboseLogs": false,            // New in release 6.0
      "HousekeepingInterval": 1,             // New in release 7.0
      "AllowInconsistentChildCounts": false  // New in release 7.2
    },
    "Plugins" : [
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLIndex.so",
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLStorage.so"
    ]
  }

**Important:** The ``EnableIndex`` and ``EnableStorage`` options must
be explicitly set to ``true``, otherwise Orthanc will continue to use
its default SQLite back-end and the filesystem storage area.

**Remark 1:** When using the ``Storage`` PostgreSQL plugin, the DICOM
files are stored as large objects in the database.  This might
actually consume more space than the DICOM file itself.  We have
observed overhead up to 40%.  However, it seems this overhead is
temporary and comes from Write-Ahead Logging.  Check this `discussion
<https://groups.google.com/d/msg/orthanc-users/pPzHOpb--iw/QkKZ808gIgAJ>`__
on the Orthanc Users group for more info).

**Remark 2:** A typical usage of the PostgreSQL plugin is to enable
only the ``Index``, and to use the default filesystem storage for
DICOM files (on a NAS with proper disaster recovery strategies). This
setup provides best performance for large-scale databases.

**Remark 3:** Setting the ``EnableSsl`` to ``true`` forces the use of
`SSL connections
<https://www.postgresql.org/docs/current/libpq-ssl.html>`__ between
Orthanc and the PostgreSQL server. It is a synonym for
``sslmode=require`` in connections URI (see below). Setting
``EnableSsl`` to ``false`` corresponds to ``sslmode=disable``
(i.e. SSL is not used, even if it is both available in Orthanc and
PostgreSQL). To choose other values for the SSL mode (i.e. ``allow``
and ``prefer``), please use connection URIs.



.. highlight:: text

Orthanc must of course be **restarted** after the modification of its
configuration file. The log will contain an output similar to::

  $ ./Orthanc Configuration.json
  W0212 16:30:34.576972 11285 main.cpp:632] Orthanc version: 0.8.6
  W0212 16:30:34.577386 11285 OrthancInitialization.cpp:80] Using the configuration from: Configuration.json
  [...]
  W0212 16:30:34.598053 11285 main.cpp:379] Registering a plugin from: /home/jodogne/Subversion/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLIndex.so
  W0212 16:30:34.598470 11285 PluginsManager.cpp:258] Registering plugin 'postgresql-index' (version 1.0)
  W0212 16:30:34.598491 11285 PluginsManager.cpp:148] Using PostgreSQL index
  W0212 16:30:34.608289 11285 main.cpp:379] Registering a plugin from: /home/jodogne/Subversion/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLStorage.so
  W0212 16:30:34.608916 11285 PluginsManager.cpp:258] Registering plugin 'postgresql-storage' (version 1.0)
  W0212 16:30:34.608947 11285 PluginsManager.cpp:148] Using PostgreSQL storage area
  [...]
  W0212 16:30:34.674648 11285 main.cpp:530] Orthanc has started


.. highlight:: json

Instead of specifying explicit authentication parameters, you can also
use the `PostgreSQL connection URIs syntax
<https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING>`__. For
instance::

  {
    "Name" : "MyOrthanc",
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "ConnectionUri" : "postgresql://username:password@localhost:5432/database?sslmode=prefer"
    },
    "Plugins" : [
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLIndex.so",
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLStorage.so"
    ]
  }


**Remark:** The Debian Med project maintains `another useful set of
instructions
<https://salsa.debian.org/med-team/orthanc-postgresql/-/blob/master/debian/README.Debian>`__.


Advanced options
----------------

Several advanced options are available as well to fine-tune the
configuration of the PostgreSQL plugins. They are documented below.


.. _postgresql-multiple-writers:

Multiple writers or connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting with Orthanc 1.9.2 and PostgreSQL 4.0, it is possible to use
:ref:`multiple writers or connections in large-scale deployments
<multiple-writers>`. Here is the list of configuration that control
this behavior:

* ``Lock`` must be set to ``false`` (cf. :ref:`below <postgresql-lock>`)

* ``MaximumConnectionRetries`` governs how many times Orthanc tries to
  connect to the database, as well as how many times Orthanc replays
  transactions to deal with collisions between multiple writers in 
  ``Serializable`` transaction mode or with any transient transaction errors
  in all transaction modes.

* ``IndexConnectionsCount`` controls the number of connections from
  the index plugin to the PostgreSQL database. Starting from v7.0, it is set to ``50`` by
  default.

* ``ConnectionRetryInterval`` is only used when opening one database
  connection to PostgreSQL.

* ``TransactionMode`` has been added in the release 6.0.  2 values are
  allowed: ``Serializable`` (that was the default value up to version 6.2)
  and ``ReadCommitted`` that is available only from release 6.0 and is the default
  value starting from version 7.0.  See below.

* The PostgreSQL plugin supports the :ref:`revision mechanism
  <revisions>` to protect metadata and attachments from concurrent
  modifications.


.. _postgresql-lock:

Locking
^^^^^^^

.. highlight:: json

By default, the plugins lock the database (using `PostgreSQL advisory
locks
<https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS>`__)
to prevent other instances of Orthanc from using the same PostgreSQL
database. If you want several instances of Orthanc to share the same
database or if you need multiple connections to the PostgreSQL
database, set the ``Lock`` option to ``false`` in the configuration
file::

  {
    "Name" : "MyOrthanc",
    "PostgreSQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "Lock" : false,
      "ConnectionUri" : "postgresql://username:password@localhost:5432/database"
    },
    "Plugins" : [
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLIndex.so",
      "/home/user/orthanc-databases/BuildPostgreSQL/libOrthancPostgreSQLStorage.so"
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
<https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=15>`__ such as::

  E0220 03:20:51.562601 PluginsManager.cpp:163] Exception in database back-end: Error in PostgreSQL: server closed the connection unexpectedly.
  This probably means the server terminated abnormally before or while processing the request.
  E0220 06:51:03.924868 PluginsManager.cpp:163] Exception in database back-end: Error in PostgreSQL: no connection to the server

This is due to a timeout in the PostgreSQL server. Please make sure to
`enable keep-alive
<https://dba.stackexchange.com/questions/97534/is-there-a-timeout-option-for-remote-access-to-postgresql-database>`__
in the configuration of your PostgreSQL server


Transaction modes (new in version 6.0)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: json

Starting from the release 6.0 of the plugin and Orthanc 1.12.3, orthanc supports 2 transaction modes that 
can be configured in the ``TransactionMode`` configuration of the ``PostgreSQL`` plugin:

- ``Serializable`` in which all write transactions are serialized which might lead
  to performance bottlenecks when lots of threads or Orthanc instances are trying
  to write to the same Database.  This was the default setting up to release 6.2.
- ``ReadCommitted`` that allows multiple threads or Orthanc instances to write at the
  same time to the same Database.  This is the default setting starting from release 7.0.

Optimizations
^^^^^^^^^^^^^

* ``AllowInconsistentChildCounts`` has been added in the release 7.2 to provide
  some optimization when accessing e.g tags like ``NumberOfStudyRelatedInstances``.
  If set to ``true``, childCount values of recently ingested resources will be 
  incorrect until the next execution of the DB housekeeping thread.


Other options
^^^^^^^^^^^^^

* ``EnableVerboseLogs`` has been added in the release 6.0 to log the 
  SQL queries that are being executed.  This is mainly target at developers.

* ``HousekeepingInterval`` has been added in the release 7.0 to define the
  interval (in seconds) at which the DB housekeeping thread is executed.  The
  DB housekeeping thread is in charge of updating values like the statistics
  and childCount entries to speed up their computation. 


Scalability
^^^^^^^^^^^

When configuring your PostgreSQL plugin, ensure you've read the :ref:`scalability section 
<scalability>`


Upgrades/Downgrades
^^^^^^^^^^^^^^^^^^^

New vesions of the PostgreSQL might modify the DB schema by adding new columns/tables/triggers.

+---------------------------+-------------------------------------------+
| Plugin version            | Schema revision                           |
+===========================+===========================================+
| before 5.1                | no revision                               |
+---------------------------+-------------------------------------------+
| 5.1                       | 1                                         |
+---------------------------+-------------------------------------------+
| 6.0 - 6.2                 | 2                                         |
+---------------------------+-------------------------------------------+
| 7.0 - 7.1                 | 3                                         |
+---------------------------+-------------------------------------------+
| 7.2                       | 4                                         |
+---------------------------+-------------------------------------------+
| from 8.0                  | 5                                         |
+---------------------------+-------------------------------------------+


Upgrades from one revision to the other is always automatic.  Furthermore, if you are upgrading
from e.g plugin 3.3 to 8.0, Orthanc will apply all migration steps autonomously.

However, if, for some reasons, you would like to reinstall a previous plugin version, the
older plugin might refuse to start because the revision is newer and unknown to it.

To downgrade from revision 5 to revision 4, one might run this procedure::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Downgrades/Rev5ToRev4.sql
  $ psql -U postgres -f Rev5ToRev4.sql

To downgrade from revision 4 to revision 3, one might run this procedure::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Downgrades/Rev4ToRev3.sql
  $ psql -U postgres -f Rev4ToRev3.sql

To downgrade from revision 3 to revision 2, one might run this procedure::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Downgrades/Rev3ToRev2.sql
  $ psql -U postgres -f Rev3ToRev2.sql

To downgrade from revision 2 to revision 1, one might run this procedure::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Downgrades/Rev2ToRev1.sql
  $ psql -U postgres -f Rev2ToRev1.sql


Note for large databases and multiple Orthanc instances:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

When upgrading from one revision to another, the upgrade might take quite some time.  E.g, we have observed the upgrade
taking 17 minutes on a DB with 300.000 studies and 150 millions instances when upgrading from revision 1 to 2 and multiple minutes
when upgrading from revision 2 to 3.  Orthanc will not respond during the upgrade.  Therefore,
if you have enabled autohealing (automatic restart in case Orthanc is not responsive), you should likely disable it
during the first start with the PostgreSQL plugin v6.0 or v7.0 which will apply these migrations.

Also note that, if you have multiple containers connected to the same DB, all containers will try to acquire an exclusive lock
to perform the upgrade of the DB.  Only one of them will actually perform the upgrade.  Also note that you should not perform a
rolling updates of the Orthanc containers when performing a DB upgrade.  All Orthanc containers should use the same version of the
plugin, the one that is compatible with the current revision.

Therefore, in complex setups, it might be simpler/safer to simply shut-down the Orthanc containers, perform the upgrade
manually and then, restart the Orthanc containers with the newest version of the plugin.

To upgrade manually from revision 1 to revision 2, one might run this procedure on the existing DB (note: make
sur to select the correct DB and schema (Orthanc is using the default ``public`` shema))::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Upgrades/Rev1ToRev2.sql
  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/PrepareIndex.sql
  $ psql -U postgres -f Rev1ToRev2.sql
  $ psql -U postgres -f PrepareIndex.sql

To upgrade manually from revision 2 to revision 3::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Upgrades/Rev2ToRev3.sql
  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/PrepareIndex.sql
  $ psql -U postgres -f Rev2ToRev3.sql
  $ psql -U postgres -f PrepareIndex.sql

To upgrade manually from revision 3 to revision 4::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Upgrades/Rev3ToRev4.sql
  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/PrepareIndex.sql
  $ psql -U postgres -f Rev3ToRev4.sql
  $ psql -U postgres -f PrepareIndex.sql

To upgrade manually from revision 4 to revision 5::

  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/Upgrades/Rev4ToRev5.sql
  $ wget https://orthanc.uclouvain.be/hg/orthanc-databases/raw-file/default/PostgreSQL/Plugins/SQL/PrepareIndex.sql
  $ psql -U postgres -f Rev4ToRev5.sql
  $ psql -U postgres -f PrepareIndex.sql

These procedures are identical to the one performed automatically by Orthanc when it detects that an upgraded is required.


Troubleshooting
---------------

SCRAM authentication
^^^^^^^^^^^^^^^^^^^^

.. note:: This section only applies to releases <= 3.2 of the
          PostgreSQL plugins. Starting with release 3.3, the plugins
          use a version of libpq that should support SCRAM
          authentication.

In the releases 3.2 of the PostgreSQL plugins, the precompiled
binaries use an old, but stable version of the PostgreSQL client
(libpq 9.6.1). This makes these binaries very portable, however they
might not be compatible with more recent features of PostgreSQL.

In particular, the precompiled binaries are not compatible with `SCRAM
authentication
<https://en.wikipedia.org/wiki/Salted_Challenge_Response_Authentication_Mechanism>`__
that is available since PostgreSQL 10. If you get the error ``psql:
authentication method 10 not supported``, this indicates that the
PostgreSQL plugins cannot connect to a PostgreSQL server because SCRAM
is enabled.

`Ian Smith
<https://groups.google.com/g/orthanc-users/c/4EH7HpcEnSA/m/a4x6oiucAgAJ>`__
has reported the following method to disable SCRAM:

1. Drop/delete the ``orthanc`` database and user in PostgreSQL.
2. Edit the files ``postgresql.conf`` and ``pg_hba.conf`` and change
   ``scram-sha-256`` to ``md5`` in all cases.
3. Add the ``orthanc`` user and database in PostgreSQL again.
4. Restart Orthanc.


Compilation
-----------

Static linking
^^^^^^^^^^^^^^

.. highlight:: text

The procedure to compile these plugins is similar to that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir BuildPostgreSQL
  $ cd BuildPostgreSQL
  $ cmake ../PostgreSQL -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce 2 shared libraries, each containing one plugin for Orthanc:

* ``OrthancPostgreSQLIndex`` replaces the default SQLite index of Orthanc by PostgreSQL. 
* ``OrthancPostgreSQLStorage`` makes Orthanc store the DICOM files it receives into PostgreSQL. 

  
.. _postgresql-ubuntu1604:

Dynamic linking on Ubuntu 16.04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

If static linking is not desired, here are build instructions for
Ubuntu 16.04 (provided build dependencies for the :ref:`core of
Orthanc <compiling>` have already been installed)::

  $ sudo apt-get install libpq-dev postgresql-server-dev-all
  $ mkdir BuildPostgreSQL
  $ cd BuildPostgreSQL
  $ cmake ../PostgreSQL -DCMAKE_BUILD_TYPE=Release \
                        -DALLOW_DOWNLOADS=ON \
                        -DUSE_SYSTEM_GOOGLE_TEST=OFF \
                        -DUSE_SYSTEM_ORTHANC_SDK=OFF
  $ make


.. _postgresql-cmake:
  
Dynamic linking on other GNU/Linux distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

The build instructions should always be very similar to those for
:ref:`Ubuntu 16.04 <postgresql-ubuntu1604>`. One difficulty that could
however arise is that it is possible that the CMake environment that
is shipped with the GNU/Linux distribution cannot locate a recent
version of the development headers for PostgreSQL. This leads to an
error while invoking CMake that looks like::

  -- Could NOT find PostgreSQL (missing: PostgreSQL_TYPE_INCLUDE_DIR)

In such a situation, please add your version of PostgreSQL to the
macro ``PostgreSQL_ADDITIONAL_VERSIONS`` that is defined at the end of
the `Resources/CMake/PostgreSQLConfiguration.cmake file
<https://orthanc.uclouvain.be/hg/orthanc-databases/file/default/Resources/CMake/PostgreSQLConfiguration.cmake>`__
in the sources of the project.
