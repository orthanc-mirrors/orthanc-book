Does Orthanc support worklists?
==============================

Orthanc partially supports the Dicom Modality Worklists (MWL) through
one of his `plugin <https://bitbucket.org/sjodogne/orthanc/src/Orthanc-1.0.0/Plugins/Samples/ModalityWorklists/>`__.

Thanks to this plugin, Orthanc can act as a worklist server (C-Find SCP)
and serve the worklists stored in a folder.  

However, Orthanc does not provide any functionality to generate the worklist files.
Usually, worklists are generated from HL7 messages or directly from a `RIS <https://en.wikipedia.org/wiki/Radiology_information_system>`__
database.  It's actually your responsibility to provide the worklist
generator.  `dump2dcm <http://support.dcmtk.org/docs/dump2dcm.html>`__ 
might be very useful in this task.

