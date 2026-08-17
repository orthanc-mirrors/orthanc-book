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
production in hospitals with more than 65TB of data, 340,000 studies
and around 150 millions of instances (please `get in touch with us
<https://www.orthanc-server.com/static.php?page=contact>`__ if you can
share other testimonials).

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

* Make sure to use the latest release of Orthanc (1.13.0 at the time of
  writing) running on a GNU/Linux distribution.

* We suggest to use the latest release of the :ref:`PostgreSQL plugin
  <postgresql>` to store the database index (10.2 at the time of
  writing). Make sure that ``EnableIndex`` is set to ``true``.

* If you build Orthanc yourself, make sure that :ref:`run-time debug assertions <troubleshooting>`
  are turned off. A warning will show in the logs if this is not the
  case. Note that all `pre-compiled binaries
  <https://orthanc.uclouvain.be/downloads/index.html>`__ provided by
  the Orthanc project are correctly configured in that respect, except
  if they are explicitly tagged as "debug".

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
  * ``KeepAlive = true``
  * ``TcpNoDelay = true``
  * ``StorageAccessOnFind = Never``
  * Consider adding ``SaveJobs = false``
  * To prevent users from performing searches that would return the whole
    Orthanc database and therefore consume a lot of resources on the DB server,
    consider adding limits to ``LimitFindResults`` and ``LimitFindInstances``.

* Make sure to fine tune the :ref:`threads related configurations <scalability-threads>`.

* If you are using a postgreSQL plugin between v 4.0 and v 6.2, by default, the
  PostgreSQL index plugin uses 1 single connection to the PostgreSQL
  database. You can have multiple connections by setting the
  ``IndexConnectionsCount`` to a higher value (for instance ``50`` or one per HTTP thread) in
  the ``PostgreSQL`` section of the configuration file. This will
  improve concurrency. Check out :ref:`the explanation below <multiple-writers>`.
  From v 7.0, the default is set to ``50``.

* Since Orthanc 1.9.2 and PostgreSQL plugins 4.0: If you have an
  hospital-wide VNA deployment, you could consider to deploy multiple
  Orthanc servers sharing the same PostgreSQL database. A typical
  scenario is having one "writer" Orthanc server that handles the
  ingesting of DICOM instances, and multiple "reader" Orthanc servers
  with features such as DICOMweb or viewers.

* Since Orthanc 1.12.3 and PostgreSQL plugins 6.0: You may enable
  the ``ReadCommitted`` transaction mode to allow multiple threads to
  write in DB at the same time.  From v 7.0, this is the default configuration.

* From Orthanc 1.11.0: you have the ability to add
  more :ref:`main DICOM tags <main-dicom-tags>` in the Orthanc Index 
  to speed up C-Find, ``tools/find``, DICOMweb QIDO-RS, WADO-RS and 
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

* If using PostgreSQL as a managed cloud service by Microsoft Azure,
  make sure to reduce the verbosity of the logs. If logging is not
  minimal, we have observed an impact on performance.

.. _scalability-threads:

Controlling the threads
-----------------------

Orthanc uses many `threads <https://en.wikipedia.org/wiki/Thread_(computing)>`__ 
to perform operations in parallel.  Depending on your infrastructure and
usage, you may fine tune many configurations related to threading:

+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
|                Option                 |                           Purpose                           | Default |                 Related metrics                 |                                         Recommended Adjustments                                          |
+=======================================+=============================================================+=========+=================================================+==========================================================================================================+
| ``HttpThreadsCount``                  | Threads for handling the Rest API.                          | 50      | ``orthanc_available_http_threads_count``        | Increase when the number of available threads is too low. An alternative adjustment is to spin           |
|                                       |                                                             |         |                                                 | another Orthanc on another VM, connected to the same PostgreSQL Database to spread the workload.         |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``DicomThreadsCount``                 | Threads for handling DICOM SCP operations.                  | 4       | ``orthanc_available_dicom_threads``             | Increase when the number of available threads is too low e.g, if Orthanc must handle many C-STORE        |
|                                       |                                                             |         |                                                 | and C-FIND in parallel. E.g: if Orthanc is connected to 100 DICOM modalities, statistically, there might |
|                                       |                                                             |         |                                                 | be 10 modalities that will try to communicate with Orthanc at a given time.  You should therefore        |
|                                       |                                                             |         |                                                 | increase it to 10.                                                                                       |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``ConcurrentJobs``                    | Maximum number of processing jobs that are simultaneously   | 2       | ``orthanc_jobs_running``                        | Increase when the number of pending jobs is too high.  Note that each job may itself use multiple        |
|                                       | running at any given time.                                  |         | ``orthanc_jobs_pending``                        | to execute.                                                                                              |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``JobsEngineThreadsCount.``           | Number of threads that are used to perform a resource       | 1       |                                                 | Increase to 8-16 if you are using a distributed object storage for the Orthanc Storage.                  |
| ``ResourceModification``              | modification or anonymization.                              |         |                                                 |                                                                                                          |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``StorageLoaderThreadsCount``         | Number of threads that are used to read files from Storage. | 4       | ``orthanc_storage_available_threads``           | Increase when the number of available threads is too low.  Typically if you are using a distributed      |
|                                       |                                                             |         |                                                 | object storage for the Orthanc Storage, increase to e.g. 20.                                             |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``DicomParserThreadsCount``           | Number of threads that are used to parse DICOM files and    | 2       | ``orthanc_dicom_parser_available_threads``      | Increase when the number of available threads is too low.                                                |
|                                       | access DICOM Tags that are not in the SQL Database.         |         |                                                 |                                                                                                          |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``TranscoderThreadsCount``            | Number of threads that are used to transcode DICOM files    | 4       | ``orthanc_transcoder_available_threads``        | Increase when the number of available threads is too low.                                                |
|                                       |                                                             |         |                                                 |                                                                                                          |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+
| ``SequentialDicomReaderThreadsCount`` | Number of threads used for the sequential access to DICOM   | 4       | ``orthanc_sequential_reader_available_threads`` | Increase when the number of available threads is too low.  If not defined, the default value is          |
|                                       | instances (for archive jobs, C-STORE SCU, C-GET SCP and     |         |                                                 | identical to ``StorageLoaderThreadsCount`` so you should probably never adjust this value.               |
|                                       | C-MOVE SCP)                                                 |         |                                                 |                                                                                                          |
+---------------------------------------+-------------------------------------------------------------+---------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------+

Pay attention that all these threads might consume a lot of memory and you might need to limit the memory usage.

.. _scalability-memory:

Controlling memory usage
------------------------

Starting with Orthanc 1.13.0, you may fine tune many configurations related to
the memory consumption.  However, you should always keep in mind that, when
handling large DICOM files, Orthanc needs to store the full file in memory and,
possibly multiple times during a transcoding or a compression so, even if you
have set limits on memory usage, Orthanc might overpass these limits and this might
result in an Out Of memory error (OOM).  E.g. if, at some point, Orthanc must handle
a 3 GB DICOM file while there is only 2 GB RAM on the system, the system will crash !

+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
|                 Option                  |                                       Purpose                                       | Default |               Related metrics                |                                                 Recommended Adjustments                                                 |
+=========================================+=====================================================================================+=========+==============================================+=========================================================================================================================+
| ``MaximumStorageCacheSize``             | Maximum size of the storage cache in MB.  The storage cache                         | 128     | ``orthanc_storage_cache_miss_count``         | The cache is relevant mainly if you are using the received DICOM data directly after you have                           |
|                                         | is stored in RAM and contains a copy of recently accessed files                     |         | ``orthanc_storage_cache_hit_count``          | received it.  E.g. when you are viewing data directly after acquisition or if you are using                             |
|                                         |                                                                                     |         | ``orthanc_storage_cache_count``              | Orthanc as a router.  In this case, it might be interresting to have a large cache size (possibly                       |
|                                         |                                                                                     |         | ``orthanc_storage_cache_size_mb``            | of multiple GB) to avoid reading data from disk.                                                                        |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``DicomParserCacheSize``                | Maximum size of the cache of parsed DICOM files in MB.                              | 256     | ``orthanc_dicom_parser_cache_miss_count``    | This cache is relevant when e.g. a viewer or the Rest API request the same DICOM tags multiple times.                   |
|                                         | is stored in RAM and contains a copy of recently accessed files                     |         | ``orthanc_dicom_parser_cache_hit_count``     | However, it is expected that the cache miss is very high and you should probably not worry about it.                    |
|                                         |                                                                                     |         | ``orthanc_dicom_parser_cache_count``         |                                                                                                                         |
|                                         |                                                                                     |         | ``orthanc_dicom_parser_cache_size_mb``       |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``TranscoderCacheSize``                 | Maximum size of the cache of transcoded DICOM files in MB.                          | 256     | ``orthanc_transcoder_cache_miss_count``      | This cache is relevant when e.g. a viewer or the Rest API request the same transcoded DICOM files multiple times.       |
|                                         | is stored in RAM and contains a copy of recently accessed files                     |         | ``orthanc_transcoder_cache_hit_count``       | However, it is expected that the cache miss is very high and you should probably not worry about it.                    |
|                                         |                                                                                     |         | ``orthanc_transcoder_cache_count``           |                                                                                                                         |
|                                         |                                                                                     |         | ``orthanc_transcoder_cache_size_mb``         |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``StorageMemoryCapacity``               | Peak amount of RAM (in MB) that can be allocated by the threads                     | 512     | ``orthanc_storage_memory_usage_mb``          | Monitor ``orthanc_storage_memory_usage_mb``.  If it is regularly close to the configured capacity, this means that      |
|                                         | loading from the storage area.                                                      |         | ``orthanc_storage_memory_max_usage_mb``      | some storage loader threads might will have to wait until more RAM is available which will degrade the performance.     |
|                                         | Note that this limit can be exceeded when a single file is larger than this option. |         | ``orthanc_storage_memory_count``             |                                                                                                                         |
|                                         |                                                                                     |         | ``orthanc_storage_memory_capacity_mb``       |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``DicomParserMemoryCapacity``           | Peak amount of RAM (in MB) that can be allocated by the threads                     | 256     | ``orthanc_dicom_parser_memory_usage_mb``     | Monitor ``orthanc_dicom_parser_memory_usage_mb``.  If it is regularly close to the configured capacity, this means that |
|                                         | that parse the DICOM files.                                                         |         | ``orthanc_dicom_parser_memory_max_usage_mb`` | some DICOM parser threads might will have to wait until more RAM is available which will degrade the performance.       |
|                                         | Note that this limit can be exceeded when a single file is larger than this option. |         | ``orthanc_dicom_parser_memory_count``        |                                                                                                                         |
|                                         |                                                                                     |         | ``orthanc_dicom_parser_memory_capacity_mb``  |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``TranscoderMemoryCapacity``            | Peak amount of RAM (in MB) that can be allocated by the threads                     | 256     | ``orthanc_transcoder_memory_usage_mb``       | Monitor ``orthanc_transcoder_memory_usage_mb``.  If it is regularly close to the configured capacity, this means that   |
|                                         | that transcode the DICOM files.                                                     |         | ``orthanc_transcoder_memory_max_usage_mb``   | some transcoder threads might will have to wait until more RAM is available which will degrade the performance.         |
|                                         | Note that this limit can be exceeded when a single file is larger than this option. |         | ``orthanc_transcoder_memory_count``          |                                                                                                                         |
|                                         |                                                                                     |         | ``orthanc_transcoder_memory_capacity_mb``    |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| ``SequentialDicomReaderWindowCapacity`` | Maximum amount of RAM (in MB) allocated to each local                               | 128     |                                              | There is currently no way to monitor these memory consumptions.                                                         |
|                                         | sliding-window buffer for each thread accessing a set of DICOM instances in         |         |                                              |                                                                                                                         |
|                                         | sequential order.  See also the ``SequentialDicomReaderWindowSize`` configuration.  |         |                                              |                                                                                                                         |
|                                         | Note that this limit can be exceeded when a single file is larger than this option. |         |                                              |                                                                                                                         |
+-----------------------------------------+-------------------------------------------------------------------------------------+---------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+

All the **Caches** will always fill to their full capacity as soon as they are used so you should always expect them to consume the declared amount of RAM.

For the **MemoryCapacities**, the RAM will be used only when a thread requires RAM in this particular RAM space and the RAM will be released as soon
as the thread has finished its job with this particular data.  If, at some point, a thread requires X MB of RAM and this amount of RAM is currently not
available, it will have to wait until other threads have freed X MB.

E.g.  If you have declared 512 MB of ``StorageMemoryCapacity`` and if have 2 threads that have reserved 200 MB each to each handle a 200 MB file and
a third thread would like to reserve 200 MB for another file, the third thread will have to wait until one of the first two threads has completed
its work and until there are at least 200 MB of available memory in that RAM space.

If you have declared 512 MB of ``StorageMemoryCapacity`` and if have 2 threads that have reserved 200 MB each to each handle a 200 MB file and
a third thread would like to reserve 600 MB for another file, the third thread will have to wait until both threads have completed their work and,
only at that time, the 3rd thread will be allocated 600 MB (more than the declared maximum capacity !!!).  The maximum usage of this RAM space will be recorded
in the ``orthanc_*_memory_max_usage_mb`` metrics.

**Note**: Orthanc also uses RAM that is not part of these RAM spaces where the memory is controlled.  It is very difficult to evaluate the amount
of RAM that is not controlled but you should consider that an extra 128 MB is required.


How can I compute the total amount of memory Orthanc will consume ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this section, we will consider 2 scenario: 
- in the first one, you know that your Orthanc
instance only handles `small` DICOM files that are less than 10-20 MB (MRI, CT, CR, DX, standard US, ...)
- in the second one, where Orthanc also handles `large` DICOM files between 300 MB and 4 GB (Mammography, Cardiac US, ...).

For both scenario, consider we have these configurations:

.. code-block:: json

  {
    "ConcurrentJobs": 8,
    
    "StorageLoaderThreadsCount": 20,
    "StorageMemoryCapacity": 512,
    "MaximumStorageCacheSize": 128,

    "SequentialDicomReaderThreadsCount": 20,
    "SequentialDicomReaderWindowCapacity": 128,

    "DicomParserThreadsCount": 2,
    "DicomParserCacheSize": 256,
    "DicomParserMemoryCapacity": 256,

    "TranscoderThreadsCount": 4,
    "TranscoderCacheSize": 256,
    "TranscoderMemoryCapacity": 256
  }

In the first scenario, where Orthanc handles small files, Orthanc should never exceed the ``*MemoryCapacity`` configurations:

.. code-block:: txt

  MaximumStorageCacheSize:                          128 MB
  DicomParserCacheSize:                             256 MB
  TranscoderCacheSize:                              256 MB
  ------------------------------------------------------------------
  TOTAL CACHES                                                640 MB

  StorageMemoryCapacity:                            512 MB
  DicomParserMemoryCapacity:                        256 MB
  TranscoderMemoryCapacity:                         256 MB
  SequentialDicomReaderWindowCapacity 
  * SequentialDicomReaderThreadsCount:  128*20 =   2560 MB
  ------------------------------------------------------------------
  TOTAL MEMORY CAPACITIES                                    3584 MB

  EXTRA MARGIN FOR UNMANAGED MEMORY                           128 MB

  ==================================================================
  TOTAL                                                      4352 MB 

In the second scenario, let's consider the worst case scenario where, at a given time, each active thread is handling a file
that is 600 MB, therefore, exceeding the ``*MemoryCapacity`` configurations:

.. code-block:: txt

  MaximumStorageCacheSize:                          128 MB
  DicomParserCacheSize:                             256 MB
  TranscoderCacheSize:                              256 MB
  ------------------------------------------------------------------
  TOTAL CACHES                                                640 MB
  
  StorageMemoryCapacity (overpassed):               600 MB
  DicomParserMemoryCapacity (overpassed):           600 MB
  TranscoderMemoryCapacity (overpassed):            600 MB
  SequentialDicomReaderWindowCapacity (overpassed) 
  * SequentialDicomReaderThreadsCount:  600*20 =  12000 MB
  ------------------------------------------------------------------
  TOTAL MEMORY CAPACITIES                                   13800 MB
  
  EXTRA MARGIN FOR UNMANAGED MEMORY                           128 MB

  ==================================================================
  TOTAL                                                     14568 MB 


Running Orthanc on a system with limited RAM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are running Orthanc on a system with very limited memory, you should
configure Orthanc accordingly.

You should probably leave 64 MB to the OS, don't use any caches in Orthanc, reduce the number of **SequentialDicomReaderThreadsCount**
and reduce all **MemoryCapacities** and reduce the number of HTTP and DICOM threads. E.g.:

.. code-block:: txt

  MaximumStorageCacheSize:                            0 MB
  DicomParserCacheSize:                               0 MB
  TranscoderCacheSize:                                0 MB
  ------------------------------------------------------------------
  TOTAL CACHES                                                  0 MB
  
  StorageMemoryCapacity:                             32 MB
  DicomParserMemoryCapacity:                         32 MB
  TranscoderMemoryCapacity:                          32 MB
  SequentialDicomReaderWindowCapacity 
  * SequentialDicomReaderThreadsCount:  16*2   =     32 MB
  ------------------------------------------------------------------
  TOTAL MEMORY CAPACITIES                                     128 MB
  
  EXTRA MARGIN FOR UNMANAGED MEMORY                           128 MB

  ==================================================================
  TOTAL                                                       256 MB 


For this scenario, your configuration would look like:

.. code-block:: json

  {
    "ConcurrentJobs": 2,
    "HttpThreadsCount": 8,
    "DicomThreadsCount": 2,
    
    "StorageLoaderThreadsCount": 2,
    "StorageMemoryCapacity": 32,
    "MaximumStorageCacheSize": 0,

    "SequentialDicomReaderThreadsCount": 2,
    "SequentialDicomReaderWindowCapacity": 16,

    "DicomParserThreadsCount": 2,
    "DicomParserCacheSize": 0,
    "DicomParserMemoryCapacity": 32,

    "TranscoderThreadsCount": 2,
    "TranscoderCacheSize": 0,
    "TranscoderMemoryCapacity": 32
  }


Observed memory consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The absence of memory leaks in Orthanc is verified thanks to `valgrind
<https://valgrind.org/>`__.

**Note:** It is not yet clear if the below section is still applicable
to Orthanc 1.13.0 since we have introduced new memory handling configurations.


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

* The ``orthancteam/orthanc`` images automatically set
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
<https://github.com/orthanc-server/orthanc-setup-samples/tree/master/docker/multiple-orthancs-on-same-db/>`__.
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
`issue 83 <https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=83>`__,
`issue 121 <https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=121>`__,
`issue 151 <https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=151>`__.

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
  of concurrent transactions).  Note that, since version 6.0 of the PostgreSQL
  plugin, it is now possible to configure the ``TransactionMode`` to 
  ``ReadCommitted`` instead of the default ``Serializable`` mode to avoid
  most of the transactions collisions.  This option is not (yet) available
  for the MySQL plugin.

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

  - Similarly, each Orthanc instance maintains its own :ref:`status
    for the resources it has received <stable-resources>`. Thus, the
    ``IsStable`` information is local to each Orthanc instance.

  - The ``/modalities`` or the ``/peers`` are also private to each
    instance of Orthanc in the cluster, as soon as the respective
    options ``DicomModalitiesInDatabase`` and
    ``OrthancPeersInDatabase`` are set to ``true``.

  If you need to use such primitives in your application, you have
  three possibilities: (1) Introduce a distinguished Orthanc server
  that is responsible to take care of all the jobs (including
  modalities and peers) and/or to receive all the DICOM instances, (2)
  create an :ref:`Orthanc plugin <plugins>` (e.g. using :ref:`Python
  <python-plugin>` or :ref:`Java <java-plugin>`) that queries all the
  Orthanc in the cluster and that aggregates all of their answers,
  or (3) do the same using a higher-level framework (such as Node.js).
    

Latency
^^^^^^^

Up to v 6.2, for some queries to the database, Orthanc performs several small SQL
requests. For instance, a request to a route like ``/studies/{id}``
can trigger 6 SQL queries. Given these round-trips between Orthanc and
the DB server, it's important for the **network latency to be as small
as possible**. For instance, if your latency is 20ms, a single request
to ``/studies/{id}`` might take 120ms. Typically, a latency of 1-4 ms
is expected to have correct performances.

As a consequence, if deploying Orthanc in a cloud infrastructure, make
sure that the DB server and Orthanc VMs are located in the **same
datacenter**. Note that most of the time-consuming queries have
already been optimized in v 6.0 and a huge improvement has been implemented
in v 7.0.

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

If switching from HDD to SDD is not applicable, you may also use 
the :ref:`Delayed Deletion plugin <delayed-deletion-plugin>` .
The plugin would maintains a queue of files to be removed. The actual
deletion from the filesystem is done asynchronously in a
separate thread.
