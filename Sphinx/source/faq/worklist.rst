Does Orthanc support worklists?
===============================

Orthanc supports DICOM Modality Worklists (MWL) through its `plugin
SDK
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__.
In other words, Orthanc can act as a worklist server (C-Find SCP), but
an user-defined plugin must be provided to answer a list of worklists
given a MWL query.

The rationale for using plugins instead of providing a built-in MWL
mechanism, is that the way worklists are generated is very specific to
the clinical flows and to the manufacturer of your `RIS system
<https://en.wikipedia.org/wiki/Radiology_information_system>`__.
Indeed, depending on the situation, worklists can be generated either
from HL7 messages, from calls to a Web service (e.g. through FHIR), or
from a direct access to some RIS database. It is thus up to the
Orthanc user to provide the worklist generator that is best suited for
her use.

A `sample plugin
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ModalityWorklists/>`__
is available to serve the worklists stored in some folder on the
filesystem. This mimics the behavior of the ``wlmscpfs`` command-line
tool from the `DCMTK software
<http://support.dcmtk.org/docs/wlmscpfs.html>`__. ``dump2dcm`` might
be a very `useful companion tool
<http://support.dcmtk.org/docs/dump2dcm.html>`__ to feed the sample
plugin with worklists for some separate maintenance script.

For more complex or integrated workflows where you must implement a
custom MWL plugin, please check the `documentation of the part of the
Orthanc plugin SDK
<https://orthanc.chu.ulg.ac.be/sdk/group__Worklists.html>`__ that is
related to the management of worklists.


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