.. _worklists-plugin:


Sample Modality Worklists plugin
================================

This page describes the **official sample plugin** turning Orthanc
into a server of DICOM worklists. General information about how
Orthanc supports DICOM worklists through plugins is explained in the
:ref:`FAQ <worklist>`.

The sample plugin will serve the worklists stored in some folder on
the filesystem. This mimics the behavior of the ``wlmscpfs``
command-line tool from the `DCMTK software
<http://support.dcmtk.org/docs/wlmscpfs.html>`__. 

The worklists to be served must be put inside the folder of interest
by an external application or script (note: files must have a ``.wl`` extension). ``dump2dcm`` might be a very
`useful companion tool
<http://support.dcmtk.org/docs/dump2dcm.html>`__ to generate such
worklist files. Whenever a C-Find SCP request is issued to Orthanc,
the plugin will read the content of the folder of interest to locate
the worklists that match the request. As a consequence, the external
application can dynamically modify the content of this folder while
Orthanc is running to add/remove worklists.

The source code of this sample plugin is `available in the source
distribution of Orthanc
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__
(GPLv3+ license).


Basic configuration
-------------------

.. highlight:: json

1. First, generate the :ref:`default configuration of Orthanc <configuration>`.
2. Then, modify the ``Plugins`` option to point to the folder containing
   the shared library of the plugin.
3. Finally, create a section "ModalityWorklists" in the configuration
   file to configure the worklist server.

A basic configuration would read as follows::

  {
    [...]
    "Plugins" : [ 
      "."
    ],
    "Worklists" : {
      "Enable": true,
      "Database": "./WorklistsDatabase",
      "FilterIssuerAet": false  // Some modalities do not specify 'ScheduledStationAETitle (0040,0001)'
                                // in the C-Find and may receive worklists not related to them.  This option 
                                // adds an extra filtering based on the AET of the modality issuing the C-Find.
    }
  }

The folder ``WorklistsDatabase`` of the `source distribution of
Orthanc
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__
contains a database of sample worklists, that comes from the DCMTK
source distribution, as described in the `FAQ entry #37 of the DCMTK
project <http://forum.dcmtk.org/viewtopic.php?t=84>`__.


Tutorial
--------

.. highlight:: javascript
 
- Download `DCMTK utilities
  <http://dicom.offis.de/download/dcmtk/release/bin/>`__.
- Download sample `worklist files
  <https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__
  from the Orthanc source code and copy them in a dedicated folder.
- Generate the :ref:`default configuration of Orthanc <configuration>`.
- Enable the ModalityWorklist plugin in your configuration file by adding this section::
  
    "Worklists" : {
      "Enable": true,
      "Database": "WorklistsDatabase"  // Path to the folder with the worklist files
    },

- Add the plugin to the list of plugins to load (this is an example
  for Microsoft Windows)::
  
    "Plugins" : [
      "OsimisWebViewer.dll",
      "ModalityWorklists.dll"   // On GNU/Linux, use libModalityWorklists.so
    ],

- The tests below will be done using the ``findscu`` command-line tool
  from the `DCMTK utilities
  <http://support.dcmtk.org/docs/findscu.html>`__. Assuming
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

- In another command-line prompt, launch a ``findscu`` request to ask
  Orthanc to return all worklists for ``CT`` modalities::

    findscu -W -k "ScheduledProcedureStepSequence[0].Modality=CT" 127.0.0.1 4242

  The ``-W`` option makes ``findscu`` issue a DICOM worklist query,
  the ``-k`` option specifies the query of interest, ``127.0.0.1``
  corresponds to the localhost, and ``4242`` corresponds to the
  default DICOM TCP port of Orthanc.

- ``findscu`` will display the matching worklists.


How to create a worklist file
-----------------------------

.. highlight:: bash
  
- Start with an existing worklist file, some samples of which can be
  found in the `Orthanc source distribution
  <https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/WorklistsDatabase/>`__
  (with ``.wl`` file extensions).
- The worklist file is a DICOM file. Dump its content as a text file
  using ``dcmdump``::

    dcmdump.exe wklist1.wl > sampleWorklist.txt
  
- The content of the just-generated ``sampleWorklist.txt`` file should
  look similar to this text file::

    # Dicom-File-Format
    
    # Dicom-Meta-Information-Header
    # Used TransferSyntax: Little Endian Explicit
    (0002,0000) UL 202                                      #   4, 1 FileMetaInformationGroupLength
    (0002,0001) OB 00\01                                    #   2, 1 FileMetaInformationVersion
    (0002,0002) UI [1.2.276.0.7230010.3.1.0.1]              #  26, 1 MediaStorageSOPClassUID
    (0002,0003) UI [1.2.276.0.7230010.3.1.4.2831176407.11154.1448031138.805061] #  58, 1 MediaStorageSOPInstanceUID
    (0002,0010) UI =LittleEndianExplicit                    #  20, 1 TransferSyntaxUID
    (0002,0012) UI [1.2.276.0.7230010.3.0.3.6.0]            #  28, 1 ImplementationClassUID
    (0002,0013) SH [OFFIS_DCMTK_360]                        #  16, 1 ImplementationVersionName
    
    # Dicom-Data-Set
    # Used TransferSyntax: Little Endian Explicit
    (0008,0005) CS [ISO_IR 100]                             #  10, 1 SpecificCharacterSet
    (0008,0050) SH [00000]                                  #   6, 1 AccessionNumber
    (0010,0010) PN [VIVALDI^ANTONIO]                        #  16, 1 PatientName
    (0010,0020) LO [AV35674]                                #   8, 1 PatientID
    (0010,0030) DA [16780304]                               #   8, 1 PatientBirthDate
    (0010,0040) CS [M]                                      #   2, 1 PatientSex
    (0010,2000) LO [METASTASIS]                             #  10, 1 MedicalAlerts
    (0010,2110) LO [TANTAL]                                 #   6, 1 Allergies
    (0020,000d) UI [1.2.276.0.7230010.3.2.101]              #  26, 1 StudyInstanceUID
    (0032,1032) PN [SMITH]                                  #   6, 1 RequestingPhysician
    (0032,1060) LO [EXAM6]                                  #   6, 1 RequestedProcedureDescription
    (0040,1001) SH [RP454G234]                              #  10, 1 RequestedProcedureID
    (0040,1003) SH [LOW]                                    #   4, 1 RequestedProcedurePriority
  
- Open ``sampleWorklist.txt`` file in a standard text editor so as to
  modify, add or remove some DICOM tags depending on your needs.
- Generate a new DICOM worklist file from your modified file using
  ``dump2dcm``::

    dump2dcm.exe sampleWorklist.txt newWorklist.wl
  
- As a last step, copy that file in the folder where Orthanc searches
  for its worklist files. Of course, this worklist generation workflow
  can be automated using any scripting language.

Troubleshooting C-Find queries
------------------------------

When trying to retrieve worklists from a modality, one usually don't get debugging capabilities from the modality itself.
Therefore, it is usually convenient to mimic the modality with ``findscu`` (provided by `DCMTK software
<http://support.dcmtk.org/docs/wlmscpfs.html>`__).  

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

- According to the `specification
  <http://dicom.nema.org/MEDICAL/Dicom/2015c/output/chtml/part02/sect_B.4.2.2.3.html>`__,
  modalities should not include their AET name in
  ``ScheduledStationAETitle`` on user initiated queries.  Therefore,
  they do receive worklists that do not concern them. This may be
  handled by the ``FilterIssuerAet`` configuration option. Note that
  this might in some cases be intended.

- Orthanc 1.2.0 does not handle the ``Generic group length`` tags.  
  You might need to include this kind of :ref:`lua script <lua-fix-cfind>` to remove these tags from the queries::
  
    function IncomingFindRequestFilter(query, origin)
      
      -- First display the content of the C-Find query
      PrintRecursive(query)
      PrintRecursive(origin)

      -- Remove the "Generic group length" tags from the query
      local v = query
      v['0008,0000'] = nil
      v['0010,0000'] = nil
      v['0020,0000'] = nil
      return v
    
    end
