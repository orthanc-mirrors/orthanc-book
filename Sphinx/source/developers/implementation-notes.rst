.. _implementation-notes:

Implementation notes
====================

Encodings
---------

DICOM supports many codepages to encode strings. DICOM instances using
special characters should contain the ``SpecificCharacterSet
(0008,0005)`` tag. The latter tag `specifies which codepage
<http://dicom.nema.org/dicom/2013/output/chtml/part03/sect_C.12.html#sect_C.12.1.1.2>`__
is used by the DICOM instance. Internally, Orthanc converts all these
codepages to the `UTF-8 encoding
<https://en.wikipedia.org/wiki/UTF-8>`__.

In particular, :ref:`plugins <creating-plugins>` must assume that any
string or JSON file coming from the Orthanc core is encoded using
UTF-8. Similarly, plugins must use UTF-8 when calling services
provided by the Orthanc core. The conversion to/from UTF-8 is done
transparently by the plugin engine.

The :ref:`configuration option <configuration>` ``DefaultEncoding``
plays an important role. It is used in three cases:

1. If receiving a DICOM instance without the ``SpecificCharacterSet
   (0008,0005)`` tag, Orthanc will interpret strings within this
   instance using this default encoding. This is important in
   practice, as many DICOM modalities are not properly configured with
   respect to encodings.

2. When answering a :ref:`C-Find query <dicom-find>` (including for
   worklists), Orthanc will use its default encoding. If one single
   answer uses a different encoding, it will be transcoded.

3. If creating a new instance (e.g. through the
   ``/tools/create-dicom`` URI of the :ref:`REST API <rest>`, or
   through the ``OrthancPluginCreateDicom()`` primitive of the plugin
   SDK) and if ``SpecificCharacterSet (0008,0005)`` is not provided
   for this instance, Orthanc will use its default encoding. Note
   however that if ``SpecificCharacterSet`` is set, Orthanc will
   transcode the incoming UTF-8 strings to the codepage specified in
   this tag, and not to the default encoding.
