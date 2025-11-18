.. _worklists-plugin-new:


Worklists plugin
================

.. warning:: 
  This page documents the new ``Worklists plugin`` that supersedes the
  legacy :ref:`Sample Modality Worklists plugin <worklists-plugin>` that is
  provided as a sample project with the Orthanc source code since 1.0.0.

.. contents::

The worklists plugin turns Orthanc
into a server of DICOM worklists. General information about how
Orthanc supports DICOM worklists through plugins is explained in the
:ref:`FAQ <worklist>`.

The plugin serves the worklists stored in some folder on the filesystem 
or directly in the Orthanc database.  It also provides a REST API to create and manage 
worklists.

The source code of this plugin is `available on GitHub
<https://github.com/orthanc-server/orthanc-worklists>`__
(AGPLv3+ license).

Basic configuration
-------------------

.. highlight:: json

1. First, generate the :ref:`default configuration of Orthanc <configuration>`.
2. Then, modify the ``Plugins`` option to point to the folder containing
   the shared library of the plugin.
3. Finally, create a section "Worklists" in the configuration
   file to configure the worklist server.

A basic configuration would read as follows::

  {
    [...]
    "Plugins" : [ 
      "."
    ],
    "Worklists" : {
      "Enable": true,

      "FilterIssuerAet": false, // Some modalities do not specify 'ScheduledStationAETitle (0040,0001)'
                                // in the C-Find and may receive worklists not related to them.  This option 
                                // adds an extra filtering based on the AET of the modality issuing the C-Find.
      "LimitAnswers": 0,        // Maximum number of answers to be returned (new in release 1.7.3)

      "Directory": "./WorklistsDatabase",  // The folder from which worklists are read or in which they are created.
      

      "SaveInOrthancDatabase": false,      // If set to true and if the Orthanc Database supports Key-Value stores
                                           // (PostgreSQL or SQLite), the worklists must be created through the REST API
                                           // and are stored in the Orthanc DB.
      "SetStudyInstanceUidIfMissing": true,  // Add a StudyInstanceUID to the worklist if none is provided in the REST API call to create it
      "DeleteWorklistsOnStableStudy": true,   // Delete the worklist as soon as a a stable study is found with the StudyInstanceUID
                                              // provided in the worklist.  
                                              // Note that this check is performed in the Worklist Housekeeper thread.  The plugin
                                              // does not react synchronously on the Stable Study event.
                                              // This process is only available if you are providing a StudyInstanceUID
                                              // or if you have set the 'SetStudyInstanceUIDIfMissing' configuration to true
      "HousekeepingInterval": 60,             // Interval [in seconds] between 2 execution of the Worklist Housekeeper thread.

      // New options only if SaveInOrthancDatabase is set to true.
      
      "DeleteWorklistsDelay": 24          // Delay [in hours] after which the worklist is deleted.
                                          // Note that this check is performed in the Worklist Housekeeper thread.
                                          // The plugin only deletes worklists that have been created through the REST API.
                                          // Set it to 0 if you don't want the plugin to delete worklists after a delay.
    }
  }


Tutorial
--------

.. highlight:: javascript
 
- Download `DCMTK utilities
  <https://dicom.offis.de/download/dcmtk/release/bin/>`__.
- Enable the Worklists plugin in your configuration file by adding this section::
  
    "Worklists" : {
      "Enable": true,
      "SaveInOrthancDatabase": true
    },

- Add the plugin to the list of plugins to load (this is an example
  for Microsoft Windows)::
  
    "Plugins" : [
      "StoneWebViewer.dll",
      "OrthancExplorer2.dll",
      "OrthancWorklists.dll"   // On GNU/Linux, use libOrthancWorklists.so
    ],

- The tests below will be done using the ``findscu`` command-line tool
  from the `DCMTK utilities
  <https://support.dcmtk.org/docs/findscu.html>`__. Assuming
  ``findscu`` and Orthanc runs on the same computer (i.e. on the
  ``127.0.0.1`` localhost), declare the ``FINDSCU`` AET to the list of
  know modalities::
  
    "DicomModalities" : {
      "horos" : [ "HOROS", "192.168.0.8", 11112 ],
      "findscu" : [ "FINDSCU", "127.0.0.1", 1234 ]
    },

.. highlight:: bash
  
- Launch Orthanc as usual, making sure to give the proper
  configuration file (e.g. for Microsoft Windows)::
  
    Orthanc.exe config.json

- Open the `Orthanc Explorer 2 User interface <http://localhost:8042/ui/app/>`__
  and create a worklist for a ``CT``.

- In another command-line prompt, launch a ``findscu`` request to ask
  Orthanc to return all worklists for ``CT`` modalities::

    findscu -W -k "ScheduledProcedureStepSequence[0].Modality=CT" 127.0.0.1 4242

  The ``-W`` option makes ``findscu`` issue a DICOM worklist query,
  the ``-k`` option specifies the query of interest, ``127.0.0.1``
  corresponds to the localhost, and ``4242`` corresponds to the
  default DICOM TCP port of Orthanc.

- ``findscu`` will display the matching worklists.


How to create a worklist using the REST API
-------------------------------------------

.. highlight:: bash

The new worklsits plugin provides a REST API that can be
used to create worklists.  For example::

  $ curl --request POST http://localhost:8042/worklists/create \
      --data '{
                "Tags" : {
                  "PatientID": "PID-45",
                  "PatientName": "Toto",
                  "ScheduledProcedureStepSequence" : [
                    {
                      "Modality": "US",
                      "ScheduledProcedureStepStartDate": "20251014",
                      "ScheduledProcedureStepDescription": "Description"
                    }
                  ]
                }
              }'

In response, you'll get something like::
  
  {
    "ID" : "5fdc7404-f9dc-4798-b6e1-8f715e2f9e71",
    "Path" : "/worklists/5fdc7404-f9dc-4798-b6e1-8f715e2f9e71"
  }

You can then check the content of the worklist by calling::

  $ curl --request GET http://localhost:8042/worklists/5fdc7404-f9dc-4798-b6e1-8f715e2f9e71

To delete it, call::

  $ curl --request DELETE http://localhost:8042/worklists/5fdc7404-f9dc-4798-b6e1-8f715e2f9e71

To browse all worklists, call::

  $ curl --request GET http://localhost:8042/worklists/?format=Simplify
  $ curl --request GET http://localhost:8042/worklists/?format=Short
  $ curl --request GET http://localhost:8042/worklists/?format=Full



Troubleshooting C-Find queries
------------------------------

When trying to retrieve worklists from a modality, one usually don't get debugging capabilities from the modality itself.
Therefore, it is usually convenient to mimic the modality with ``findscu`` (provided by `DCMTK software
<https://support.dcmtk.org/docs/wlmscpfs.html>`__).  

- First, you should make sure that you have configured the Worklist plugin correctly and that you have pushed
  at least a ``.wl`` file in the worklist database.  For this, you should issue this kind of command::

    findscu -W 127.0.0.1 4242 -k 0008,0050="*"

  This is the most generic C-Find request and should return all AccessionNumber of all the worklists in your database.

  Note: you should make sure you have added a ``findscu`` DICOM modality in your configuration file.

  ``findscu`` should output something like this::
  
    W: ---------------------------
    W: Find Response: 1 (Pending)
    W:
    W: # Dicom-Data-Set
    W: # Used TransferSyntax: Little Endian Explicit
    W: (0008,0005) CS [ISO_IR 100]                             #  10, 1 SpecificCharacterSet
    W: (0008,0050) SH [**********]                             #  10, 1 AccessionNumber
    W:

  If you don't get any output, you may add ``-v -d`` options to the ``findscu`` command line to get additional details.

- Everytime it receives a C-Find request, Orthanc displays the query parameters in its :ref:`logs <log>`.
  With the previous C-Find command, you should expect this kind of output::

    I0422 17:16:03.512449 CommandDispatcher.cpp:490] Association Received from AET FINDSCU on IP 127.0.0.1
    I0422 17:16:03.514433 CommandDispatcher.cpp:688] Association Acknowledged (Max Send PDV: 16372)
    I0422 17:16:03.532062 main.cpp:118] No limit on the number of C-FIND results at the Patient, Study and Series levels
    I0422 17:16:03.535986 main.cpp:128] No limit on the number of C-FIND results at the Instance level
    I0422 17:16:03.536968 PluginsManager.cpp:171] Received worklist query from remote modality FINDSCU:
    {
       "0008,0050" : "*"
    }
    I0422 17:16:03.559539 CommandDispatcher.cpp:891] DUL Peer Requested Release
    I0422 17:16:03.560520 CommandDispatcher.cpp:898] Association Release

- Now you may try to issue a C-Find request from your modality and check Orthanc logs.  You should then have a better understanding of the query
  content and eventually understand why it does not match your worklists.  You should also be able re-issue ``findscu`` requests with additional arguments to mimic the requests issued by your modality.

Common problems
---------------

- C-FIND requests can be modified by implementing the
  ``IncomingWorklistRequestFilter`` :ref:`Lua callback
  <lua-fix-cfind>` since Orthanc 1.4.2. This can be useful to
  fix/sanitize worklist queries.

- According to the `specification
  <http://dicom.nema.org/MEDICAL/Dicom/2015c/output/chtml/part02/sect_B.4.2.2.3.html>`__,
  modalities should not include their AET name in
  ``ScheduledStationAETitle`` on user initiated queries.  Therefore,
  they do receive worklists that do not concern them. This may be
  handled by the ``FilterIssuerAet`` configuration option. Note that
  the default behavior might in some cases be intended.
