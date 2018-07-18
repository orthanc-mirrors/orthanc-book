.. _mysql:


MySQL/MariaDB plugins
=====================

.. contents::

The Orthanc project provides two **official** plugins to replace the
default storage area (on the filesystem) and the default SQLite index
by a MySQL or a MariaDB database.

For general information, check out the `official homepage of the
plugins <http://www.orthanc-server.com/static.php?page=mysql>`__.



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

Pre-compiled binaries for Microsoft Windows `are also available
<http://www.orthanc-server.com/browse.php?path=/plugin-mysql>`__.


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
      "Lock" : true            // See section about Locking
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


Locking
^^^^^^^

.. highlight:: json

By default, the plugins lock the database (using `MySQL/MariaDB
"GET_LOCK()"
<https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_get-lock>`__)
to prevent other instances of Orthanc from using the same database. If
you want several instances of Orthanc to share the same database, set
the ``Lock`` option to ``false`` in the configuration file.

Obviously, one must be very cautious when sharing the same database
between instances of Orthanc. In particular, all these instances
should share the same configuration.
