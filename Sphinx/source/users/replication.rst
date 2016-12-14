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
whether she actually wants to upgrade the database. At this point, the
user might indeed decide to modify its :ref:`configuration file
<configuration>` to create a new database elsewhere on the filesystem.

If you decide to upgrade the database schema, you have to apply the
following 3 steps:

1. If not done yet, stop the running Orthanc service:

   * Under Microsoft Windows, use the `services control panel
     <https://en.wikipedia.org/wiki/Windows_service>`__.
   * Under Debian, use ``sudo /etc/init.d/orthanc stop``.

2. Manually call Orthanc with the ``--upgrade`` command-line option, 
   and point to your default configuration file:

   * Under Microsoft Windows, ``Orthanc.exe c:/Orthanc/``.
   * Under Debian, use ``sudo /usr/sbin/Orthanc /etc/orthanc/ --upgrade``.

3. Start the Orthanc service again:

   * Under Microsoft Windows, use the `services control panel
     <https://en.wikipedia.org/wiki/Windows_service>`__.
   * Under Debian, use ``sudo /etc/init.d/orthanc stop``.

Note that, depending on the size of the Orthanc database, upgrading
the database schema might take time.


Direct access to the filesystem
-------------------------------

The most direct way to replicate consists in using the
`ImportDicomFiles
<https://bitbucket.org/sjodogne/orthanc/src/default/Resources/Samples/ImportDicomFiles/ImportDicomFiles.py>`_
script of the Orthanc distribution. For instance, the following
command would recursively explore the content of the ``OrthancStorage``
folder (where Orthanc stores its DICOM files by default), and send
each DICOM file inside this folder to the instance of Orthanc whose
REST API is listening on ``http://192.168.0.2:8042``::

    $ python ImportDicomFiles.py 192.168.0.2 8042 OrthancStorage

This method will only succeed if:

* The source Orthanc uses the default SQLite back-end of Orthanc (and
  not the `PostgreSQL plugin
  <http://www.orthanc-server.com/static.php?page=postgresql>`_, for
  instance),
* You have command-line access to the source Orthanc, and
* The transparent :ref:`compression` of the DICOM instances is
  disabled (cf. option ``StorageCompression`` in the
  :ref:`configuration file <configuration>`).

**Important remark:** Because of :ref:`the way Orthanc stores its
database <orthanc-storage>` on the filesystem, it is *entirely normal*
that the ``ImportDicomFiles.py`` script ends by saying that only half
of the DICOM files were properly sent. This is because the JSON
summaries are not DICOM files, and are thus rejected by the target
Orthanc server. More information are available `on the discussion
group
<https://groups.google.com/d/msg/orthanc-users/Zlhtcpo76qQ/tp8EqaRCAQAJ>`__.


Generic replication
-------------------

If you cannot use the first method, you can use the `Replicate
<https://bitbucket.org/sjodogne/orthanc/src/default/Resources/Samples/Python/Replicate.py>`_
script of the Orthanc distribution. This script will use the REST API
of both the source and target instances of Orthanc. For instance::

    $ python Replicate.py http://orthanc:password@localhost:8042/ http://192.168.0.2/

Obviously, contrarily to the first method, the source instance of
Orthanc must be up and running during the replication.
