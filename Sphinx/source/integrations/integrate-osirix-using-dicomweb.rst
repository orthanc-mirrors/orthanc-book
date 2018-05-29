.. _integrate-osirix-using-dicomweb:

Integrate Osirix using DICOMWeb
===============================

Configuration of Osirix
-----------------------

* In Preferences->Listener, activate and configure AETitle and Port (eg : Osirix 11112)
* In Preferences->Locations->DICOMWeb Node, add a DICOM Nodes :
    * with the url of the orthanc server
    * with the DicomWeb api path of orthanc (default is /dicom-web)
    * with a name (eg MYORTHANC)
    * with Q&R activated
    * without authentication
    * with Send Transfers syntax : Explicit Little Endian

Configuration of Orthanc
------------------------

Make sure Orthanc has the Dicom Web protocol enabled::

  DW_ENABLED: "true"

If using Orthanc in a docker container, map the Orthanc DICOMWeb Http Port. Eg in docker-compose file::

  ports:
    - "4242:4242"