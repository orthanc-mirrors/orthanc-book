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

As of Orthanc 1.4.2 (and later), the predefined list is:

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

Since version 1.11.0 (not released yet), it is possible to
customize a list of ``ExtraMainDicomTags`` to include in the DB
through a new configuration option.

Below is a sample configuration that is well suited to
optimize DICOMWeb routes in general, especially when you are using
a DICOMWeb viewer::

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
            "PerformedProcedureStepStartTime"
        ],
        "Study": [
            "TimezoneOffsetFromUTC"
        ],
        "Patient": []
        }
    }

This configuration will apply only to newly added resources
in Orthanc.  If you want to apply this change to resources
already in Orthanc, you may call the ``/studies/../reconstruct``
API route or use the  :ref:`Housekeeper plugin <housekeeper-plugin>` 
to automate this reconstruction process.


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


