.. _integrate-horos-using-dicom:

Integrate Horos using DICOM
===========================

Configuration of Horos
-----------------------

- In ``Preferences->Listener``, activate and configure AETitle and Port (e.g. Horos 11112).
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

