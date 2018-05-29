.. _integrate-osirix-using-dicomweb:

Integrate Osirix using DICOMWeb
===============================

Configuration of Osirix
-----------------------

- In ``Preferences->Listener``, activate and configure AETitle and Port (e.g. Osirix 11112)
- In ``Preferences->Locations->DICOMWeb Node``, add a DICOM Node:

  - with the URL of the Orthanc server
  - with the DICOMweb API path of Orthanc (default is ``/dicom-web``)
  - with a name (eg ``MYORTHANC``)
  - with Q&R activated
  - without authentication
  - with Send Transfers syntax : Explicit Little Endian


Configuration of Orthanc
------------------------

First, make sure to :ref:`install and enable the DICOMweb plugin <dicomweb>`.

Adapt the following :ref:`configuration options <configuration>`
(obviously, adapt the IP address)::

  {
    "Plugins" : [ /* fill the path to the DICOMweb plugin */ ],
    "RemoteAccessEnabled" : true,
    "DicomWeb" : {
      "Enable" : true,
      "Root" : "/dicom-web/"
    }
  }



Configuration of Docker images by Osimis
----------------------------------------

This section applies if you are using the `Docker images by Osimis
<https://osimis.atlassian.net/wiki/spaces/OKB/pages/26738689/How+to+use+osimis+orthanc+Docker+images>`__
to run Orthanc.

Make sure Orthanc has the Dicom Web protocol enabled::

  DW_ENABLED: "true"

If using Orthanc in a docker container, map the Orthanc DICOMWeb Http Port. Eg in docker-compose file::

  ports:
    - "4242:4242"
