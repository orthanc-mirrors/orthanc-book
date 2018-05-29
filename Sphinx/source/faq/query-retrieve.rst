.. _query-retrieve:

Configuring DICOM Query/Retrieve
================================

Starting with release 0.7.0, Orthanc supports DICOM Query/Retrieve
(i.e. Orthanc can act as C-Find SCP and C-Move SCP). To configure this
feature, follow these instructions:

* Get the AET (Application Entity Title), the IP address and the port
  number of your DICOM client.
* Add an entry in the ``DicomModalities`` section of your Orthanc
  :ref:`configuration file <configuration>` to reflect these settings.
* Restart Orthanc with the updated configuration file.
* Symmetrically, in your DICOM client, configure an additional DICOM
  node corresponding to your Orthanc AET (see the ``DicomAet``
  parameter of your Orthanc configuration, by default, ORTHANC), IP
  address et port number (cf. ``DicomPort``, by default 4242).

If you encounter configuration problem with query/retrieve, please be
sure to read the :ref:`dicom-move` section.

For examples specific to well-known applications, check out the
:ref:`integrations` section.
