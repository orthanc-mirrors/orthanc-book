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

* Make sure to use the latest release of Orthanc (1.10.1 at the time of
  writing) running on a GNU/Linux distribution.

* We suggest to use the latest release of the :ref:`PostgreSQL plugin
  <postgresql>` to store the database index (4.0 at the time of
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

* If your Orthanc instance is performing a lot of IO requests in parallel
  e.g because many clients are reading/writing DICOM files at the same
  time, you should consider using an :ref:`object storage <object-storage>` 
  plugin to store your files.

* The :ref:`Orthanc configuration file <configuration>` should have
  the following values for performance-related options (but make sure
  to understand their implications):
  
  * ``StorageCompression = false``
  * ``LimitFindResults = 100``
  * ``LimitFindInstances = 100``
  * ``KeepAlive = true``
  * ``TcpNoDelay = true``
  * ``StorageAccessOnFind = Never``
  * Consider adding ``SaveJobs = false``

* Since Orthanc 1.9.2 and PostgreSQL plugins 4.0: By default, the
  PostgreSQL index plugin uses 1 single connection to the PostgreSQL
  database. You can have multiple connections by setting the
  ``IndexConnectionsCount`` to a higher value (for instance ``5``) in
  the ``PostgreSQL`` section of the configuration file. This will
  improve concurrency. Check out :ref:`the explanation below <multiple-writers>`.

* Since Orthanc 1.9.2 and PostgreSQL plugins 4.0: If you have an
  hospital-wide VNA deployment, you could consider to deploy multiple
  Orthanc servers sharing the same PostgreSQL database. A typical
  scenario is having one "writer" Orthanc server that handles the
  ingesting of DICOM instances, and multiple "reader" Orthanc servers
  with features such as DICOMweb or viewers.

* From Orthanc 1.11.0 (not released yet): you have the ability to add
  more :ref:`main DICOM tags <main-dicom-tags>` in the Orthanc Index 
  to speed up C-Find, ``tools/find``, DICOMWeb QIDO-RS, WADO-RS and 
  especially WADO-RS Retrieve Metadata.

* Make sure to carefully :ref:`read the logs <log>` in ``--verbose``
  mode, especially at the startup of Orthanc. The logs may contain
  very important information regarding performance.

* Make sure to read guides about the `tuning of PostgreSQL
  <https://wiki.postgresql.org/wiki/Performance_Optimization>`__.

* Make sure to enable the `Autovacuum Daemon
  <https://www.postgresql.org/docs/current/routine-vacuuming.html>`__
  of PostgreSQL, or to periodically run the ``VACUUM`` SQL command on
  the PostgreSQL database in order to `reclaim the storage space
  <https://www.postgresql.org/docs/current/sql-vacuum.html>`__ that is
  occupied by rows that have been deleted from the database (e.g. in a
  cron job).

* You might also be interested in checking the options related to
  :ref:`security <security>`.

* Consider using filesystems that are known to achieve high
  performance, such as `XFS <https://en.wikipedia.org/wiki/XFS>`__ or
  `Btrfs <https://en.wikipedia.org/wiki/Btrfs>`__ on GNU/Linux
  distributions.

* If you need to grow the storage area as more space becomes needed,
  you can consider the following solutions:

  - Move the storage area to another disk partition, and update the
    ``StorageDirectory`` :ref:`configuration option <configuration>`
    accordingly.
  - :ref:`Replicate <replication>` your current instance of Orthanc
    onto another instance of Orthanc with a larger storage area.
  - On GNU/Linux distributions, check out `LVM (Logical Volume Manager)
    <https://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)>`__.
  - On Microsoft Windows, check out the so-called "`Storage Spaces
    <https://docs.microsoft.com/en-us/windows-server/storage/storage-spaces/overview>`__".
  - Another approach is to use `MinIO <https://docs.min.io/>`__ in
    distributed mode in conjunction with the :ref:`AWS S3 plugin
    <minio>` for Orthanc.

* If using the :ref:`DICOMweb server plugin <dicomweb-server-config>`,
  consider setting configuration option ``StudiesMetadata`` to
  ``MainDicomTags``.

* If using PostgreSQL as a managed cloud service by Microsoft Azure,
  make sure to reduce the verbosity of the logs. If logging is not
  minimal, Osimis has observed an impact on performance.


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

**Status:**

* Since **Orthanc 1.8.2**, the global configuration ``MallocArenaMax``
  automatically sets ``MALLOC_MMAP_THRESHOLD_`` (defaults to ``5``)
  during the startup of Orthanc.

* The ``jodogne/orthanc`` and ``jodogne/orthanc-plugins`` Docker
  images automatically set ``MALLOC_ARENA_MAX`` to ``5`` **since
  release 1.6.1** (cf. `changeset
  <https://github.com/jodogne/OrthancDocker/commit/bd7e9f4665ce8dd6892f82a148cabe8ebcf1c7d9>`__).

* The ``osimis/orthanc`` images automatically set
  ``MALLOC_ARENA_MAX`` to ``5`` **since release 20.12.2**.


.. _scalability-limitations:

Known limitations
-----------------

Exclusive access to the DB in Orthanc <= 1.9.1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Orthanc was originally designed as a mini-DICOM server in 1-to-1
relation with a SQLite database. Until **Orthanc 1.9.1**, because of
this original design, the internal code accessing the DB was affected
by a strong limitation: Inside a single Orthanc process, there was no
concurrent access to the DB.

One solution to avoid this limitation was to have multiple Orthanc
accessing the same DB (works only for MySQL and PostgreSQL) as
presented in this `sample
<https://bitbucket.org/osimis/orthanc-setup-samples/src/master/docker/multiple-orthancs-on-same-db/>`__.
However, this solution was only robust if there was **one single
"writer" Orthanc server** (i.e. only one Orthanc was modifying the
database).  Indeed, the core of Orthanc <= 1.9.1 did not support the
replay of database transactions, which is necessary to deal with
conflicts between several instances of Orthanc that would
simultaneously write to the database.

Concretely, in Orthanc <= 1.9.1, when connecting multiple Orthanc to a
single database by setting ``Lock`` to ``false``, there should only be
one instance of Orthanc acting as a writer and all the other instances
of Orthanc acting as readers only. Be careful to set the option
``SaveJobs`` to ``false`` in the configuration file of all the
instances of Orthanc acting as readers (otherwise the readers would
also modify the database).

Some issues reported in our bug tracker are related this limitation:
`issue 83 <https://bugs.orthanc-server.com/show_bug.cgi?id=83>`__,
`issue 121 <https://bugs.orthanc-server.com/show_bug.cgi?id=121>`__,
`issue 151 <https://bugs.orthanc-server.com/show_bug.cgi?id=151>`__.

This limitation has disappeared with Orthanc 1.9.2 and
PostgreSQL/MySQL plugins 4.0, were the database engine was fully
rewritten.


.. _multiple-writers:

Concurrent accesses to the DB in Orthanc >= 1.9.2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Orthanc 1.9.2 and PostgreSQL/MySQL plugins 4.0**, the database
engine of Orthanc was rewritten from scratch to allow multiple
writers/readers to share the same database. This new feature
necessitated a full refactoring of the database engine, so as to
replay transactions in the case of collisions between concurrent
transactions to the database.

Furthermore, one Orthanc server can also manage several connections to
PostgreSQL or MySQL, in order to improve performance by adding
concurrency. Read-only database transactions are also distinguished
from read-write transactions in order for the database engine to
further optimize the patterns of access.

Summarizing, the **multiple readers/writers** is now possible. Here is
a drawing representing a possible deployment with 4 Orthanc servers,
all sharing the same DICOM images, with some servers handling multiple
connections to a PostgreSQL database for higher throughput:

.. image:: ../images/2021-04-22-MultipleWriters.png
           :align: center
           :width: 500px

Care must be taken to the following aspects:

* Orthanc 1.9.2 must be combined with a database plugin that supports
  multiple writers. This is the case of the PostgreSQL and MySQL
  plugins with version >= 4.0. The built-in SQLite database **does
  not** support multiple writers.
  
* Concurrent access can result in so-called `non-serializable
  transactions
  <https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable>`__
  if two separate database transactions modify the database at the
  same time (cf. ``ErrorCode_DatabaseCannotSerialize`` in the source
  code of Orthanc). Orthanc will **automatically replay such
  transactions** a certain number of times (waiting 100ms more between
  each retry), until the transactions succeed. The plugins provide an
  option to control the maximum number of retries. If the maximum
  number of retries is exceeded, the ``503 Service Unavailable`` HTTP
  error is raised (server overloaded because of unsuccessful retries
  of concurrent transactions).

* If a higher-level application **modifies metadata and/or
  attachments** in the presence of multiple writers, Orthanc provides
  a :ref:`revision mechanism <revisions>` to prevent concurrent
  updates.

* Thanks to this support of concurrent accesses, it is possible to put
  a **load balancer** on the top of the REST API of Orthanc. All the
  DICOM resources (patients, studies, series and instances) are indeed
  shared by all the instances of Orthanc connected to the same
  underlying database. As an application, this might be of great help
  if multiple viewers must connect to Orthanc. In `Kubernetes
  <https://kubernetes.io/>`__, concurrent accesses also make it
  possible to manage a set of replicas of Orthanc (e.g. as `deployment
  <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>`__).

  There are however some caveats if using a load balancer or
  Kubernetes replicas, notably:
    
  - Each Orthanc instance maintains its own list of jobs. Therefore,
    the ``/jobs`` route will return only the jobs of the responding
    Orthanc.

  - The ``/modalities`` or the ``/peers`` are also private to each
    instance of Orthanc in the cluster, as soon as the respective
    options ``DicomModalitiesInDatabase`` and
    ``OrthancPeersInDatabase`` are set to ``true``.

  If you need to use such primitives in your application, you have
  three possibilities: (1) Introduce a distinguished Orthanc server
  that is responsible to take care of all the jobs (including
  modalities and peers), (2) create an :ref:`Orthanc plugin <plugins>`
  (e.g. using :ref:`Python <python-plugin>`) that queries all the
  Orthanc in the cluster and that aggregates all of their answers,
  or (3) do the same using a higher-level framework (such as Node.js).
    

Latency
^^^^^^^

For some queries to the database, Orthanc performs several small SQL
requests. For instance, a request to a route like ``/studies/{id}``
can trigger 6 SQL queries. Given these round-trips between Orthanc and
the DB server, it's important for the **network latency to be as small
as possible**. For instance, if your latency is 20ms, a single request
to ``/studies/{id}`` might take 120ms. Typically, a latency of 1-4 ms
is expected to have correct performances.

As a consequence, if deploying Orthanc in a cloud infrastructure, make
sure that the DB server and Orthanc VMs are located in the **same
datacenter**. Note that most of the time-consuming queries have
already been optimized, and that future versions of Orthanc SDK might
aggregate even more SQL requests.

Starting with Orthanc 1.9.2, and PostgreSQL/MySQL index plugins 4.0,
Orthanc can also be configured to handle **multiple connections to the
database server** by setting the ``IndexConnectionsCount`` to a value
greater than ``1``. This allows concurrent accesses to the database,
which avoids to sequentially wait for a database transaction to be
concluded before starting another one. Having multiple connections
makes the latency problem much less important.


Slow deletions
^^^^^^^^^^^^^^

Deleting large studies can take much time, because removing a large
number of files from a filesystem can be an expensive operation (which
might sound counter-intuitive). This is especially true with HDD
drives, that can be much slower than SSD (`an user has reported
<https://groups.google.com/g/orthanc-users/c/1lga0oFCHN4/m/jF1inrc4AgAJ>`__
a 20 times speedup by switching from HDD to SSD).

If switching from HDD to SDD is not applicable, it is possible to
create an :ref:`storage area plugin <creating-plugins>` that delays
the actual deletion from the filesystem. The plugin would maintain a
queue (e.g. as a SQLite database) of files to be removed. The actual
deletion from the filesystem would be done asynchronously in a
separate thread.

We are looking for funding from the industry to implement such a
plugin.
