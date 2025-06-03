Terminology of advanced features
================================

.. contents::
   :depth: 3

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
the Internet with :ref:`Orthanc peers <peering>`.


.. _recycling:

Recycling/Protection
--------------------

Because of its focus on low-end computers, Orthanc may implement **disk
space recycling**: The patient that has been stored for the longest
time inside Orthanc can be automatically deleted when the disk space
used by Orthanc grows above a threshold, or when the number of stored
patients grows above a threshold. This feature enables the automated
control of the disk space dedicated to Orthanc.  Note that each time
a new instance is received for an existing patient, the patient will
be marked as the most recent one in the recycling order.

Recycling is controlled by the ``MaximumStorageSize`` and the
``MaximumPatientCount`` options in the :ref:`Orthanc configuration
file <configuration>`.  Setting both these values to 0 will disable 
recycling.

Starting with version 1.11.2, Orthanc also implements another **rejection**
behaviour when the ``MaximumStorageSize`` or ``MaximumPatientCount`` is 
reached.  In this case, patients are not recycled but Orthanc rejects new incoming
data.  Check the ``MaximumStorageMode`` option in the :ref:`Orthanc configuration
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

To protect/unprotect a patient, one must call the ``/patients/../protected`` route:: 

$ curl -X PUT http://localhost:8042/patients/0946fcb6-cf12ab43-bad958c1-bf057ad5-0fc6f54c/protected -d "1"
$ curl -X PUT http://localhost:8042/patients/0946fcb6-cf12ab43-bad958c1-bf057ad5-0fc6f54c/protected -d "0"


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

Note that the Orthanc distribution comes with the
``OrthancRecoverCompressedFile`` command-line tool if a system
administrator needs to recover one attachment compressed by Orthanc.


.. _metadata:

Metadata & attachments
----------------------

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
attachments). Choosing between metadata and attachments is most often
a matter of trade-off: Metadata must be kept small (as a rule of
thumb, under 1KB) and used if fast access is needed, whereas
attachments can be used to store arbitrarily large piece of data.

However, pay attention to the fact that metadata must be UTF-8 strings
terminated by the ``\0`` character. If you need to store arbitrary
binary objects, use an attachment or use `Base64 encoding
<https://en.wikipedia.org/wiki/Base64>`__.

Also note that metadata and attachments are only available for
resources stored inside Orthanc. Once one DICOM instance leaves the
Orthanc ecosystem, its associated metadata and attachments are lost.

.. _metadata-core:

Core metadata
^^^^^^^^^^^^^

Here are the main metadata handled by the Orthanc core:

* ``ReceptionDate`` records when a DICOM instance was received by
  Orthanc. Similarly, ``LastUpdate`` records, for each
  patient/study/series, the last time a DICOM instance was added to
  this resource.  Starting with Orthanc 1.12.1, ``LastUpdate`` is also
  updated when a child resource is deleted.
* ``RemoteAET`` records the AET of the modality that has sent some
  DICOM instance to Orthanc using the DICOM protocol. This metadata is
  only available at the level of DICOM instances, as the instances of
  a patient/study/series can possibly originate from different
  modalities.
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
  is expected to contain. This information is :ref:`not always
  available <series-completion>`.
* Starting with Orthanc 1.2.0, ``TransferSyntax`` and ``SopClassUid``
  respectively stores the `transfer syntax UID
  <http://dicom.nema.org/medical/dicom/current/output/html/part05.html#chapter_10>`__
  and the `SOP class UID
  <http://dicom.nema.org/medical/dicom/current/output/chtml/part02/sect_A.1.html>`__
  of DICOM instances, in order to speed up the access to this
  information.
* ``RemoteIP`` (new in Orthanc 1.4.0): The IP address of the remote
  SCU (for REST API and DICOM protocol).
* ``CalledAET`` (new in Orthanc 1.4.0): The AET that was called by the
  SCU, which normally matches the AET of Orthanc (for DICOM protocol).
* ``HttpUsername`` (new in Orthanc 1.4.0): The username that created
  the instance (for REST API).
* ``PixelDataOffset`` (new in Orthanc 1.9.1): Offset (in bytes) of the
  Pixel Data DICOM tag in the DICOM file, if available.
* ``MainDicomTagsSignature`` (new in Orthanc 1.11.0):
  The list of :ref:`MainDicomTags <main-dicom-tags>` that have been
  saved in DB for this resource.

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
<configuration>`::

  "UserMetadata" : {
    "SampleMetaData1" : 1024,
    "SampleMetaData2" : 1025
  }


Accessing metadata
^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Metadata associated with one DICOM resource can be accessed through
the :ref:`REST API <rest>`, for instance::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata?expand
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/RemoteAet
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/SampleMetaData1

User-defined metadata can be modified by issuing a HTTP PUT against
the REST API::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/1024 -X PUT -d 'hello'
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/metadata/1024
  hello



.. _attachments:

User-defined attachments
^^^^^^^^^^^^^^^^^^^^^^^^

Orthanc users are allowed to define their own **user-defined attachments**.
Such attachments are associated with an integer key that is
greater or equal to 1024 (whereas keys below 1023 are reserved for
core attachments).

You can associate a symbolic name to user-defined attachments using the
``UserContentType`` option inside the :ref:`configuration of Orthanc
<configuration>`.  Optionally, the user may specify a MIME content type
for the attachment::

  "UserContentType" : {
    "samplePdf" : [1024, "application/pdf"],
    "sampleJson" : [1025, "application/json"],
    "sampleRaw" : 1026
  }

Accessing attachments
^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Attachments associated with one DICOM resource can be accessed through
the :ref:`REST API <rest>`, for instance::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/attachments/samplePdf/data
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/attachments/sampleJson/data

User-defined attachments can be modified by issuing a HTTP PUT against
the REST API::

  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/attachments/samplePdf -X PUT --data-binary @sample.pdf
  $ curl http://localhost:8042/instances/cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e/attachments/sampleRaw -X PUT -d 'raw data'


DICOM-as-JSON attachments
^^^^^^^^^^^^^^^^^^^^^^^^^

In the version of Orthanc <= 1.9.0, whenever Orthanc receives a DICOM
file, it pre-computes a JSON summary of its DICOM tags, and caches
this JSON file as an attachment to the DICOM instance (accessible at
the ``/instances/{...}/attachments/dicom-as-json/`` URI). This
attachment is used as a cache to speed up future accesses to
``/instances/.../tags``, lookups using ``/tools/find`` or C-FIND
queries.

This caching might cause issues if the dictionary of DICOM tags is
subsequently modified, which implies that the cached JSON file does
not perfectly match the new dictionary.

.. highlight:: bash

Since Orthanc 1.2.0, you can force the re-generation of the cached
JSON file by DELETE-ing it, for instance::

  $ curl -X DELETE http://localhost:8042/instances/301896f2-1416807b-3e05dcce-ff4ce9bb-a6138832/attachments/dicom-as-json

.. highlight:: text

The next time you open this particular instance with Orthanc Explorer,
you will see messages in the Orthanc logs (in verbose mode) stating
that the Orthanc server has reconstructed the JSON summary, which will
match the new content of the dictionary::

  I0222 08:56:00.923070 FilesystemStorage.cpp:155] Reading attachment "2309c47b-1cbd-4601-89b5-1be1ad80382c" of "DICOM" content type
  I0222 08:56:00.923394 ServerContext.cpp:401] Reconstructing the missing DICOM-as-JSON summary for instance: 301896f2-1416807b-3e05dcce-ff4ce9bb-a6138832
  I0222 08:56:00.929117 ServerContext.cpp:540] Adding attachment dicom-as-json to resource 301896f2-1416807b-3e05dcce-ff4ce9bb-a6138832
  I0222 08:56:00.929425 FilesystemStorage.cpp:118] Creating attachment "3c830b66-8a00-42f0-aa3a-5e37b4a8b5a4" of "JSON summary of DICOM" type (size: 1MB)

These DICOM-as-JSON attachments are not automatically generated
anymore starting with Orthanc 1.9.1.  They can possibly be removed 
by the :ref:`Housekeeper plugin <housekeeper-plugin>` to reclaim disk space.

.. _registry:

Central registry of metadata and attachments
--------------------------------------------

Obviously, one must pay attention to the fact that different
applications might use the same key to store different user-defined
:ref:`metadata <metadata>`, which might result in incompatibilities
between such applications. Similarly, incompatibilities might show up
for user-defined :ref:`attachments <orthanc-storage>`.

Developers of applications/plugins that use user-defined metadata,
attachments or global properties (using
``OrthancPluginSetGlobalProperty()``) are therefore kindly invited to
complete the **central registry** below:

* ``Attachment 1`` is used by the core of Orthanc to store the DICOM
  file associated with one instance.
* ``Attachment 2`` was used by Orthanc <= 1.9.0 to cache the so-called
  ``DICOM-as-JSON`` information (as returned by the
  ``/instances/.../tags`` URI in the :ref:`REST API <rest>`) in order
  to speed up subsequent requests to the same URI. This attachment is
  not automatically generated anymore starting with Orthanc 1.9.1, in
  order to improve performance (creating two files for each DICOM
  instance has a cost) and consistency (if the DICOM dictionary gets
  modified in the future).
* ``Attachment 3`` is used since Orthanc 1.9.1 to store the DICOM
  instance until the ``Pixel Data (7fe0,0010)`` tag, if the global
  configuration option ``StorageCompression`` is ``true``, or if the
  storage area plugin doesn't support range reads. This allows to
  avoid downloading the full DICOM instance if not necessary.
* ``Attachment 4301`` is used by the :ref:`DICOMweb plugin <dicomweb>` to cache WADO-RS series metadata (starting from v 1.15 of the plugin).
* ``Attachment 9997`` is used by the :ref:`Osimis WebViewer plugin <osimis_webviewer>` to store series information.
* ``Attachment 9998`` is used by the :ref:`Osimis WebViewer plugin <osimis_webviewer>` to store instance information.
* ``Attachment 9999`` is used by the :ref:`Osimis WebViewer plugin <osimis_webviewer>` to store annotations.
* ``Attachments 10000-13999`` are used by the :ref:`Osimis WebViewer plugin <osimis_webviewer>` to store reduced quality images.
* ``Global property 1025`` is used by default by the Housekeeper plugin.
* ``Global property 5467`` is used by the Osimis Cloud plugin.
* ``Global property 5468`` is used by the :ref:`DICOMweb plugin <dicomweb>` to store the DICOMweb servers into the Orthanc database.
* ``Metadata 4200`` is used by the plugin for :ref:`whole-slide imaging <wsi>` with version <= 0.7.
* ``Metadata 4201`` is used by the plugin for :ref:`whole-slide imaging <wsi>` with version >= 1.0.
* ``Metadata 4202`` is used by the :ref:`OHIF plugin <ohif>` to store precomputed information about the DICOM instances.


Jobs
----

Check out the :ref:`advanced features of the REST API <jobs>`.



.. _stable-resources:

Stable resources
----------------

A DICOM resource (patient, study or series) is referred to as
**stable** if it has not received any new instance for a certain
amount of time.

This amount of time is configured by the the option ``StableAge`` in
the :ref:`configuration file <configuration>`.

When some resource becomes stable, an event is generated as a log
entry in the ``/changes`` :ref:`URI in the REST API <changes>`, a
:ref:`Lua callback <lua-callbacks>` is invoked, the callback function
registered by ``OrthancPluginRegisterOnChangeCallback()`` in
:ref:`C/C++ plugins <creating-plugins>` is executed, as well as the
:ref:`Python callback <python-changes>` registered by
``orthanc.RegisterOnChangeCallback()``.

The ``IsStable`` field is also available to get the status of an
individual patient/study/series using the REST API of Orthanc.

In the multiple readers/writers scenario enabled since Orthanc 1.9.2,
each Orthanc server is considered separately: The "stable" information
is monitored by threads inside the Orthanc process, and is **not**
shared in the database. In other words, the "stable" information is
local to the Orthanc server that is queried.  Synchronization between
multiple readers/writers must be implemented at a higher level
(e.g. using a distributed `message-broker system
<https://en.wikipedia.org/wiki/Message_broker>`__ such as RabbitMQ
that is fed by an Orthanc plugin).


.. _revisions:

Revisions
---------

.. highlight:: bash

Higher-level applications built on the top of Orthanc might have to
modify metadata and/or attachments. This can cause concurrency
problems if multiple clients modify the same metadata/attachment
simultaneously. To avoid such problems, Orthanc implements a so-called
**revision mechanism** to protect from concurrent modifications.

The revision mechanism is optional, was introduced in **Orthanc
1.9.2** and must be enabled by setting :ref:`configuration option
<configuration>` ``CheckRevisions`` to ``true``. It is strongly
inspired by the `CouchDB API
<https://docs.couchdb.org/en/stable/api/document/common.html>`__.

When the revision mechanism is enabled, each metadata and attachment
is associated with a **revision number**. Whenever one sets a metadata
for the first time using a ``PUT`` query, this revision number can be
found in the HTTP header ``ETag`` that is reported by Orthanc::

  $ curl -v http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata/1024 -X PUT -d 'Hello'
  [...]
  < ETag: "0"

Any ``GET`` query will also return the current value of ``ETag``::
  
  $ curl -v http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata/1024
  [...]
  < ETag: "0"

If one needs to subsequently modify or delete this metadata, the HTTP
client must set this value of ``ETag`` into the ``If-Match`` HTTP
header::

  $ curl -v http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata/1024 -X PUT -d 'Hello 2' -H 'If-Match: "0"'
  [...]
  < ETag: "1"

Note how this second call has incremented the value of ``ETag``: This
is the new revision number to be used in future updates. If a bad
revision number is provided, the HTTP error ``409 Conflict`` is
generated::

  $ curl -v http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata/1024 -X PUT -d 'Hello 3' -H 'If-Match: "0"'
  [...]
  < HTTP/1.1 409 Conflict

Such a ``409`` error must be handled by the higher-level
application. The revision number must similarly be given if deleting a
metadata/attachment::

  $ curl -v http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/metadata/1024 -X DELETE -H 'If-Match: "1"'
  [...]
  < HTTP/1.1 200 OK

Check out the `OpenAPI reference <https://orthanc.uclouvain.be/api/>`__
of the REST API of Orthanc for more information.

**Warning:** The database index back-end must implement support for
revisions. As of writing, only the **PostgreSQL plugins** in versions
above 4.0 and the **ODBC plugins** implement support for revisions.


Synchronous vs. asynchronous C-MOVE SCP
---------------------------------------

The :ref:`C-MOVE SCP <dicom-move>` of Orthanc (i.e. the component of
the Orthanc server that is responsible for routing DICOM instances
from Orthanc to other modalities) can be configured to run either in
synchronous or in asynchronous mode, depending on the value of the
``SynchronousCMove`` :ref:`configuration option <configuration>`:

* In **synchronous mode** (if ``SynchronousCMove`` is ``true``),
  Orthanc will interleave its C-STORE SCU commands with the C-MOVE
  instructions received from the remote modality. In other words,
  Orthanc immediately sends the DICOM instances while it handles the
  C-MOVE command from the remote modality. This mode is for
  compatibility with simple DICOM client software that considers that
  when its C-MOVE SCU is over, it should have received all the
  instructed DICOM instances. This is the default behavior of Orthanc.

* In **asynchronous mode** (if ``SynchronousCMove`` is ``false``),
  Orthanc will queue the C-MOVE instructions and :ref:`creates a job
  <jobs-synchronicity>` that will issue the C-STORE SCU commands
  afterward. This behavior is typically encountered in hospital-wide
  PACS systems, but requires the client software to be more complex as
  it must be handle the delay between its C-MOVE queries and the
  actual reception of the DICOM instances through C-STORE.

As a consequence, by setting ``SynchronousCMove`` to ``true``, Orthanc
can be used as a buffer that enables communications between a simple
C-MOVE client and a hospital-wide PACS. This can be interesting to
introduce compatibility with specialized image processing
applications.


.. _labels:

Labels
------

.. highlight:: text

Orthanc 1.12.0 introduced the concept of **labels**. A label is a
string that can be attached to any DICOM resource (i.e. patients,
studies, series, or instances). In contrast with :ref:`metadata
<metadata>`, labels are not associated with a value, however labels
are **indexed in the Orthanc database** for efficient lookups.

Labels can notably be used as the building block to implement
**multi-tenancy**, which means that a single database could be shared
between different tenants that are distinguished by different labels.
This idea is illustrated by the :ref:`multitenant DICOM server
<multitenant-dicom>` sample plugin. A similar approach could be used
to implement Web interfaces that restrict the resources that are
accessible to some users by assigning labels to users. Labels are also
useful in **machine learning** (or deep learning) workflows to
separate DICOM resources belonging to the training set or to the
testing set.

The labels attached to one given DICOM resource can be read through
the REST API::

  $ curl http://localhost:8042/instances/19816330-cb02e1cf-df3a8fe8-bf510623-ccefe9f5/labels
  $ curl http://localhost:8042/series/3774320f-ccda46d8-69ee8641-9e791cbf-3ecbbcc6/labels
  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels
  $ curl http://localhost:8042/patients/ef9d77db-eb3b2bef-9b31fd3e-bf42ae46-dbdb0cc3/labels

A label can be added to one DICOM resource using the PUT HTTP method,
and can be removed using the DELETE HTTP method::

  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels
  []
  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels/hello -X PUT -d ''
  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels
  [ "hello" ]
  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels/hello -X DELETE
  $ curl http://localhost:8042/studies/66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e/labels
  []
  
The built-in :ref:`Orthanc Explorer <orthanc-explorer>` Web interface
can be used to display, add, and remove labels.

Once labels are set, the ``/tools/find`` :ref:`route of the REST API
<rest-find>` of Orthanc can be used to efficiently look for the DICOM
resources that are associated with given labels. This is done by
providing the set of labels of interest in the ``Labels`` field, as
illustrated in the following request::

  $ curl --request POST --url http://localhost:8042/tools/find \
    --data '{
              "Level" : "Study",
              "Labels" : [ "hello" ],
              "LabelsConstraint" : "All",
              "Query" : { }
            }'

The ``LabelsConstraint`` field can be used to control the request over
the labels. Its value can be ``All`` (to return the resources that are
associated with all the labels provided in the ``Labels`` field at
once), ``Any`` (to return the resources that are associated with at
least one of the labels provided in the ``Labels`` field), or ``None``
(to return the resources that are associated with none of the labels
provided in the ``Labels`` field). If not provided,
``LabelsConstraint`` defaults to ``All``. Note that if there is only
one label in the ``Labels`` field, both ``Any`` and ``All`` have the
same behavior.

            
**Warning:** The database index back-end must implement support for
labels. As of writing, only the **PostgreSQL plugins** in versions
above 5.0 and the **MySQL plugins** in version above 5.0 implement
support for labels.
