.. highlight:: bash
.. _orthanc-dicom-origin:

How to find out where a DICOM instance originates from?
========================================================

Information about the origin of the instances is stored as Metadata, which can be accessed using the REST API::


    $ curl http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata
    [
    "IndexInSeries",
    "ReceptionDate",
    "RemoteAET",
    "Origin",
    "TransferSyntax",
    "SopClassUid",
    "RemoteIP",
    "CalledAET"
    ]


The relevant metadata about the origin of an instance is:

- ``Origin``: Whether the instance was received from the REST API, the DICOM protocol, some plugin or some Lua script.
- ``RemoteAET``: The remote AET (for DICOM).
- ``RemoteIP`` (in Orthanc ≥ 1.4.0): The IP address of the remote server (for REST API and DICOM).
- ``CalledAET`` (in Orthanc ≥ 1.4.0): The called AET (for DICOM).
- ``HttpUsername`` (in Orthanc ≥ 1.4.0): The username that created the instance (for REST API).

Please note that adding ``?expand`` to the REST endpoint will result in expanding the actual Metadata values::

    $ curl http://localhost:8042/instances/cab76369-429ce4d8-6ed415e7-7a3c9482-50f3b1b4/metadata?expand
    {
    "CalledAET" : "ORTHANCTMP1",
    "IndexInSeries" : "1",
    "Origin" : "DicomProtocol",
    "ReceptionDate" : "20190225T143257",
    "RemoteAET" : "ORTHANC",
    "RemoteIP" : "127.0.0.1",
    "SopClassUid" : "1.2.840.10008.5.1.4.1.1.1",
    "TransferSyntax" : "1.2.840.10008.1.2"
    }

