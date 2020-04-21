.. _scalability:

Scalability of Orthanc
======================

.. contents::
  
Overview
--------

One of the most common question about Orthanc is: *"How many DICOM
instances can be stored by Orthanc?"* 

The source code of Orthanc imposes no such hard limit by itself.

At the time of writing, we know that Orthanc is being used in
production in hospitals with more than 15TB of data, 125,000 studies
and around 50 millions of instances (please `get in touch with us
<https://www.orthanc-server.com/static.php?page=contact>`__ if you can
share other testimonials). Other users have even reported more than
28TB of data. Here are links to some testimonials that were published
on the `Orthanc Users
<https://groups.google.com/forum/#!forum/orthanc-users>`__ discussion
group: `1
<https://groups.google.com/d/msg/orthanc-users/-L0D1c2y6rw/KmWnwEijAgAJ>`__,
`2
<https://groups.google.com/d/msg/orthanc-users/-L0D1c2y6rw/nLXxtYzuCQAJ>`__,
`3
<https://groups.google.com/d/msg/orthanc-users/s5-XlgA2BEY/ZpYagqBwAAAJ>`__,
`4
<https://groups.google.com/d/msg/orthanc-users/A4hPaJo439s/NwR6zk9FCgAJ>`__,
`5
<https://groups.google.com/d/msg/orthanc-users/Z5cLwbVgJc0/SxVzxF7ABgAJ>`__,
`6
<https://groups.google.com/d/msg/orthanc-users/6tGNOqlUk-Q/vppkAYnFAQAJ>`__...

The stress is actually put on the underlying database engine, and on
the storage area (check out :ref:`orthanc-storage`). As explained in
the :ref:`troubleshooting section <troubleshooting>`, the built-in
SQLite database engine should be replaced by an enterprise-ready
database engine once Orthanc must store several hundreds of thousands
of DICOM instances (check out the :ref:`postgresql` and
:ref:`mysql`). It is also true that the performance of Orthanc in the
presence of large databases has continuously improved over time,
especially when it comes to the speed of :ref:`DICOM C-FIND
<dicom-find>`.


.. _scalability-setup:

Recommended setup for best performance
--------------------------------------

Here is a generic setup that should provide best performance in the
presence of large databases:

* Make sure to use the latest release of Orthanc (1.6.1 at the time of
  writing).

* We suggest to use the latest release of the :ref:`PostgreSQL plugin
  <postgresql>` to store the database index (3.2 at the time of
  writing). Make sure that ``EnableIndex`` is set to ``true``.

* Make sure that :ref:`run-time debug assertions <troubleshooting>`
  are turned off. A warning will show in the logs if this is not the
  case. Note that all pre-built binaries provided by Osimis are
  correctly configured in that respect.

* We suggest to use the default filesystem storage area. Of course,
  make sure that the filesystem is properly backed up, and that
  technologies such as RAID are enabled. Make sure that the option
  ``EnableStorage`` of the PostgreSQL plugins is set to ``false``.

* Obviously, the PostgreSQL database should be stored on a high-speed
  drive (SSD). This is less important for the storage area.

* It may be useful to store the PostgreSQL database on another drive
  than the storage area. This should improve the use of the available
  bandwidth to the disks.

* The :ref:`Orthanc configuration file <configuration>` should have
  the following values for performance-related options (but make sure
  to understand their implications):
  
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

* Make sure to read guides about the `tuning of PostgreSQL
  <https://wiki.postgresql.org/wiki/Performance_Optimization>`__.

* You might also be interested in checking the options related to
  :ref:`security <security>`.

* Consider using filesystems that are known to achieve high
  performance, such as `XFS <https://en.wikipedia.org/wiki/XFS>`__ or
  `Btrfs <https://en.wikipedia.org/wiki/Btrfs>`__ on GNU/Linux
  distributions.

* On GNU/Linux distributions, `LVM (Logical Volume Manager)
  <https://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)>`__
  can be used to dynamically and easily grow the storage area as more
  space becomes needed.

* If using the :ref:`DICOMweb server plugin <dicomweb-server-config>`,
  consider setting configuration option ``StudiesMetadata`` to
  ``MainDicomTags``.


.. _scalability-memory:

Controlling memory usage
------------------------

The absence of memory leaks in Orthanc is verified thanks to `valgrind
<https://valgrind.org/>`__.

On GNU/Linux systems, you might however `observe a large memory
consumption
<https://groups.google.com/d/msg/orthanc-users/qWqxpvCPv8g/47wnYyhOCAAJ>`__
in the "resident set size" (VmRSS) of the application, notably if you
upload multiple large DICOM files using the REST API.

This large memory consumption comes from the fact that the embedded
HTTP server is heavily multi-threaded, and that many so-called `memory
arenas <https://sourceware.org/glibc/wiki/MallocInternals>`__ are
created by the glibc standard library (up to one per thread). As a
consequence, if each one of the 50 threads in the HTTP server of
Orthanc (default value of the ``HttpThreadsCount`` option) allocates
at some point, say, 50MB, the total memory usage reported as "VmRSS"
can grow up to 50 threads x 50MB = 2.5GB, even if the Orthanc threads
properly free all the buffers.

.. highlight:: bash
               
A possible solution to reducing this memory usage is to ask glibc to
limit the number of "memory arenas" that are used by the Orthanc
process. On GNU/Linux, this can be controlled by setting the
environment variable ``MALLOC_ARENA_MAX``. For instance, the following
bash command-line would use one single arena that is shared by all the
threads in Orthanc::

  $ MALLOC_ARENA_MAX=1 ./Orthanc

Obviously, this restrictive setting will use minimal memory, but will
result in contention among the threads. A good compromise might be to
use 5 arenas::

  $ MALLOC_ARENA_MAX=5 ./Orthanc

Memory allocation on GNU/Linux is a complex topic. There are other
options available as environment variables that could also reduce
memory consumption (for instance, ``MALLOC_MMAP_THRESHOLD_`` would
bypass arenas for large memory blocks such as DICOM files). Check out
the `manpage <http://man7.org/linux/man-pages/man3/mallopt.3.html>`__
of ``mallopt()`` for more information.
