.. _debugging_encodings:

Debugging encoding issues (SpecificCharacterSet)
================================================

.. contents::

.. highlight:: bash

Orthanc does not display the PatientName correctly
--------------------------------------------------

If your DICOM files are valid, Orthanc should display all strings correctly both
in the UI and in the Rest API in which all strings are converted to UTF-8.

However, it might still be useful to understand what's wrong with your files
such that you can possibly fix your files once they have been stored in Orthanc
or configure your modality correctly.

**Example 1**: a DICOM file is sent to Orthanc with ``SpecificCharacterSet`` set to ``ISO_IR 100``
(Latin1).  The PatientName is expected to be ``ccžšd^CCŽŠÐ`` but Orthanc displays ``ccd^CCÐ``.
If you open the DICOM file in an Hex editor and search for the PatientName, you'll find this sequence
of bytes: ``63 63 9e 9a 64 5e 43 43 8e 8a d0``.  By checking the `Latin1 code page 
<https://en.wikipedia.org/wiki/ISO/IEC_8859-1>`__, you realise that the ``9e`` and ``9a`` characters
are not valid Latin1 characters and are therefore replaced by ```` in Orthanc UI.  

In this case, they have most likely been generated on a Windows system by using the default `Windows 1252 
<https://en.wikipedia.org/wiki/Windows-1252>`__ encoding in which ``9e`` is ``ž``.

How to solve it ?  It is highly recommended to fix it before Orthanc: in your RIS, worklist server or modality.
However, if you can not fix it there, you may still try to fix it once the file has been stored in Orthanc.
You can get inspiration from this `lua script <https://bitbucket.org/osimis/orthanc-setup-samples/src/master/lua-samples/sanitizeInvalidUtf8TagValues.lua>`__ 
that is fixing invalid UTF-8 characters

