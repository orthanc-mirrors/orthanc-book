.. _viewers:

What DICOM viewer is compatible with Orthanc?
=============================================

Basically, any viewer that supports :ref:`DICOM query/retrieve
<query-retrieve>` should be compatible with Orthanc.

Because the Orthanc project is focused on the promotion of free
software for medical imaging, we do not publish the list of
proprietary DICOM viewers that are compatible with Orthanc. Here is a
list of free and open-source viewers that are known to be compatible
with Orthanc (do not hesitate to `warn us
<mailto:s.jodogne@gmail.com>`__ about other compatible FOSS):

* `Horos <https://www.horosproject.org/>`__.
* `Gingko CADx <https://www.ginkgo-cadx.com/>`__ (a
  :ref:`configuration guide <ginkgo-cadx>` is available).
* `3D Slicer <https://www.slicer.org/>`__.
* `medInria <https://med.inria.fr/>`__.
* `Aeskulap <https://github.com/pipelka/aeskulap>`__.
* `OsiriX <http://www.osirix-viewer.com/>`__ (note however that the
  openness of this particular software is `currently subject to
  discussion
  <http://blog.purview.net/an-open-letter-to-the-osirix-community>`__).

Make also sure to check out the following extensions to Orthanc:

* `Web viewer plugin <http://www.orthanc-server.com/static.php?page=web-viewer>`__.
* `ImageJ extension <http://www.orthanc-server.com/static.php?page=imagej>`__.
* `Stone of Orthanc <http://www.orthanc-server.com/static.php?page=stone>`__.
* `dwv-orthanc-plugin
  <https://github.com/ivmartel/dwv-orthanc-plugin>`__ by Yves
  Martelli, that embeds `dwv
  <https://github.com/ivmartel/dwv/wiki>`__.
* `Advanced Web viewer plugin by Osimis
  <https://bitbucket.org/osimis/osimis-webviewer-plugin>`__.

Very importantly, Marco Barnig independently keeps track of a list of
`Mobile DICOM Viewers <http://www.web3.lu/mobile-dicom-viewers/>`__
that are compatible with Orthanc. The Orthanc project is very grateful
to Marco for this great contribution.

As far as Sébastien Jodogne is concerned, he uses the Web viewer
plugin and the ImageJ extension for simple analysis tasks. For more
intensive 3D viewing, he uses Ginkgo CADx. Finally, for advanced
usages (such as PET-CT fusion or contouring), he switches to 3D
Slicer.

If you face problems when configuring DICOM networking, make sure to
follow the :ref:`troubleshooting guide <dicom>`.
