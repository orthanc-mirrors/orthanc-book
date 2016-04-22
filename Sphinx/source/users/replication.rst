.. highlight:: bash
.. _replication:

Replication and upgrade
=======================

This page explains how to replicate the content of one instance of
Orthanc to another instance of Orthanc. This is useful to **upgrade**
between :ref:`versions of the database schema <db-versioning>`, or to
create **mirrored DICOM servers**.

Note that if you only want to automatically upgrade the database for
successive versions of Orthanc, you most probably only have to add the
``--upgrade`` command-line option while starting Orthanc.


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

Generic replication
-------------------

If you cannot use the first method, you can use the `Replicate
<https://bitbucket.org/sjodogne/orthanc/src/default/Resources/Samples/Python/Replicate.py>`_
script of the Orthanc distribution. This script will use the REST API
of both the source and target instances of Orthanc. For instance::

    $ python Replicate.py http://orthanc:password@localhost:8042/ http://192.168.0.2/

Obviously, contrarily to the first method, the source instance of
Orthanc must be up and running during the replication.
