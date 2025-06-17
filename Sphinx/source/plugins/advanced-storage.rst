.. _advanced-storage:

Advanced Storage Plugin
======================

.. contents::

This **official plugin** extends Orthanc with an advanced storage mechanism:

- It enables customization of the structure of the Orthanc storage.
- It supports multiple storages.
- It supports indexing an existing storage, replacing the :ref:`Indexer <indexer>` plugin.
- It supports delayed deletion, replacing the :ref:`Delayed Deletion plugin <delayed-deletion-plugin>`.

Restrictions
------------

.. warning::
   This plugin only works with either the default SQLite database (from Orthanc 1.12.8) or the PostgreSQL Index plugin (from version 8.0).

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

Orthanc must, of course, be restarted after the modification of its configuration file.

Configuration
-------------

A full description of all configuration options is available directly in the source code `default configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`__.

Multiple storages
-----------------

If your current storage gets full, you may configure the plugin to use another disk to store newly received DICOM files:

.. code-block:: json

  {
    "StorageDirectory": "/var/lib/orthanc/db/",
    ...
    "AdvancedStorage": {
      "Enable": true,
      "MultipleStorages": {
        "Storages": {
          "ext1": "/mnt/disk1/orthanc",
          "ext2": "/mnt/disk2/orthanc"
        },
        "CurrentWriteStorage": "ext1"
    }
  }

For example, with the above configuration, Orthanc might have ingested DICOM files a long time ago. 
These files are still stored in ``/var/lib/orthanc/db/`` (the main ``StorageDirectory``). The advanced storage plugin will still be able to read files from this directory.

Then, the advanced storage plugin has been configured to use two extra disks whose IDs are ``ext1`` and ``ext2``. 
These identifiers can never change since they are stored in the database for each file.

The ``CurrentWriteStorage`` configuration defines where the new received files are stored.

Note that if one of the disks gets full, you will have to switch the ``CurrentWriteStorage`` configuration manually.

Customizing paths
-----------------

By default, in Orthanc, each file is automatically associated with a `Universally Unique Identifier (UUID) <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_ and files are stored in a 3-level hierarchy of directories. The first two hexadecimal characters of the UUID give the first-level folder, and the two next characters give the second-level folder (e.g., ``/var/lib/orthanc/db/5f/39/5f3936ea-95b6-4ad9-b0f1-4075be3e52d0``). This structure is machine-friendly but is not convenient to browse for a human.

One of the great features of the advanced storage plugin is its ability to customize the storage structure. The ``NamingScheme`` configuration enables full customization of the storage structure by using :ref:`DICOM Tags <main-dicom-tags>` or :ref:`Orthanc identifiers <orthanc-ids>` from the DICOM instance.

For example, a ``NamingScheme`` of ``{PatientID} - {PatientName}/{StudyDate} - {StudyDescription}/{SeriesNumber}/{pad6(InstanceNumber)}-{UUID}{.ext}`` will produce paths like ``1234 - WHO^JOHN/20241102 - HEAD SCAN/100/000007-5f3936ea-95b6-4ad9-b0f1-4075be3e52d0.dcm``.

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`_ for a full description of the keywords that can be used in the ``NamingScheme``.

To prevent files from being overwritten, it is very important that their path is unique! Therefore, your ``NamingScheme`` must always include:

- Either the file ``{UUID}``
- Or, if you have not set ``"OverwriteInstances"`` to true, at least:

  - A patient identifier ``{PatientID}`` or ``{OrthancPatientID}``
  - A study identifier ``{StudyInstanceUID}`` or ``{OrthancStudyID}``
  - A series identifier ``{SeriesInstanceUID}`` or ``{OrthancSeriesID}``
  - An instance identifier ``{SOPInstanceUID}`` or ``{OrthancInstanceID}``

The ``NamingScheme`` defines a **relative** path to either the ``"StorageDirectory"`` of Orthanc or one of the ``"MultipleStorages"`` of this plugin.

The relative path generated from the ``NamingScheme`` is stored in the SQL database. Therefore, you may change the ``NamingScheme`` at any time and you will still be able to access previously saved files.

Indexer Mode
------------

When the indexer mode is enabled, the plugin continuously synchronizes the content of an Orthanc server with the content of a filesystem, which can then be accessed through Orthanc based on the :ref:`DICOM model of the real world <model-world>`. The indexed DICOM resources are immediately available in a web interface and in a web viewer and can be queried/retrieved by DICOM clients. The DICOM files are **not** copied into the Orthanc storage, so this solution has a very small footprint in terms of storage requirements.

The indexer mode can parse multiple folders. If new DICOM files are ingested through DICOM or HTTP, they are saved in the default Orthanc storage (defined by ``StorageDirectory`` or by the ``MultipleStorages`` configurations).

**Note:** The plugin should never be configured to index its own Orthanc storage! However, the plugin might be used to index another Orthanc storage, e.g., to perform a migration from SQLite to PostgreSQL.

**Note:** This plugin is actually a replacement for the :ref:`Folder Indexer plugin <indexer>`. The Indexer plugin needed a separate SQLite database, which made it impossible to use with multiple Orthanc instances or uncomfortable to use together with the PostgreSQL plugin. The advanced storage plugin implements the same features as the Indexer plugin without requiring a separate database. Everything is stored in the Orthanc main database.

The ``Indexer mode`` has its own configuration:

.. code-block:: json

   {
     "StorageDirectory": "/var/lib/orthanc/db/",
     "AdvancedStorage": {
       "Enable": true,
       "Indexer": {
         "Enable": true,
         "Folders": ["/tmp/dicom-files"],
         "TakeOwnership": false
       }
     }
   }

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`_ for all the ``Indexer mode`` configurations.

If you set ``TakeOwnership`` to false (default), the ``Indexer mode`` will have the exact same behavior as the Indexer plugin. Orthanc will not own the indexed files and will therefore not delete the files if you delete the related resources in Orthanc.

If you set ``TakeOwnership`` to true, all indexed files will belong to Orthanc, and Orthanc will therefore delete the files if you delete the related resources in Orthanc.

Setting ``TakeOwnership`` to true is useful, e.g., when you have been using Orthanc with the default SQLite database and you wish to switch to PostgreSQL. Orthanc will then be able to *adopt* the DICOM files from the previous Orthanc installation. Check this `sample setup <https://github.com/orthanc-server/orthanc-setup-samples/tree/master/docker/sqlite-to-postgresql>`_.

Delayed Deletion Mode
---------------------

On some file systems, the deletion of files can be quite long, and therefore, a DELETE request on a study with thousands of instances can last minutes.

The delayed deletion mode handles file deletion asynchronously by pushing the files to delete into a queue that is handled asynchronously.

**Note:** This plugin actually replaces the :ref:`Delayed Deletion plugin <delayed-deletion-plugin>`. The Delayed Deletion plugin needed a separate SQLite database, which made it impossible to use with multiple Orthanc instances or uncomfortable to use together with the PostgreSQL plugin. The advanced storage plugin implements the same features as the Delayed Deletion plugin without requiring a separate database. Everything is stored in the Orthanc main database.

The ``Delayed deletion mode`` has its own configuration:

.. code-block:: json

   {
     "StorageDirectory": "/var/lib/orthanc/db/",
     "AdvancedStorage": {
       "Enable": true,
       "DelayedDeletion": {
         "Enable": true
       }
     }
   }

Check the `configuration file <https://github.com/orthanc-server/orthanc-advanced-storage/blob/master/Plugin/Configuration.json>`_ for all the ``Delayed deletion mode`` configurations.

Typical Scenarios
^^^^^^^^^^^^^^^^^

Running Out of Storage
""""""""""""""""""""""

You have an Orthanc instance running for a long time, and its storage is almost full. Right now, you have a configuration like this one:

.. code-block:: json

   {
     "IndexDirectory": "C:/Orthanc",
     "StorageDirectory": "C:/Orthanc"
   }

You can now define an additional volume to store new data, e.g., in ``D:/Orthanc``, and keep the old studies in ``C:/Orthanc``:

.. code-block:: json

   {
     "IndexDirectory": "C:/Orthanc",
     "StorageDirectory": "C:/Orthanc",
     "AdvancedStorage": {
       "MultipleStorages": {
         "Storages": {
           "1": "D:/Orthanc"
         },
         "CurrentWriteStorage": "1"
       }
     }
   }

Importing All Studies from Another PACS
"""""""""""""""""""""""""""""""""""""""

You were using another PACS and want to switch to Orthanc but have limited storage, or you just want to try Orthanc on your existing dataset. You can use the ``Indexer mode`` to parse the existing dataset, e.g., with this kind of configuration:

.. code-block:: json

   {
     "IndexDirectory": "C:/Orthanc",
     "StorageDirectory": "C:/Orthanc",
     "AdvancedStorage": {
       "Indexer": {
         "Folders": ["C:/My-old-pacs"],
         "TakeOwnership": false
       }
     }
   }

If you ingest new files in Orthanc through the DICOM protocol or the REST API, they will be stored in ``C:/Orthanc``.

REST API Extensions
-------------------

This plugin brings in a few new API routes:

**adopt-instance** to adopt an instance that is outside the storage. This is equivalent to the Indexer mode adopting an instance:

.. code-block:: bash

   $ curl http://localhost:8042/plugins/advanced-storage/adopt-instance -d @- << EOF
   {
     "Path": "/tmp/my-dicom-file.dcm",
     "TakeOwnership": false
   }
   EOF

**abandon-instance** to remove an adopted instance (if Orthanc is not the owner of the instance). This is equivalent to the Indexer mode abandoning an instance, e.g., the indexed file has been deleted:

.. code-block:: bash

   $ curl http://localhost:8042/plugins/advanced-storage/abandon-instance -d @- << EOF
   {
     "Path": "/tmp/my-dicom-file.dcm"
   }
   EOF

**move-storage** to move a resource from a storage to another one. Note: it does not recompute the relative path but only changes the base path (aka ``StorageId``):

.. code-block:: bash

   $ curl http://localhost:8042/plugins/advanced-storage/move-storage -d @- << EOF
   {
     "Resources": ["ca58b590-8a115ed5-906f7f21-c7af8058-2637f722"],
     "TargetStorageId": "ext2"
   }
   EOF

The plugin now provides extra information in the **../attachments/info** routes. For example:

.. code-block:: bash

   $ curl http://localhost:8042/instances/ca58b590-8a115ed5-906f7f21-c7af8058-2637f722/attachments/dicom/info

will return these new fields:

.. code-block:: json

   {
     "IsOwnedByOrthanc": true,
     "Path": "1234 - WHO^JOHN/20241102 - HEAD SCAN/100/000007-5f3936ea-95b6-4ad9-b0f1-4075be3e52d0.dcm",
     "StorageId": "ext1"
   }

The plugin also provides its status in this route **/plugins/advanced-storage/status**. For example:

.. code-block:: bash

   $ curl http://localhost:8042/plugins/advanced-storage/status

will return:

.. code-block:: json

   {
     "DelayedDeletionIsActive": true,
     "FilesPendingDeletion": 123,
     "IndexerIsActive": true
   }

Compilation
-----------

.. highlight:: bash

The procedure to compile this plugin is similar to that for the :ref:`core of Orthanc <binaries>`. The following commands should work for most UNIX-like distributions (including GNU/Linux):

.. code-block:: bash

   $ mkdir Build
   $ cd Build
   $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
   $ make

The compilation will produce a shared library ``AdvancedStorage`` that contains the plugin.
