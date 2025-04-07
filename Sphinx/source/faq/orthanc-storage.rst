.. _orthanc-storage:

How does Orthanc store its database?
====================================

Orthanc actually uses 2 different places to store its data:

* the files are saved in the :ref:`Storage Area <orthanc-storage-area>`, 
  usually, a standard file-system but it can also be replaced by a cloud 
  :ref:`object storage <object-storage>` like AWS S3, Azure blob storage or Google cloud.
* a summary of all resources is saved in the :ref:`Index <orthanc-index>`
  that is a SQL database.

Orthanc always needs both the ``Storage`` and the ``Index`` and these 2 components
must always remain synchronized.


.. _orthanc-storage-area:

Storage area
------------

**By default**, Orthanc stores all the
DICOM files it receives in a folder called ``OrthancStorage`` on the
filesystem (defined in the ``StorageDirectory`` configuration in the 
:ref:`configuration file <configuration>`).

The default storage can also be replaced by a plugin to store these 
files in an :ref:`object storage <object-storage>` like AWS S3, Azure 
blob storage or Google cloud.  

Alternatively, the file storage can also be implemented inside a 
:ref:`PostgreSQL <postgresql>` or :ref:`MySQL <mysql>` Database but 
this is actually quite uncommon.

More precisely, the ``Storage`` contains a set of
so-called **attachments**, that may correspond to either a DICOM file,
a JSON file, or any user-defined file. 

Internally, each attachment is
automatically associated with an `universally unique identifier (UUID)
<https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.
Orthanc can be configured to compress these files on-the-fly in order
to save disk space (cf. the ``StorageCompression`` :ref:`configuration
option <configuration>`).

To reduce the number of files in a single directory (which is
something that some operating systems might not like), a 3-level
hierarchy of directories is created to store the attachments: The
first two hexadecimal characters of the UUID give the first-level
folder, and the two next characters give the second-level folder.



.. _orthanc-index:

Orthanc Index
-------------

Orthanc also maintains a summary of all the DICOM resources in a SQL
database in the so called ``Index``.  This ``Index`` is mandatory to
rapidly provide information when browsing and accessing the resources
either through the :ref:`REST API of Orthanc <rest>` or through the
:ref:`DICOM protocol <dicom-guide>`.

**By default**, this index is implemented in a `SQLite
database <https://en.wikipedia.org/wiki/SQLite>`__ that is stored
in the same folder as the files (if you are using a file-system).
This folder is defined by the ``IndexDirectory`` in the :ref:`configuration
option <configuration>`)

The default ``Index`` can also be replaced by a plugin to store the 
index in a :ref:`PostgreSQL <postgresql>`, :ref:`MySQL <mysql>` or 
:ref:`ODBC <odbc>` Database.


Index content
-------------

The ``Index`` database **indexes** all the attachments stored in the ``Storage``. 
The database records, for each attachment, its compression method, and its MD5 hashes before and
after compression in order to detect disk corruption (cf. the
``StoreMD5ForAttachments`` :ref:`configuration option
<configuration>`).

One attachment must be associated with one :ref:`DICOM resource
<model-world>` (patient, study, series, or instance). Incoming DICOM
files are associated with one instance-level resource, but user-defined attachments can be
associated with any kind of resource. 

Given one DICOM resource, all of its child attachments are identified
by a number between 0 and 65535. Identifiers <= 1023 are reserved for
the Orthanc core, whereas identifiers >= 1024 can be user-defined for
external applications.

Besides the attachments, the database index maintains other
information for each DICOM resource, notably the :ref:`metadata
<metadata>`, the :ref:`history of changes <changes>`, and an
associative map that stores the so-called "main" DICOM tags (to avoid
accessing the storage folder are when this is not needed). 

The database schema is kept as simple as possible, e.g, for SQLite,
the schema can be found in the following two files of the source code of Orthanc:
`PrepareDatabase.sql
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.7/OrthancServer/Sources/Database/PrepareDatabase.sql>`__
and `InstallTrackAttachmentsSize.sql
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.7/OrthancServer/Sources/Database/InstallTrackAttachmentsSize.sql>`__.


Direct access
-------------

Directly accessing the content of the ``Storage`` folder and
the content of the SQLite/MySQL/PostgreSQL ``Index`` database is strongly
discouraged for several reasons:

* The ``Storage`` internal organization outlined above is only true when no
  database plugin is used (e.g. the :ref:`PostgreSQL <postgresql>` and
  :ref:`MySQL <mysql>` plugins can be configured to store the
  attachments inside a database).
* Orthanc can be configured to compress the attachments before writing
  them on the disk (cf. the ``StorageCompression`` option) making them
  less easily readable by an external tool (check the ``OrthancRecoverCompressedFile``
  executable in the Orthanc distribution).  
* By directly reading/writing the content of the ``Storage``, you bypass
  all the locking mechanisms used by Orthanc, which might result in
  data corruption.
* If you are using SQLite for the ``Index``, one SQLite database should be accessed by at most one process at any
  time to avoid any problem (e.g. with NFS filesystems), for reasons
  that are `explained in the SQLite FAQ
  <https://www.sqlite.org/faq.html#q5>`__. Orthanc will stop if it
  receives the ``SQLITE_BUSY`` status.
* The internal structure of the databases might evolve across
  successive versions of Orthanc or of the database plugins.
  
As a consequence, it is **HIGHLY recommended NOT to directly access**
the ``Storage`` and the SQLite/MySQL/PostgreSQL ``Index``
database. Use the :ref:`REST API <rest>` instead, which contains
primitives to access the attachments (cf. the ``.../attachments/...``
URIs) and all other resources.

The only exception to this rule is for **read-only access when Orthanc
is stopped**, e.g. as a part of a :ref:`backup <backup>` or
:ref:`upgrade/replication <replication>` process.
