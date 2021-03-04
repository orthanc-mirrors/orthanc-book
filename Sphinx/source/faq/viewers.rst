.. _viewers:

What DICOM viewer is compatible with Orthanc?
=============================================

.. note:: The viewer that is the easiest to use with Orthanc is most
          probably the `Stone Web viewer
          <https://www.orthanc-server.com/static.php?page=stone-web-viewer>`__.
  
Basically, any viewer that supports :ref:`DICOM query/retrieve
<query-retrieve>` should be compatible with Orthanc.

Because the Orthanc project is focused on the promotion of free
software for medical imaging, we do not publish the list of
proprietary DICOM viewers that are compatible with Orthanc. Here is a
list of free and open-source viewers that are known to be compatible
with Orthanc (do not hesitate to `warn us
<mailto:s.jodogne@orthanc-labs.com>`__ about other compatible FOSS):

* `Open Health Imaging Foundation (OHIF) <https://docs.ohif.org/>`__.
* `Horos <https://horosproject.org/>`__.
* `Gingko CADx <http://ginkgo-cadx.com/en/>`__ (a
  :ref:`configuration guide <ginkgo-cadx>` is available).
* `3D Slicer <https://www.slicer.org/>`__.
* `medInria <https://med.inria.fr/>`__.
* `Aeskulap <https://github.com/pipelka/aeskulap>`__.
* `Weasis
  <https://nroduit.github.io/en/basics/customize/integration/#orthanc-web-server>`__
  (through the :ref:`DICOM web plugin <dicomweb>`).

Make also sure to check out the following extensions to Orthanc:

* `Stone Web viewer plugin <https://www.orthanc-server.com/static.php?page=stone-web-viewer>`__
  (advanced version of the Orthanc Web viewer).
* `Orthanc Web viewer plugin <https://www.orthanc-server.com/static.php?page=web-viewer>`__.
* `Osimis Web viewer plugin
  <https://www.orthanc-server.com/static.php?page=osimis-web-viewer>`__
  (deprecated, but provides compatibility with Web browsers that do
  not support `WebAssembly <https://caniuse.com/?search=wasm>`__).
* `ImageJ extension <https://www.orthanc-server.com/static.php?page=imagej>`__.
* `Stone of Orthanc <https://www.orthanc-server.com/static.php?page=stone>`__.
* `dwv-orthanc-plugin
  <https://github.com/ivmartel/dwv-orthanc-plugin>`__ by Yves
  Martelli, that embeds `dwv
  <https://github.com/ivmartel/dwv/wiki>`__.

Very importantly, Marco Barnig independently keeps track of a list of
`Mobile DICOM Viewers <http://www.web3.lu/mobile-dicom-viewers/>`__
that are compatible with Orthanc. The Orthanc project is very grateful
to Marco for this great contribution.

If you face problems when configuring DICOM networking, make sure to
follow the :ref:`troubleshooting guide <dicom>`.
