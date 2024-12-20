.. _troubleshooting:

Troubleshooting
===============

As a general rule, when you encounter an issue, always make sure that
you use the `most recent version
<https://www.orthanc-server.com/download.php>`__ of Orthanc.

Also make a search on the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__, and make a
search in the present Orthanc Book (there is a search field at the top
of this page). Your issue might indeed have already been discussed in
the past or in the FAQ.

Startup
-------

* If **Orthanc fails to start** with the error "**The TCP port of the DICOM 
  server is privileged or already in use**", this means another software is
  already using the port Orthanc is trying to use.  Usually, this means
  that an other instance of Orthanc is running.  However, note that, by default, 
  Orthanc uses port 4242 which might also be used by other software like
  a `Juniper VPN client <https://www.file.net/process/dsncservice.exe.html>`__.
  To determine which other process is using the port: 

  On Windows, you may use the `Resource Monitor <https://en.wikipedia.org/wiki/Resource_Monitor>`__.
  In the `Network` tab, check the `Listening Ports`.  

  On Linux, you may use this command line: ``sudo ss --tcp --listen --numeric --processes``.

  Starting with version 1.3.0, the check at Orthanc startup is more robust
  (it also checks for UDP socket using the same port) and Orthanc 1.3.0 might 
  display error messages that where not displayed by previous versions.

* If Orthanc **does not start anymore after a hard shutdown** and if
  you use the :ref:`Orthanc Web viewer plugin <webviewer>`, this might
  reflect a corruption in the cache of the Web viewer. In such a case,
  it is safe to remove the folder that contains the cache. By default,
  this folder is called ``OrthancStorage/WebViewerCache/``
  (cf. :ref:`configuration option <configuration>` ``CachePath`` in
  the ``WebViewer`` section). Of course, don't remove the folder
  ``OrthancStorage/``, as it contains the DICOM files.
  
  
DICOM networking
----------------

* The troubleshooting of DICOM network protocol is covered in a
  :ref:`separate FAQ entry <dicom>`.


Validating DICOM files
----------------------

* Invalid DICOM files are often encountered in practice. Such files
  can cause failures in Orthanc, or can prevent DICOM network
  transfers. You can validate DICOM files by using the ``dciodvfy``
  command-line tool (cf. `its documentation
  <http://dclunie.com/dicom3tools/dciodvfy.html>`__) from the
  `dicom3tools <https://www.dclunie.com/dicom3tools.html>`__ project
  by David Clunie.

  The core team of Orthanc will **only provide support for DICOM files
  that are reported as valid** by ``dciodvfy``.

* Side-note: The default transfer syntax of DICOM is Little Endian
  Implicit (``1.2.840.10008.1.2``). For DICOM files that include
  private tags, **we recommend using Little Endian Explicit**
  (``1.2.840.10008.1.2.1``) instead Little Endian Implicit whenever
  possible. Instead, in Little Endian Explicit, each DICOM tag has an
  explicit declaration of its value representation (type), which
  contrasts with Little Endian Implicit that necessitates to configure
  the dictionary of private tags to be properly handled in some
  operations (cf. the ``Dictionary`` :ref:`configuration option
  <configuration>`).
  
  
Orthanc Explorer
----------------

* **I cannot login to Orthanc Explorer**: For security reasons, access
  to Orthanc from remote hosts is disabled by default. Only the
  localhost is allowed to access Orthanc. You have to set the
  ``RemoteAccessAllowed`` option in the :ref:`configuration file
  <configuration>` to ``true``. It is then strongly advised to set
  ``AuthenticationEnabled`` to ``true`` and to add a user to the
  ``RegisteredUsers`` option, also in the configuration file.


Performance issues
------------------

* **Run-time debug assertions**: If performance is important to you,
  make sure to add the option ``-DCMAKE_BUILD_TYPE=Release`` when
  invoking ``cmake`` while :ref:`compiling Orthanc
  <compiling>`. Indeed, by default, `run-time debug assertions
  <https://en.wikipedia.org/wiki/Assertion_(software_development)#Assertions_for_run-time_checking>`_
  are enabled, which can seriously impact performance, especially if
  your Orthanc server stores a lot of DICOM instances.

  Note that the `official Docker images
  <https://github.com/jodogne/OrthancDocker>`__ of Orthanc <= 1.0.0
  were not compiled in ``Release`` mode. As a consequence, to improve
  performance, make sure to use either the mainline version of the
  container (run ``docker pull jodogne/orthanc`` to ensure you use the
  most recent version of the mainline), or versions more recent than
  ``jodogne/orthanc:1.1.0``.

* **Orthanc slows down if storing many files**: The default database
  engine that is built in Orthanc is `SQLite
  <https://www.sqlite.org/index.html>`__. As SQLite is above all a
  lightweight database engine, it is not designed to `store very large
  datasets <https://www.sqlite.org/whentouse.html>`__. If you are sure
  that you have properly disabled run-time debug assertions
  (cf. above), but still experience degradation in performance over
  time, you should seriously consider switching to a more scalable
  database engine. To this end, you can notably check out the
  :ref:`official PostgreSQL plugin <postgresql>`.

  As a rule of thumb, the performance of the default SQLite engine
  built in Orthanc should run fine up to about 50,000 DICOM instances.
  However, we have seen Orthanc running fairly well with more than 2
  millions of instances. This limit really depends upon your
  application, and upon the patterns of access to the database.

  Also check out the section about the :ref:`scalability`.


* **Orthanc Explorer is slow under Windows on the localhost**:

  - Favor ``127.0.0.1`` instead of ``localhost`` when specifying the
    network address of a server. Users have reported that this minor
    change `can massively improve performance
    <https://groups.google.com/d/msg/orthanc-users/tTe28zR0nGk/Lvs0STJLAgAJ>`__
    on Windows. Starting with Orthanc 1.0.1, the samples from the
    source distribution have been adapted in this way.

  - As an alternative, you can disable IPv6 support. This is a
    Windows-specific problem that is discussed `here
    <https://superuser.com/questions/43823/google-chrome-is-slow-to-localhost>`__
    and `here
    <https://stackoverflow.com/questions/1726585/firefox-and-chrome-slow-on-localhost-known-fix-doesnt-work-on-windows-7>`__.

* If you experience **slow DICOM transfers under GNU/Linux**, please
  read the `following bug report
  <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=785400>`__. This
  issue does *not* affect all the versions of GNU/Linux. A patch to
  this issue is shipped with the Orthanc source code. In order to take
  advantage of this patch, you need to statically link Orthanc against
  DCMTK by using the ``-DUSE_SYSTEM_DCMTK=OFF`` flag `when invoking
  CMake
  <https://orthanc.uclouvain.be/hg/orthanc/file/default/LinuxCompilation.txt>`__.

  
Checking integrity of the storage area
--------------------------------------

.. highlight:: bash

Orthanc stores, in its database, an `MD5 hash
<https://en.wikipedia.org/wiki/MD5>`_ of the files stored in its
:ref:`storage area <orthanc-storage>` (which notably includes the
DICOM files), provided that the ``StoreMD5ForAttachments``
configuration option is set to ``true``.

This MD5 corresponds to the hash of the files in memory, before they
are written to the disk by Orthanc. This information is safely stored
inside the database for any incoming file attachment.

It is possible to ask Orthanc to check by itself whether some attachment
file was corrupted (i.e. to check whether the MD5 hash stored in the
database corresponds to the hash of the file on the disk)::

  $ curl -X POST http://localhost:8042/instances/f257b066-f3992cc4-ca6a5e5f-3f8dcf3a-d4958939/attachments/dicom/verify-md5 -d ''

This MD5 may be different if errors occurred while the DICOM file was
initially written to the storage, or if the file contents were
tampered with afterwards.

You can retrieve the stored MD5 hash of a DICOM instance as follows::

  $ curl http://localhost:8042/instances/f257b066-f3992cc4-ca6a5e5f-3f8dcf3a-d4958939/attachments/dicom/md5

Windows-specific issues
-----------------------

* Under Windows, Orthanc creates the "OrthancStorage" folder, and
  crashes with the error "**SQLite: Unable to open the database**":
  Your directory name is either too long, or it contains special
  characters. Please try and run Orthanc in a folder with a simple
  name such as ``C:\Orthanc``.

* If you run Orthanc as a Windows service, and if you want to store
  the Orthanc database (or the :ref:`Orthanc Web Viewer plugin
  <webviewer>`) onto a shared network drive, you might encounter an
  error ``boost::filesystem::status: The specified server cannot
  perform the requested operation``. This probably means that the
  ``SYSTEM`` account is not allowed to access the **mapped network
  drive**. The easiest approach to this end consists in configuring
  the Windows service to **run as user** (instead of the default
  ``SYSTEM`` account), `as explained in this thread
  <https://groups.google.com/g/orthanc-users/c/axrJfgA-Enk/m/Zeg3iUPOAwAJ>`__
  on the Orthanc Users forum (cf. `additional reference
  <https://docs.microfocus.com/SM/9.61/Hybrid/Content/serversetup/tasks/configure_the_service_manager_service_to_run_as_a_windows_user.htm>`__
  elsewhere on Internet).

* If **Orthanc crashes when handling one large DICOM file**, this most
  probably indicates a memory allocation error. Indeed, some
  precompiled `official Windows binaries
  <https://orthanc.uclouvain.be/downloads/windows-32/orthanc/index.html>`__
  are compiled using a 32bit compiler. As a consequence, Orthanc only
  has access to less than 4GB of RAM. If this is an important
  limitation for you, precompiled command-line versions of Orthanc for
  Windows 64bit are `also available
  <https://orthanc.uclouvain.be/downloads/windows-64/orthanc/index.html>`__.

* Avoid installing Orthanc, its database or its storage area in
  folders whose names contain **spaces or special characters**.

* If you run Orthanc as a Windows service, with the Python plugin
  enabled, you might have to change your ``PATH`` environment variable
  for Orthanc to **find the Python DLL**. The easiest approach to this
  end consists in configuring the Windows service to **run as user**
  (instead of the default ``SYSTEM`` account), `as explained in this
  thread
  <https://groups.google.com/g/orthanc-users/c/axrJfgA-Enk/m/Zeg3iUPOAwAJ>`__
  on the Orthanc Users forum (cf. `additional reference
  <https://docs.microfocus.com/SM/9.61/Hybrid/Content/serversetup/tasks/configure_the_service_manager_service_to_run_as_a_windows_user.htm>`__
  elsewhere on Internet).
