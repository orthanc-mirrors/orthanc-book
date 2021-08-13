.. _mysql:


MySQL/MariaDB plugins
=====================

.. contents::

The Orthanc project provides two **official** plugins to replace the
default storage area (on the filesystem) and the default SQLite index
by a MySQL or a MariaDB database.

For general information, check out the `official homepage of the
plugins <https://www.orthanc-server.com/static.php?page=mysql>`__.

For information about scalability, make sure to read the section about
:ref:`multiple writers in large-scale deployments <multiple-writers>`.

The source code of the MySQL/MariaDB plugins can be found in the
``orthanc-databases`` `Mercurial repository
<https://hg.orthanc-server.com/orthanc-databases/>`__, next to the
source code of the :ref:`ODBC <odbc>` and :ref:`PostgreSQL
<postgresql>` plugins.

**Warning:** According to `this thread on our discussion group
<https://groups.google.com/d/msg/orthanc-users/yV3LSTh_TjI/Fb4ShaYMBAAJ>`__,
the MySQL/MariaDB plugins require MySQL 8.x if running on Microsoft
Windows.



Compilation
-----------

Static linking
^^^^^^^^^^^^^^

.. highlight:: text

The procedure to compile these plugins is similar to that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir BuildMySQL
  $ cd BuildMySQL
  $ cmake ../MySQL/ -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce 2 shared libraries, each containing one plugin for Orthanc:

* ``OrthancMySQLIndex`` replaces the default SQLite index of Orthanc by MySQL. 
* ``OrthancMySQLStorage`` makes Orthanc store the DICOM files it receives into MySQL. 

  
Microsoft Windows
^^^^^^^^^^^^^^^^^

Pre-compiled binaries for Microsoft Windows 32bit `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-mysql>`__.


Dynamic linking on Ubuntu 16.04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

If static linking is not desired, here are build instructions for
Ubuntu 16.04 (provided build dependencies for the :ref:`core of
Orthanc <compiling>` have already been installed)::

  $ sudo apt-get install libmysqlclient-dev
  $ mkdir BuildMySQL
  $ cd BuildMySQL
  $ cmake ../MySQL/ -DCMAKE_BUILD_TYPE=Release \
                    -DALLOW_DOWNLOADS=ON \
                    -DUSE_SYSTEM_GOOGLE_TEST=OFF \
                    -DUSE_SYSTEM_ORTHANC_SDK=OFF
  $ make

  
Usage
-----

You of course first have to :ref:`install Orthanc <binaries>`, with a
version above 0.9.5. You then have to **create a database** dedicated
to Orthanc on some MySQL/MariaDB server. Please refer to the `MySQL
documentation
<https://dev.mysql.com/doc/refman/8.0/en/database-use.html>`__.

.. highlight:: json

Once Orthanc is installed and the database is created, you must add a
section in the :ref:`configuration file <configuration>` that
specifies the address of the **MySQL/MariaDB server together with your
credentials**. You also have to tell Orthanc in which path it can find
the plugins: This is done by properly modifying the ``Plugins``
option. You could for instance adapt the following configuration
file::

  {
    "Name" : "MyOrthanc",
    "MySQL" : {
      "EnableIndex" : true,
      "EnableStorage" : true,
      "Host" : "localhost",    // For TCP connections (notably Windows)
      "Port" : 3306,           // For TCP connections (notably Windows)
      "UnixSocket" : "/var/run/mysqld/mysqld.sock",  // For UNIX on localhost
      "Database" : "orthanc",
      "Username" : "orthanc",
      "Password" : "orthanc",
      "EnableSsl" : false,     // force SSL connections
      "SslVerifyServerCertificates": true, // Verify server certificates if EnableSsl is true
      "SslCACertificates": "",             // Path to CA certificates to validate servers
      "Lock" : true,                       // See section about Locking
      "MaximumConnectionRetries" : 10,     // New in release 3.0
      "ConnectionRetryInterval" : 5,       // New in release 3.0
      "IndexConnectionsCount" : 1          // New in release 4.0
    },
    "Plugins" : [
      "/home/user/orthanc-databases/BuildMySQL/libOrthancMySQLIndex.so",
      "/home/user/orthanc-databases/BuildMySQL/libOrthancMySQLStorage.so"
    ]
  }

**Important 1:** The ``EnableIndex`` and ``EnableStorage`` options must
be explicitly set to ``true``, otherwise Orthanc will continue to use
its default SQLite back-end and the filesystem storage area.

**Important 2:** To force a TCP connection on the ``localhost`` in
UNIX (i.e. to instruct Orthanc not to use UNIX socket), the
``UnixSocket`` can be set to the empty string.

**Remark:** To force using a TLS connection, you must set ``EnableSsl``
to ``true``.  Once ``EnableSsl`` is ``true``, the ``SslVerifyServerCertificates``
enables the check of server certificates (``true`` by default).
The CA certificates used to verify the server certificate can be defined
through ``SslCACertificates``; if not defined or empty, the value of the global
Orthanc configuration ``HttpsCACertificates`` is used.  These options have been
introduced in the mainline in July 2020 and have not yet been released.

**Remark:** When using the ``Storage`` MySQL plugin, the DICOM files
are stored as blobs in the database. This might actually consume more
space than the DICOM file itself.

Note that a typical usage of the MySQL plugin is to enable only the
``Index``, using the default filesystem storage for DICOM files.



.. highlight:: text

Orthanc must of course be **restarted** after the modification of its
configuration file. The log will contain an output similar to::

  $ ./Orthanc Configuration.json
  W0710 14:25:35.143828 main.cpp:1298] Orthanc version: 1.3.2
  W0710 14:25:35.146528 OrthancInitialization.cpp:120] Reading the configuration from: "./Configuration.json"
  [...]
  W0710 14:25:35.173652 main.cpp:671] Loading plugin(s) from: /home/jodogne/Subversion/orthanc-databases/BuildMySQL/libOrthancMySQLIndex.so
  W0710 14:25:35.175927 PluginsManager.cpp:269] Registering plugin 'mysql-index' (version mainline)
  W0710 14:25:35.176213 PluginsManager.cpp:168] Performance warning: The database index plugin was compiled against an old version of the Orthanc SDK, consider upgrading
  W0710 14:25:35.176323 main.cpp:671] Loading plugin(s) from: /home/jodogne/Subversion/orthanc-databases/BuildMySQL/libOrthancMySQLStorage.so
  W0710 14:25:35.177172 PluginsManager.cpp:269] Registering plugin 'mysql-storage' (version mainline)
  W0710 14:25:35.180684 PluginsManager.cpp:168] Your MySQL server cannot store DICOM files larger than 16MB
  W0710 14:25:35.180714 PluginsManager.cpp:168]   => Consider increasing "max_allowed_packet" in "my.cnf" if this limit is insufficient for your use
  W0710 14:25:35.246150 main.cpp:1098] Using a custom database from plugins
  W0710 14:25:35.246210 main.cpp:1109] Using a custom storage area from plugins
  [...]
  W0710 14:25:37.073633 main.cpp:683] Orthanc has started



Advanced options
----------------

Several advanced options are available as well to fine-tune the
configuration of the MySQL plugins. They are documented below.


.. _mysql-multiple-writers:

Multiple writers or connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting with Orthanc 1.9.2 and MySQL 4.0, it is possible to use
:ref:`multiple writers or connections in large-scale deployments
<multiple-writers>`. Here is the list of configuration that control
this behavior:

* ``Lock`` must be set to ``false`` (cf. :ref:`below <mysql-lock>`)

* ``MaximumConnectionRetries`` governs how many times Orthanc tries to
  connect to the database, as well as how many times Orthanc replays
  transactions to deal with collisions between multiple writers.

* ``IndexConnectionsCount`` controls the number of connections from
  the index plugin to the MySQL database. It is set to ``1`` by
  default, which corresponds to the old behavior of Orthanc <= 1.9.1.

* ``ConnectionRetryInterval`` is only used when opening one database
  connection to MySQL.

* As of release 4.0, the MySQL plugin does **not** support yet the
  :ref:`revision mechanism <revisions>` to protect metadata and
  attachments from concurrent modifications.


Locking
^^^^^^^

.. highlight:: json

By default, the plugins lock the database (using `MySQL/MariaDB
"GET_LOCK()"
<https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html>`__)
to prevent other instances of Orthanc from using the same database. If
you want several instances of Orthanc to share the same database, set
the ``Lock`` option to ``false`` in the configuration file.

In the absence of locking, the same limitation apply to the
MySQL/MariaDB plugins than to the PostgreSQL plugins (i.e. at most one
instance of Orthanc writing to the database).  For more information,
please check out the :ref:`documentation for PostgreSQL
<postgresql-lock>`.

Scalability
^^^^^^^^^^^

When configuring your MySQL plugin, ensure you've read the
:ref:`scalability section <scalability>`


Backup
------

The MySQL plugin uses stored routines (i.e. functions/procedures) that
are not archived by default by the ``mysqldump`` tool. As a
consequence, make sure to add the ``--routines`` command-line flag to
also archive such routines in your backup.
