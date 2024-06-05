.. _orthanc-storage:

How does Orthanc store its database?
====================================

.. _orthanc-storage-area:

Storage area
------------

**By default** (i.e. if no database plugin such as :ref:`PostgreSQL
<postgresql>` or :ref:`MySQL <mysql>` is used), Orthanc stores all the
DICOM files it receives in a folder called ``OrthancStorage`` on the
filesystem.

More precisely, the ``OrthancStorage`` folder contains a set of
so-called **attachments**, that may correspond to either a DICOM file,
a JSON file, or any user-defined file. Internally, each attachment is
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


SQLite index
------------

Inside the same ``OrthancStorage`` folder, Orthanc maintains a `SQLite
database <https://en.wikipedia.org/wiki/SQLite>`__ called ``index``
that **indexes** all these attachments. The database records, for each
attachment, its compression method, and its MD5 hashes before and
after compression in order to detect disk corruption (cf. the
``StoreMD5ForAttachments`` :ref:`configuration option
<configuration>`).

One attachment must be associated with one :ref:`DICOM resource
<model-world>` (patient, study, series, or instance). Incoming DICOM
files and associated JSON summary are associated with one
instance-level resource, but user-defined attachments can be
associated with any kind of resource. 

Given one DICOM resource, all of its child attachments are identified
by a number between 0 and 65535. Identifiers <= 1023 are reserved for
the Orthanc core, whereas identifiers >= 1024 can be user-defined for
external applications.

Besides the attachments, the database index maintains other
information for each DICOM resource, notably the :ref:`metadata
<metadata>`, the :ref:`history of changes <changes>`, and an
associative map that stores the so-called "main" DICOM tags (to avoid
accessing the storage folder are when this is not needed). The SQLite
database schema is kept as simple as possible, and can be found in the
following two files of the source code of Orthanc:
`PrepareDatabase.sql
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.4/OrthancServer/Sources/Database/PrepareDatabase.sql>`__
and `InstallTrackAttachmentsSize.sql
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.4/OrthancServer/Sources/Database/InstallTrackAttachmentsSize.sql>`__.


Direct access
-------------

Directly accessing the content of the ``OrthancStorage`` folder and
the content of the SQLite/MySQL/PostgreSQL database is strongly
discouraged for several reasons:

* The internal organization outlined above is only true when no
  database plugin is used (e.g. the :ref:`PostgreSQL <postgresql>` and
  :ref:`MySQL <mysql>` plugins can be configured to store the
  attachments inside a database).
* Orthanc can be configured to compress the attachments before writing
  them on the disk (cf. the ``StorageCompression`` option).
* By directly reading the content of ``OrthancStorage``, you bypass
  all the locking mechanisms used by Orthanc, which might result in
  data corruption.
* One SQLite database should be accessed by at most one process at any
  time to avoid any problem (e.g. with NFS filesystems), for reasons
  that are `explained in the SQLite FAQ
  <https://www.sqlite.org/faq.html#q5>`__. Orthanc will stop if it
  receives the ``SQLITE_BUSY`` status.
* The internal structure of the databases might evolve across
  successive versions of Orthanc or of the database plugins.
  
As a consequence, it is **HIGHLY recommended NOT to directly access**
the ``OrthancStorage`` folder and the SQLite/MySQL/PostgreSQL
database. Use the :ref:`REST API <rest>` instead, which contains
primitives to access the attachments (cf. the ``.../attachments/...``
URIs).

The only exception to this rule is for **read-only access when Orthanc
is stopped**, e.g. as a part of a :ref:`backup <backup>` or
:ref:`upgrade/replication <replication>` process.
