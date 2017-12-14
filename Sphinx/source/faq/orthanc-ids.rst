.. _orthanc-ids:

Orthanc identifiers
===================

In Orthanc, each patient, study, series and instance is assigned with
an unique identifier that is derived from the DICOM identifiers.
Contrarily to the :ref:`identifiers of the DICOM standard
<dicom-identifiers>`, the Orthanc identifiers are formatted as a
`SHA-1 hash <https://en.wikipedia.org/wiki/Sha-1>`__ with a fixed
length, so as to be more Web-friendly. More specifically:

* Patients are identified as the SHA-1 hash of their PatientID tag
  (0010,0020).
* Studies are identified as the SHA-1 hash of the concatenation of
  their PatientID tag (0010,0020) and their StudyInstanceUID tag
  (0020,000d).
* Series are identified as the SHA-1 hash of the concatenation of
  their PatientID tag (0010,0020), their StudyInstanceUID tag
  (0020,000d) and their SeriesInstanceUID tag (0020,000e).
* Instances are identified as the SHA-1 hash of the concatenation of
  their PatientID tag (0010,0020), their StudyInstanceUID tag
  (0020,000d), their SeriesInstanceUID tag (0020,000e), and their
  SOPInstanceUID tag (0008,0018).

NB: The concatenation adds a `pipe
<https://en.wikipedia.org/wiki/Vertical_bar>`__ separator "``|``"
between the concatenated DICOM tags.

Because the DICOM standard guarantees the StudyInstanceUID,
SeriesInstanceUID and SOPInstanceUID tags to be globally unique, the
Orthanc identifiers for studies, series and instances are also
globally unique (provided no hash collision occurs, which is highly
improbable).

The patient-level identifiers are *not* guaranteed to be globally
unique, and might collide between different hospitals. For this
reason, you should **always do queries at the study level** as soon as
you deal with an application that handles patients from different
hospitals.

The actual implementation of the hashing is carried on by the
`DicomInstanceHasher class
<https://bitbucket.org/sjodogne/orthanc/src/default/Core/DicomFormat/DicomInstanceHasher.cpp>`_.


The "Inexistent Tag" error
--------------------------

If you use an old version of Orthanc (< 0.7.4) and you receive the
"*Exception while storing DICOM: Inexistent tag*" error while storing
a DICOM instance into Orthanc, please make sure that all the 4
following tags do exist in the DICOM file:

* PatientID (0010,0020),
* StudyInstanceUID (0020,000d),
* SeriesInstanceUID (0020,000e),
* SOPInstanceUID (0008,0018).

These tags are all used to index the incoming DICOM instances. The
error message is more explicit starting with Orthanc 0.7.4.
