.. _integrate-osirix-using-dicom:

Integrate Osirix using DICOM
============================

Configuration of Osirix
-----------------------

- In ``Preferences->Listener``, activate and configure AETitle and Port (e.g. Osirix 11112).
- In ``Preferences->Locations``, add a DICOM Node:

  - with the AET of your Orthanc instance (default is ``ORTHANC``)
  - with a name (eg ``MYORTHANC``)
  - with Retrieve method C-GET
  - with Send Transfers syntax : Explicit Little Endian


Configuration of Orthanc
------------------------

Add the following :ref:`configuration options <configuration>`
(obviously, adapt the IP address)::

  {
    "DicomModalities" : {
      "Horos": [ "Horos", "192.168.253.53", 11112 ]
    }
  }


Configuration of Docker images by Orthanc Team
----------------------------------------------

This section applies if using the :ref:`Docker images by Orthanc Team
<docker-orthancteam>` to run Orthanc.

Add Modality through Environmental variable in docker::

  DICOM_MODALITIES=
  {
    "Osirix": ["Osirix", "192.168.253.53", 11112]
  }

If using Orthanc in a docker container, map the Orthanc DICOM Port. Eg in docker-compose file::

  ports:
    - "4242:4242"
