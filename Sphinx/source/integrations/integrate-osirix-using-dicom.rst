.. _integrate-osirix-using-dicom:

Integrate Osirix using dicom
===========================

Configuration of Osirix
-----------------------

* In Preferences->Listener, activate and configure AETitle and Port (eg : Osirix 11112).
* In Preferences->Locations, add a DICOM Nodes :
    * with AETitle of orthanc (default is ORTHANC)
    * with a name (eg MYORTHANC)
    * with Retrieve method C-GET
    * with Send Transfers syntax : Explicit Little Endian

Configuration of Orthanc
------------------------

Add Modality through Environmental variable in docker::

  DICOM_MODALITIES=
  {
    "Osirix": ["Osirix", "192.168.253.53", 11112]
  }

If using Orthanc in a docker container, map the Orthanc DICOM Port. Eg in docker-compose file::

  ports:
    - "4242:4242"