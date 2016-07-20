.. _dicomweb:


DICOMweb plugin
===============

This **official** plugin extends Orthanc with support of the `DICOMweb
protocols <https://en.wikipedia.org/wiki/DICOMweb>`__. More precisely,
the plugin introduces a basic, reference implementation of WADO-URI,
WADO-RS, QIDO-RS and STOW-RS, following `DICOM PS3.18
<http://dicom.nema.org/medical/dicom/current/output/html/part18.html>`__.

For general information, check out the `official homepage of the
plugins <http://www.orthanc-server.com/static.php?page=dicomweb>`__.

The full standard is not implemented yet, the supported features are
`tracked in the repository
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Status.txt>`__. Some
integration tests are `available separately
<https://bitbucket.org/sjodogne/orthanc-tests/src/default/Plugins/DicomWeb/Run.py>`__.
