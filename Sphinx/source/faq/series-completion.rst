What do the various status displayed in a series header mean?
=============================================================

A series can be assigned a status by Orthanc. I can list as *unknown*, *missing*, *inconsistent* or *complete*.

The status is meant to convey the completeness of the series, as known by Orthanc.

As a general rule, since there is no generic DICOM tag that contains the number of DICOM instances that
are contained in a given series, and since there is no generic tag that contains the index of a DICOM
instance inside its parent series, it is in general impossible to know if a series is complete in terms
of its instances. This is the meaning of the *Unknown* status displayed by Orthanc.

However, for some types of images (such as cardiac MRI), the DICOM modules might specify a tag that contains
this information. If such a tag is available for a series, Orthanc will either report a *Complete* status
(if all the instances have been received), *Incomplete* (if some instances are [still] missing) or *Inconsistent*
if there is an error inside the numbering of the instances.

