.. _integrate-osirix-using-dicomweb:

Integrate Osirix using DICOMWeb
===============================

.. note:: The OsiriX team has a blog post entitled "`Installing
          Orthanc (Open-Source PACS) on Mac
          <https://www.osirix-viewer.com/installing-orthanc-open-source-pacs-on-mac/>`__"
          that provides a guide to interface OsiriX with Orthanc
          through :ref:`DICOMweb <dicomweb>`.


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
    "RemoteAccessAllowed" : true,
    "DicomWeb" : {
      "Enable" : true,
      "Root" : "/dicom-web/"
    }
  }



Configuration of Docker images by Orthanc Team
----------------------------------------------

This section applies if you are using the :ref:`orthancteam/orthanc Docker image <docker-orthancteam>`
to run Orthanc.

Make sure Orthanc has the Dicom Web protocol enabled::

  DICOM_WEB_PLUGIN_ENABLED: "true"

If using Orthanc in a docker container, map the Orthanc DICOMWeb Http Port. Eg in docker-compose file::

  ports:
    - "8042:8042"
