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


.. _metadata:

Metadata
--------

Metadata consists in an **associative key-value array** (mapping a
integer key in the range [0,65535] to a string value) that is
associated with each :ref:`DICOM resource <orthanc-ids>` stored inside
Orthanc (may it be a patient, a study, a series or a DICOM
instance). Metadata can be either referred to using the integer key,
or using a symbolic name (if configured).  Metadata records
information that is not readily available in the DICOM tags.

In spirit, the metadata mechanism is similar to the :ref:`attachment
mechanism <orthanc-storage>`. However, metadata is stored directly
inside the database, whereas attachments are stored as separate files
on the filesystem (the database only stores a reference to the
attachments). Choosing between metadata and attachments is a matter of
trade-off: Metadata must be kept small (as a rule of thumb, under 1KB)
and used if fast access is needed, whereas attachments can be used to
store arbitrarily large piece of data.

Also note that metadata and attachments are only available for
resources stored inside Orthanc. Once one DICOM instance leaves the
Orthanc ecosystem, its associated metadata and attachments are lost.


Core metadata
^^^^^^^^^^^^^

Here are the main metadata handled by the Orthanc core:

* ``ReceptionDate`` records when a DICOM instance was received by
  Orthanc. Similarly, ``LastUpdate`` records, for each
  patient/study/series, the last time a DICOM instance was added to
  this resource.
* ``RemoteAet`` records the AET of the modality that has sent some
  DICOM instance to Orthanc.
* ``ModifiedFrom`` and ``AnonymizedFrom`` hold from which original
  resource, a resource was modified or anonymized. The presence of
  this metadata indicates that the resource is the result of a
  modification or anonymization that was carried on by Orthanc.
* ``Origin`` records through which mechanism the instance was received
  by Orthanc (may be ``Unknown``, ``DicomProtocol``, ``RestApi``,
  ``Plugins``, or ``Lua``).
* ``IndexInSeries`` records the expected index of a DICOM instance
  inside its parent series. Conversely, ``ExpectedNumberOfInstances``
  associates to each series, the number of DICOM instances this series
  is expected to contain.
* Starting with Orthanc 1.2.0, ``TransferSyntax`` and ``SopClassUid``
  respectively stores the transfer syntax UID and the SOP class UID of
  DICOM instances, in order to speed up the access to this
  information.

Metadata listed above are set privately by the Orthanc core. They are
**read-only** from the perspective of the end user, as Orthanc
internally relies on them.


User-defined metadata
^^^^^^^^^^^^^^^^^^^^^

The metadata described above where handled by the core of Orthanc.
Orthanc users are however allowed to define their own **user-defined
metadata**. Such metadata are associated with an integer key that is
greater or equal to 1024 (whereas keys below 1023 are reserved for
core metadata).

You can associate a symbolic name to user-defined metadata using the
``UserMetadata`` option inside the :ref:`configuration of Orthanc
<configuration>`.


Accessing metadata
^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Metadata associated with one DICOM resource can be accessed through
the :ref:`REST API <rest>`, for instance::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/RemoteAet

User-defined metadata can be modified by issuing a HTTP PUT against
the REST API::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/1024 -X PUT -d 'hello'
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/1024
  hello



.. _registry:

Central registry of metadata and attachments
--------------------------------------------

Obviously, one must pay attention to the fact that different
applications might use the same key to store different user-defined
:ref:`metadata <metadata>`, which might result in incompatibilities
between such applications. Similarly, incompatibilities might show up
for user-defined :ref:`attachments <orthanc-storage>`.

Developers of applications/plugins that use user-defined metadata or
attachments are therefore kindly invited to complete the **central
registry** below:

* ``Metadata 4200`` is used by the plugin for :ref:`whole-slide imaging <wsi>`.
