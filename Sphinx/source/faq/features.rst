Terminology of advanced features
================================

.. _peers:

Peers
-----

An "Orthanc peer" is another instance of Orthanc, possibly running on
a remote computer.

Contrarily to a "modality", it is possible to communicate with a peer
through the **HTTP/HTTPS protocol** (i.e. through the REST API of
Orthanc), and not through the DICOM protocol. This implies a much
easier configuration: It is only required to know the URL, the
username and the password to communicate with an Orthanc peer. This
contrasts with DICOM query/retrieve, that is quite complex and that
involves a lot of pitfalls (cf. the FAQ entry about :ref:`troubleshooting
DICOM communications <dicom>`) that can be bypassed if using HTTP.

Furthermore, as HTTP(S) communications are generally not blocked by
firewalls (contrarily to the DICOM protocol that is inherently an
Intranet protocol and that often requires the setup of VPN tunnels),
it is much easier to setup communications of medical images through
the Internet with Orthanc peers.


.. _recycling:

Recycling/Protection
--------------------

Because of its focus on low-end computers, Orthanc implements **disk
space recycling**: The patient that has been stored for the longest
time inside Orthanc can be automatically deleted when the disk space
used by Orthanc grows above a threshold, or when the number of stored
patients grows above a threshold. This feature enables the automated
control of the disk space dedicated to Orthanc.

Recycling is controlled by the ``MaximumStorageSize`` and the
``MaximumPatientCount`` options in the :ref:`Orthanc configuration
file <configuration>`.

It is possible to prevent important data from being automatically
recycled. This mechanism is called **protection**. Each patient can be
individually protected against recycling by using the
``Unprotected/Protected`` switch that is available from Orthanc
Explorer.

Note that protection is only available at the patient level. It
protects all the studies/series/instances of the patient against
recycling. The rationale is that we think it is important to keep
available all the data related to one patient. Unwillingly losing a
study/series that is part of the same patient might lead to a loss in
consistency with respect to the medical history of this patient.


.. _compression:

Compression
-----------

If your disk space is limited, besides :ref:`recycling`, you should
also consider using **disk space compression**. When compression is
enabled, Orthanc compresses the incoming DICOM instances on-the-fly
before writing them to the filesystem, using `zlib
<https://en.wikipedia.org/wiki/Zlib>`_. This is useful, because the
images are often stored as raw, uncompressed arrays in DICOM
instances: The size of a typical DICOM instance can hopefully be
divided by a factor 2 through lossless compression. This compression
process is transparent to the user, as Orthanc automatically
decompresses the file before sending it back to the external world.

Compression is controlled by the ``StorageCompression`` option in the
:ref:`Orthanc configuration file <configuration>`.
