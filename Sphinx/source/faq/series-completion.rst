.. _series-completion:

What does the series completion status mean?
============================================

Each DICOM series is assigned a completion status by Orthanc. This
completion status can list as ``Unknown``, ``Missing``,
``Inconsistent`` or ``Complete``.

The status is meant to convey the completeness of the series, as known
by Orthanc.

As a general rule, since there is no generic DICOM tag that contains
the number of DICOM instances that are contained in a given series,
and since there is no generic tag that contains the index of a DICOM
instance inside its parent series, it is in general impossible to know
if a series is complete in terms of its instances. This is the meaning
of the ``Unknown`` status displayed by Orthanc.

However, for some types of images (such as cardiac MRI), the DICOM
modules might specify a tag that contains this information. If such a
tag is available for a series, Orthanc will either report a
``Complete`` status (if all the instances have been received),
``Incomplete`` (if some instances are [still] missing) or
``Inconsistent`` if there is an error inside the numbering of the
instances.
