.. _supported-images:

Supported DICOM images
======================

Orthanc can **receive/store/send** any kind of standard DICOM files
(cf. the `DICOM conformance statement
<https://bitbucket.org/sjodogne/orthanc/src/default/Resources/DicomConformanceStatement.txt>`__).

However, its core engine is not able to **render** all of them as PNG
images. An image that Orthanc cannot decode is displayed as
"Unsupported" by Orthanc Explorer. Currently, the core engine of
Orthanc can decode:

* uncompressed (raw) DICOM files,
* JPEG DICOM files, and
* JPEG-LS DICOM files.

The supported photometric interpretations are:

* RGB,
* Grayscale2.

The Orthanc core supports from 8bpp to 16bpp depth, with integer
values.  Multiframe (notably cine), uncompressed DICOM instances can
also be displayed from Orthanc Explorer.

Other type of encodings are available in the `Web viewer plugin
<http://www.orthanc-server.com/static.php?page=web-viewer>`__, that
mostly supports whatever is supported by the well-known `GDCM toolkit
<https://sourceforge.net/projects/gdcm/>`__ by Mathieu Malaterre. Note
however that multiframe (notably cine) DICOM instances are currently
not supported by the Web viewer plugin.

Finally, consider having a look at the section in the Orthanc Book
about the :ref:`compatible DICOM viewers <viewers>`.

