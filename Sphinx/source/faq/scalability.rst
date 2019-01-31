.. _scalability:

Scalability of Orthanc
======================

One of the most common question about Orthanc is: *"How many DICOM
instances can be stored by Orthanc?"* 

The source code of Orthanc imposes no such hard limit by itself. The
stress is actually put on the underlying database engine, and on the
storage area (check out :ref:`orthanc-storage`). As explained in the
:ref:`troubleshooting section <troubleshooting>`, the built-in SQLite
database engine should be replaced by an enterprise-ready database
engine as soon as the number of DICOM instances grow above about
50,000 (check out the :ref:`postgresql` and :ref:`mysql`). It is also
true that the performance of Orthanc in the presence of large
databases has continuously improved over time, especially when it comes
to the speed of :ref:`DICOM C-FIND <dicom-find>`.

Here is a generic setup that should provide best performance in the
presence of large databases:

* Make sure that :ref:`run-time debug assertions <troubleshooting>`
  are turned off. A warning will show in the logs if this is not the
  case.

* Make sure to use the latest release of Orthanc (1.5.3 at the time of
  writing).

* We suggest to use the latest release of the :ref:`PostgreSQL plugin
  <postgresql>` to store the database index (3.0 at the time of
  writing). Make sure that ``EnableIndex`` is set to ``true``.

* We suggest to use the default filesystem storage area. Of course,
  make sure that the filesystem is properly backup, and that
  technologies such as RAID are enabled. Make sure that the option
  ``EnableStorage`` of the PostgreSQL plugins is set to ``false``.

* Obviously, the PostgreSQL database should be stored on a high-speed
  drive (SSD). This is less important for the storage area.

* The :ref:`Orthanc configuration file <configuration>` should have
  the following values for performance-related options (but make sure
  to understand their implication):
  
  * ``StorageCompression = false``
  * ``LimitFindResults = 100``
  * ``LimitFindInstances = 100``
  * ``KeepAlive = true``
  * ``TcpNoDelay = true``
  * ``SaveJobs = false``
  * ``StorageAccessOnFind = Never``

* Make sure to carefully :ref:`read the logs <log>` in ``--verbose``
  mode, especially at the startup of Orthanc. The logs may contain
  very important information regarding performance.

* Make sure to read guides about the :ref:`tuning of PostgreSQL
  <https://wiki.postgresql.org/wiki/Performance_Optimization>`__.

