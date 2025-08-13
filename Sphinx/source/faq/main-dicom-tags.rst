.. _main-dicom-tags:

Main DICOM Tags in DB
---------------------

Introduction
============

By default, Orthanc is saving a predefined subset of DICOM Tags
in the DB.  These are called the ``MainDicomTags``.

Since they are stored in DB, these tags can be retrieved very
quickly and can conveniently be used for filtering/finding resources
while, to access other DICOM tags, Orthanc needs to re-open the
DICOM file which is much slower.

As of Orthanc 1.12.5 (and later), the predefined list is:

* Patients:
    * PatientName
    * PatentID
    * PatientBirthDate
    * PatientSex
    * OtherPatientIDs

* Studies:
    * StudyDate
    * StudyTime
    * StudyID
    * StudyDescription
    * AccessionNumber
    * StudyInstanceUID
    * RequestedProcedureDescription
    * InstitutionName
    * RequestingPhysician
    * ReferringPhysicianName
    * TimezoneOffsetFromUTC (added in 1.12.5)
    * PatientName *(duplicated from the Patient level)*
    * PatentID *(duplicated from the Patient level)*
    * PatientBirthDate *(duplicated from the Patient level)*
    * PatientSex *(duplicated from the Patient level)*
    * OtherPatientIDs *(duplicated from the Patient level)*


* Series:
    * SeriesDate
    * SeriesTime
    * Modality
    * Manufacturer
    * StationName
    * SeriesDescription
    * BodyPartExamined
    * SequenceName
    * ProtocolName
    * SeriesNumber
    * CardiacNumberOfImages
    * ImagesInAcquisition
    * NumberOfTemporalPositions
    * NumberOfSlices
    * NumberOfTimeSlices
    * SeriesInstanceUID
    * ImageOrientationPatient
    * SeriesType
    * OperatorsName
    * PerformedProcedureStepDescription
    * AcquisitionDeviceProcessingDescription
    * ContrastBolusAgent
    * TimezoneOffsetFromUTC (added in 1.12.5)
    * PerformedProcedureStepStartDate (added in 1.12.5)
    * PerformedProcedureStepStartTime (added in 1.12.5)
    * RequestAttributesSequence (added in 1.12.5)

* Instances:
    * InstanceCreationDate
    * InstanceCreationTime
    * AcquisitionNumber
    * ImageIndex
    * InstanceNumber
    * NumberOfFrames
    * TemporalPositionIdentifier
    * SOPInstanceUID
    * ImagePositionPatient
    * ImageComments
    * ImageOrientationPatient


Adding more tags in DB
======================

.. highlight:: json

Since version 1.11.0, it is possible to
customize a list of ``ExtraMainDicomTags`` to include in the DB
through a new configuration option.

Since version 1.11.1, it is possible to 
include sequences in ``ExtraMainDicomTags``.  However, this should be
considered as an "experimental" feature and you should not store large
sequences (> 64KB) or sequences containing binary tags.

Here is a sample configuration to optimize C-Find queries at study level
e.g from **OSIRIX/Horos**.  They request ``SpecificCharacterSet`` and
``PerformingPhysicianName`` that are not stored in Orthanc DB by default::

    {
        "ExtraMainDicomTags" : {
        "Instance" : [
        ],
        "Series" : [
        ],
        "Study": [
            "PerformingPhysicianName",
            "RETIRED_StudyComments",
            "RETIRED_InterpretationStatusID"
        ],
        "Patient": []
        }
    }


This configuration will apply only to newly added resources
in Orthanc.  If you want to apply this change to resources
already in Orthanc, you may call the ``/studies/../reconstruct``
API route or use the  :ref:`Housekeeper plugin <housekeeper-plugin>` 
to automate this reconstruction process.

*Note :* These ``ExtraMainDicomTags`` are not used when searching
for resources in Orthanc, they are only used when returning results.
E.g. if you have added a ``StudyDescription`` at ``Series`` level and perform
a ``/tools/find`` at ``Series`` level with a filter on the ``StudyDescription``
tag, Orthanc will still use the ``StudyDescription`` recorded at ``Study`` level during
the search but will use the ``StudyDescription`` recorded at ``Series`` level when
returning the responses.

*Note:* You should only include tags from the same or from a higher level:
E.g. Storing ``StudyDescription`` at ``Series`` level is possible since
all series are supposed to share the same ``StudyDescription``.  But, adding
``SeriesDescription`` at ``Study`` level will lead to unpredictible results.
Orthanc will **not** check that the tags levels are adequate. 

*Note:* As of Orthanc 1.12.9, it is not possible to store Private DICOM tags
in the ``ExtraMainDicomTags``.


Warnings
========

Since Orthanc 1.11.0, Orthanc issues a warning everytime
it opens a DICOM file to access a DICOM tag that could have
been saved in DB.

Orthanc will also issue a warning everytime it accesses a resource 
that has been saved with a ``ExtraMainDicomTags`` configuration that
is different from the current one inviting you to call the
``/reconstruct`` route to fix this.

These warnings can be enabled/disabled through this configuration::

    {
        "Warnings" : {
            "W001_TagsBeingReadFromStorage": true,
            "W002_InconsistentDicomTagsInDb": true
        }
    }


DICOMWeb
========

Below is a sample configuration that is well suited to
optimize DICOMWeb routes in general in case you are using the 
``MainDicomTags`` metadata mode.  However, note that, from version
1.15 of the :ref:`DICOMWeb plugin <dicomweb-server-metadata-config>`, you should favor the ``Full`` mode::

    {
        "ExtraMainDicomTags" : {
        "Instance" : [
            "Rows",
            "Columns",
            "ImageType",
            "SOPClassUID",
            "ContentDate",
            "ContentTime",
            "FrameOfReferenceUID",
            "PixelSpacing",
            "SpecificCharacterSet",
            "BitsAllocated",
            "BitsStored"
        ],
        "Series" : [
            "TimezoneOffsetFromUTC",
            "PerformedProcedureStepStartDate",
            "PerformedProcedureStepStartTime",
            "RequestAttributesSequence"
        ],
        "Study": [
            "TimezoneOffsetFromUTC"
        ],
        "Patient": []
        }
    }
