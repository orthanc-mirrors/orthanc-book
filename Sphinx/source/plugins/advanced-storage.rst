.. _advanced-storage:


Advanced storage plugin
=======================

.. contents::

This **official plugin** extends Orthanc with an advanced
storage mechanism:

- It enables customization of the structure of the Orthanc storage.
- It supports multiple storages.
- It supports indexing an existing storage - replacing the :ref:`Indexer <indexer>` plugin.
- It supports delayed deletion - replacing the  :ref:`Delayed deletion plugin <delayed-deletion-plugin>` plugin

Restrictions
------------

.. warning:: 
  This plugin only works with either the default SQLite database (from Orthanc 1.12.8) 
  or the PostgreSQL Index plugin (from version 8.0).


How to get it ?
---------------

The source code is available on `Github <https://github.com/orthanc-server/orthanc-advanced-storage/>`__.

Binaries are included in:

- The `orthancteam/orthanc Docker image <https://hub.docker.com/r/orthancteam/orthanc>`__
- The `Windows Installer <https://www.orthanc-server.com/download-windows.php>`__
- The `MacOS packages <https://www.orthanc-server.com/static.php?page=download-mac>`__

Release notes are available `here <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/release-notes.md>`__.

Compilation instructions are available below.


Usage
-----

.. highlight:: json

Once Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancAuthorization/Build/libAdvancedStorage.so"
    ],
    "AdvancedStorage" : {
      "Enable": true,

      // .. see below "configuration section"
    }
  }

Orthanc must of course be restarted after the modification of its
configuration file.


Configuration
-------------

A full description of all configuration options is available directly
in the source code `default configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`__.


Multiple storages
-----------------

If your current storage gets full, you may configuration the plugin
to use another disk to store newly received DICOM files::

  {
    "StorageDirectory": "/var/lib/orthanc/db/",
    ...
    "AdvancedStorage": {
      "Enable": true,
      "MultipleStorages": {
        "Storages": {
          "ext1": "/mnt/disk1/orthanc",
          "ext2": "/mnt/disk2/orthanc",
        },
        "CurrentWriteStorage": "ext1"
    }
  }

E.g., with the above configuration, Orthanc might have ingested DICOM
files a long time ago.  These files are still stored in ``/var/lib/orthanc/db/``
(the main ``StorageDirectory``).  The advanced storage plugin will
still be able to read files from this directory.

Then, the advanced storage plugin has been configured to use 2 extra disks
whose ids are ``ext1`` and ``ext2``.  These identifiers can never change since
they are stored in DB for each file.

The ``CurrentWriteStorage`` configuration defines where the new received
files are stored.

Note that, if one of the disks gets full, you'll have to switch the ``CurrentWriteStorage``
configuration manually.


Customizing paths
-----------------

By default, in Orthanc, each file is
automatically associated with an `universally unique identifier (UUID)
<https://en.wikipedia.org/wiki/Universally_unique_identifier>`__ and files are
stored in a 3-level hierarchy of directories; the
first two hexadecimal characters of the UUID give the first-level
folder, and the two next characters give the second-level folder (e.g.: ``/var/lib/orthanc/db/5f/39/5f3936ea-95b6-4ad9-b0f1-4075be3e52d0``).  
This structure is machine friendly but is not convenient to browse for a human.

One of the great feature of the advanced storage plugin is its ability to
customize the storage structure.  The ``NamingScheme`` configuration enables full
customization of the storage structure by using :ref:`DICOM Tags <main-dicom-tags>` or :ref:`Orthanc identifiers 
<orthanc-ids>` from the DICOM instance.

E.g., a ``NamingScheme`` of ``{PatientID} - {PatientName}/{StudyDate} - {StudyDescription}/{SeriesNumber}/{pad6(InstanceNumber)}-{UUID}{.ext}``
will produce paths like ``1234 - WHO^JOHN/20241102 - HEAD SCAN/100/000007-5f3936ea-95b6-4ad9-b0f1-4075be3e52d0.dcm``.

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`__ for 
a full description of the keywords that can be used in the ``NamingScheme``.

To prevent files from being overwritten, it is very important that their path is unique !
Therefore, your NamingScheme must always include:

- either the file ``{UUID}``
- or, if you have not set ``"OverwriteInstances"`` to true, at least:
    
  - a patient identifier ``{PatientID}`` or ``{OrthancPatientID}``,
  - a study identifier ``{StudyInstanceUID}`` or ``{OrthancStudyID}``,
  - a series identifier ``{SeriesInstanceUID}`` or ``{OrthancSeriesID}``,
  - an instance identifier ``{SOPInstanceUID}`` or ``{OrthancInstanceID}``

The ``NamingScheme`` defines a **relative** path to either the ``"StorageDirectory"`` of Orthanc or one of
the ``"MultipleStorages"`` of this plugin.
    
The relative path generated from the ``NamingScheme`` is stored in the SQL DB.  Therefore, you may change the
``NamingScheme`` at any time and you'll still be able to access previously saved files.


Indexer mode
------------

This plugin can actually also replace the :ref:`Folder Indexer plugin<indexer>`.  The
Indexer plugin needed a separate SQLite DB which made it impossible to use with multiple
Orthanc instances or uncomfortable to use together with the PostgreSQL plugin.

The advanced-storage implements the same features as the Indexer plugin without requiring
a separate DB.  Everything is stored in the Orthanc main Database.

The ``Indexer mode`` has its own configuration::

  {
    "StorageDirectory": "/var/lib/orthanc/db/",
    ...
    "AdvancedStorage": {
      "Enable": true,
      "Indexer": {
        "Enable": true,
        "Folders": [ "/tmp/dicom-files" ],
        ...
        "TakeOwnership": false
    }
  }

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`__ for 
all the ``Indexer mode`` configurations.

If you set ``TakeOwnership`` to false (default), the ``Indexer mode`` will have the
exact same behavior as the Indexer plugin.  Orthanc will not own the indexed files
and will therefore not delete the files if you delete the related resources in Orthanc.

If you set ``TakeOwnership`` to true, all indexed files will belong to Orthanc
and will therefore delete the files if you delete the related resources in Orthanc.

Setting ``TakeOwnership`` to true is useful e.g. when you have been using Orthanc with
the default SQLite DB and you wish to switch to PostgreSQL.  Orthanc will then be able
to *adopt* the DICOM files from the previous Orthanc installation.  TODO: check this sample setup TODO


Delayed deletion mode
---------------------

This plugin can actually also replace the :ref:`Delayed deletion plugin<delayed-deletion-plugin>`.  The
Delayed deletion plugin needed a separate SQLite DB which made it impossible to use with multiple
Orthanc instances or uncomfortable to use together with the PostgreSQL plugin.

The advanced-storage implements the same features as the Delayed deletion plugin without requiring
a separate DB.  Everything is stored in the Orthanc main Database.

The ``Delayed deletion mode`` has its own configuration::

  {
    "StorageDirectory": "/var/lib/orthanc/db/",
    ...
    "AdvancedStorage": {
      "Enable": true,
      "DelayedDeletion": {
        "Enable": true,
        ...
    }
  }

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`__ for 
all the ``Delayed deletion mode`` configurations.



REST API extensions
-------------------

This plugin brings in a few new API routes:

**adopt-instance** to adopt an instance that is outside the storage.  This is equivalent to the
Indexer mode adopting an instance::

  $ curl http://localhost:8042/plugins/advances-storage/adopt-instance -d @- << EOF
  {
    "Path" : "/tmp/my-dicom-file.dcm",
    "TakeOwnership" : false
  }
  EOF

**abandon-instance** to remove an adopted instance (if Orthanc is not the owner of the instance).  
This is equivalent to the Indexer mode abandoning an instance e.g. the indexed file has been deleted::

  $ curl http://localhost:8042/plugins/advances-storage/abandon-instance -d @- << EOF
  {
    "Path" : "/tmp/my-dicom-file.dcm"
  }
  EOF

**move-storage** to move a resource from a storage to another one.  Note: it does not recompute the relative path 
but only change the base path (aka ``StorageId``)::

  $ curl http://localhost:8044/plugins/advanced-storage/move-storage -d @- << EOF
  {
    "Resources": ["ca58b590-8a115ed5-906f7f21-c7af8058-2637f722"],
    "TargetStorageId": "ext2"
  }
  EOF


The plugin now provides extra information in the **../attachments/info** routes.  E.g.::

  $ curl http://localhost:8042/instances/ca58b590-8a115ed5-906f7f21-c7af8058-2637f722/attachments/dicom/info 

  will return these new fields

  {
    ...
    "IsOwnedByOrthanc" : true,
    "Path" : "1234 - WHO^JOHN/20241102 - HEAD SCAN/100/000007-5f3936ea-95b6-4ad9-b0f1-4075be3e52d0.dcm",
    "StorageId" : "ext1"
  }


The plugin also provides its status in this route **/plugins/advanced-storage/status**.  E.g.::

  $ curl http://localhost:8042/plugins/advanced-storage/status 

  will return 

  {
    "DelayedDeletionIsActive": true,
    "FilesPendingDeletion": 123,
    "IndexerIsActive": true
  }


Compilation
-----------

.. highlight:: bash

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``AdvancedStorage``
that contains the plugin.
