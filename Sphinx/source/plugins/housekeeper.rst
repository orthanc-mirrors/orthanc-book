.. _housekeeper-plugin:


Housekeeper plugin
==================

This page describes the **official sample plugin** that performs
housekeeping in the Database and Storage.

When changing some configuration or when upgrading Orthanc, it
might be usefull to perform housekeeping operations to optmize
the DB or clean/compress/uncompress the storage.  This can happen e.g:

* when changing the list of indexed :ref:`MainDicomTags <main-dicom-tags>`
* when changing the ``StorageCompression`` configuration
* when changing the ``IngestTranscoding`` configuration
* to remove unnecessary attachments like the ``dicom-as-json`` that were
  used in Orthanc prior to 1.9.1.
* when upgrading the :ref:`DICOMweb plugin <dicomweb>` from 1.14 to a later version.

Note that these housekeeping operations are not mandatory.  Orthanc will
continue to work without these cleanups.  However, running the plugin
might improve performances and storage usage.

The plugin detects any configuration changes that can trigger a cleanup
and will start process the studies one by one (in the order they have
been ingested in Orthanc).  If Orthanc is stopped and restarted, the plugin
will resume where it stopped.


Configuration
-------------

.. highlight:: json

Here's a sample configuration section for this plugin with its default values::

  {
    "Housekeeper": {

      // Enables/disables the plugin
      "Enable": false,

      // the Global Prooperty ID in which the plugin progress
      // is stored.  Must be > 1024 and must not be used by
      // another plugin
      "GlobalPropertyId": 1025,

      // Forces execution even if the plugin did not detect
      // any changes in configuration
      "Force": false,

      // Delay (in seconds) between reconstruction of 2 studies
      // This avoids overloading Orthanc with the housekeeping
      // process and leaves room for other operations.
      "ThrottleDelay": 5,

      // Runs the plugin only at certain period of time.
      // If not specified, the plugin runs all the time
      // Examples: 
      // to run between 0AM and 6AM everyday + every night 
      // from 8PM to 12PM and 24h a day on the weekend:
      // "Schedule": {
      //   "Monday": ["0-6", "20-24"],
      //   "Tuesday": ["0-6", "20-24"],
      //   "Wednesday": ["0-6", "20-24"],
      //   "Thursday": ["0-6", "20-24"],
      //   "Friday": ["0-6", "20-24"],
      //   "Saturday": ["0-24"],
      //   "Sunday": ["0-24"]
      // },

      // configure events that can trigger a housekeeping processing 
      "Triggers" : {
        "StorageCompressionChange": true,
        "MainDicomTagsChange": true,
        "UnnecessaryDicomAsJsonFiles": true,
        "IngestTranscodingChange": true,
        "DicomWebCacheChange": true   // new in 1.12.2
      }
    }
  }

Scheduling/throttling
---------------------

Processing a whole database/storage might take a very long time (days, weeks 
or even months) and can be I/O & CPU intensive.  Therefore, the configuration offers
options to schedule and/or throttle the housekeeping operations.  E.g, you can
run only the plugin during the night and week-end and, you can introduce a delay
between each processed study.

Triggers & internals
--------------------

By default, all triggers are enabled.  Depending on the detected change,
various operations will happen:

* if ``MainDicomTagsChange`` or ``UnnecessaryDicomAsJsonFiles`` is triggered, 
  the plugin will call the ``/studies/.../reconstruct`` route on every study 
  one by one.  Orthanc will read the DICOM tags from the DICOM files again and update 
  their value in the DB.

* if ``DicomWebCacheChange`` is triggered (this happens when upgrading from 
  the :ref:`DICOMweb plugin <dicomweb>` from 1.14 to a later version), the plugin will call the 
  ``/studies/../update-dicomweb-cache`` route on every study one by one.

* if any other change is detected, the plugin will again call the ``reconstruct`` route
  but, this time, with the ``ReconstructFiles`` option enabled.  Orthanc will then,
  read the DICOM file from the storage, compress/uncompress/transcode it and it will
  save it again to disk.  The new file will be stored using the new Storage settings 
  (``StorageCompression`` and ``IngestTranscoding``).
  Note that, Orthanc will create a new ``Attachment`` that will be saved at a different
  place as the previous one.


Status
------

You can get a progress status of the plugin by calling the ``/housekeeper/status`` API route.


Compilation
-----------

This plugin is part of the Orthanc core repository and is included in the Orthanc makefile.  
It is compiled with Orthanc itself and is distributed together with Orthanc binaries.



