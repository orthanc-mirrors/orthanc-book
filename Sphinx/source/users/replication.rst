.. highlight:: bash
.. _replication:

Replication and upgrade
=======================

This page explains how to replicate the content of one instance of
Orthanc to another instance of Orthanc. This is useful to **upgrade**
between :ref:`versions of the database schema <db-versioning>`, or to
create **mirrored DICOM servers**.


Upgrade the database schema
---------------------------

As explained :ref:`elsewhere in the Orthanc Book <db-versioning>`,
successive versions of Orthanc might use a different version of the
database schema. If this happens, Orthanc will refuse to start (with
an explicit message in its :ref:`logs <log>`), to let the user decides
whether she actually wants to upgrade the database.

At this point, the user could indeed choose to modify its
:ref:`configuration file <configuration>` in order to create a new
database elsewhere on the filesystem (if using the default SQLite
backend), or on the database management system (e.g. if using
:ref:`PostgreSQL <postgresql>` or :ref:`MySQL/MariaDB <mysql>`). This
is important to let the user experiment a new version of Orthanc,
while keeping the older version up and running.

If you decide to upgrade the database schema, you have to apply the
following 3 steps:

1. If not done yet, stop the running Orthanc service:

   * Under Microsoft Windows, use the `services control panel
     <https://en.wikipedia.org/wiki/Windows_service>`__.
   * Under Debian, use ``sudo /etc/init.d/orthanc stop``.

2. Manually call Orthanc with the ``--upgrade`` command-line option, 
   and point to your configuration file:

   * Under Microsoft Windows, ``Orthanc.exe c:/Orthanc/ --upgrade``.
   * Under Debian, use ``sudo /usr/sbin/Orthanc /etc/orthanc/ --upgrade``.

3. Once the upgrade process is over, restart the Orthanc service:

   * Under Microsoft Windows, use the `services control panel
     <https://en.wikipedia.org/wiki/Windows_service>`__.
   * Under Debian, use ``sudo /etc/init.d/orthanc start``.

**Important remarks:**

* Orthanc is now considered as **stable**, which means that no upgrade
  in the database schema should occur in the near future.
* Depending on the size of the Orthanc database, upgrading the
  database schema might take time, as this operation implies
  re-reading all the DICOM instances from the disk.
* In the case of the official Debian and Fedora packages, the default
  location of the database changes with the version of its schema.
  For instance, DB schema version 6 will be stored in
  ``/var/lib/orthanc/db-v6/``. If upgrading the package (and if the
  configuration files are purged), a new database will automatically
  be created on the disk. Old data can be recovered either by changing
  the configuration in ``/etc/orthanc/`` to point to the previous
  location of the database then using ``--upgrade`` as written above,
  or by using the instructions for replication below.


Direct access to the filesystem
-------------------------------

The most direct way to replicate an instance of Orthanc consists in
using the `ImportDicomFiles
<https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Resources/Samples/ImportDicomFiles/ImportDicomFiles.py>`_
script of the Orthanc distribution. This process can also be used to
restore the content of an Orthanc server after a corruption of its
database.

For instance, the following command would recursively explore the
content of the ``OrthancStorage`` folder (where Orthanc stores its
DICOM files by default), and send each DICOM file inside this folder
to the instance of Orthanc whose REST API is listening on
``http://192.168.0.2:8042``::

    $ python ImportDicomFiles.py 192.168.0.2 8042 OrthancStorage

This method will only succeed if:

* The source Orthanc uses the default storage area on the filesystem
  (i.e. the source Orthanc does *not* store its DICOM files using one
  of the "storage area plugins", such as for `PostgreSQL
  <https://www.orthanc-server.com/static.php?page=postgresql>`_ or
  `MySQL/MariaDB
  <https://www.orthanc-server.com/static.php?page=mysql>`_ - but it's
  OK for the source of Orthanc to use any of the "index plugins"),
* You have command-line access to the source Orthanc, and
* The transparent :ref:`compression` of the DICOM instances is
  disabled (cf. option ``StorageCompression`` in the
  :ref:`configuration file <configuration>`).

**Important remark:** Because of :ref:`the way Orthanc stores its
database <orthanc-storage>` on the filesystem, it is *entirely normal*
if the ``ImportDicomFiles.py`` script ends by saying that only half of
the DICOM files were properly sent. This is because the JSON summaries
are not DICOM files, and are thus rejected by the target Orthanc
server. More information are available `on the discussion group
<https://groups.google.com/d/msg/orthanc-users/Zlhtcpo76qQ/tp8EqaRCAQAJ>`__.


Generic replication
-------------------

If you cannot use the first method, you can use the `Replicate
<https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Resources/Samples/Python/Replicate.py>`_
script of the Orthanc distribution. This script will use the REST API
of both the source and target instances of Orthanc. For instance::

    $ python Replicate.py http://orthanc:password@localhost:8042/ http://192.168.0.2/

Obviously, contrarily to the first method, the source instance of
Orthanc must be up and running during the replication.
