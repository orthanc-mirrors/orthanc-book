.. _worklists-plugin:


Sample Modality Worklists plugin
================================

This page describes the **official sample plugin** turns Orthanc into
a server of DICOM worklists. The worklists must be provided in some
folder of the filesystem by an external script.

The source code of this sample plugin is `available in the source
distribution of Orthanc
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__
(GPLv3 license).  The plugin will serve the worklists stored in some
folder on the filesystem. This mimics the behavior of the ``wlmscpfs``
command-line tool from the `DCMTK software
<http://support.dcmtk.org/docs/wlmscpfs.html>`__. ``dump2dcm`` might
be a very `useful companion tool
<http://support.dcmtk.org/docs/dump2dcm.html>`__ to feed the sample
plugin with worklists for some separate maintenance script.

General information about the support of DICOM worklists in Orthanc is
explained in the :ref:`FAQ <worklist>`.



How should I use it ?
---------------------

- download `DCMTK utilities <http://dicom.offis.de/download/dcmtk/release/bin/>`__
- download sample `worklist files <https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__ from the Orthanc source code and copy them in a dedicated folder. 

.. highlight:: javascript
 
- Enable the ModalityWorklist plugin in your config.json by adding this section::
	
    "Worklists" : {
      "Enable": true,
      "Database": "WorklistsDatabase"  //this is the path to the folder with the worklist files.  Use absolute path !
    },

- Add the plugin to the list of plugins to load (this is an example for Windows)::
	
	"Plugins" : [
	  "OsimisWebViewer.dll",
	  "ModalityWorklists.dll" // on Linux, use ModalityWorklists.so
	],

- Add the findscu utility to the list of know modalities (considering findscu and Orthanc runs on the same machine)::
	
    "DicomModalities" : {
      "horos" : [ "HOROS", "192.168.0.8", 11112 ],
      "findscu" : [ "FINDSCU", "127.0.0.1", 1234 ]
    },

.. highlight:: bash
	
- Launch Orthanc as usual, make sure to pass him the configuration file (ex for Windows)::
	
	Orthanc.exe config.json

- In a prompt, launch a findscu request to ask Orthanc to return all Worklists for 'CT' modalities (considering findscu and Orthanc both runs on your machine: 127.0.0.1 is the Orthanc url and 4242 is the Orthanc DICOM port)::

    findscu -W -k "ScheduledProcedureStepSequence[0].Modality=CT" 127.0.0.1 4242

- findscu should display the matching worklists

How can I create worklist files ?
---------------------------------

- let's start from an existing `worklist file <https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__.

- dump the sample worklist file to a DCMTK dump file::

    dcmdump.exe wklist1.wl > sampleWorklist.txt
	
- you'll get something like::

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
    (0040,0100) SQ (Sequence with explicit length #=1)      # 176, 1 ScheduledProcedureStepSequence
      (fffe,e000) na (Item with explicit length #=12)         # 168, 1 Item
    	(0008,0060) CS [MR]                                     #   2, 1 Modality
    	(0032,1070) LO [BARIUMSULFAT]                           #  12, 1 RequestedContrastAgent
    	(0040,0001) AE [AA32\AA33]                              #  10, 2 ScheduledStationAETitle
    	(0040,0002) DA [19951015]                               #   8, 1 ScheduledProcedureStepStartDate
    	(0040,0003) TM [085607]                                 #   6, 1 ScheduledProcedureStepStartTime
    	(0040,0006) PN [JOHNSON]                                #   8, 1 ScheduledPerformingPhysicianName
    	(0040,0007) LO [EXAM74]                                 #   6, 1 ScheduledProcedureStepDescription
    	(0040,0009) SH [SPD3445]                                #   8, 1 ScheduledProcedureStepID
    	(0040,0010) SH [STN456]                                 #   6, 1 ScheduledStationName
    	(0040,0011) SH [B34F56]                                 #   6, 1 ScheduledProcedureStepLocation
    	(0040,0012) LO (no value available)                     #   0, 0 PreMedication
    	(0040,0400) LT (no value available)                     #   0, 0 CommentsOnTheScheduledProcedureStep
      (fffe,e00d) na (ItemDelimitationItem for re-encoding)   #   0, 0 ItemDelimitationItem
    (fffe,e0dd) na (SequenceDelimitationItem for re-encod.) #   0, 0 SequenceDelimitationItem
    (0040,1001) SH [RP454G234]                              #  10, 1 RequestedProcedureID
    (0040,1003) SH [LOW]                                    #   4, 1 RequestedProcedurePriority
	
	
- open sampleWorklist.txt file in a text editor and modify/add/remove some Dicom Tags

- then, generate a new worklist file with dump2dcm::

	dump2dcm.exe sampleWorklist.txt newWorklist.wl
	
- copy that file in the folder where Orthanc searches for its worklist files and that's it !

- of course, you'll automate this worklist generation workflow with some scripting language.
