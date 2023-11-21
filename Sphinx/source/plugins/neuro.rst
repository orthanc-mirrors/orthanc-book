.. _neuro:


Neuroimaging plugin
===================

.. contents::

This **official** plugin by the `ICTEAM institute of UCLouvain
<https://uclouvain.be/en/research-institutes/icteam>`__ extends
Orthanc with features dedicated for neuroimaging:

* Conversion of DICOM series and DICOM instances to the `NIfTI-1
  <https://en.wikipedia.org/wiki/Neuroimaging_Informatics_Technology_Initiative>`__
  file format, directly from the REST API of Orthanc. This is similar
  to `well-known converters
  <https://www.sciencedirect.com/science/article/abs/pii/S0165027016300073?via%3Dihub>`__
  such as ``dcm2niix``, but smoothly integrated within a PACS server
  instead of separate command-line tools.


Compilation
-----------

.. highlight:: bash

Official releases can be `downloaded from the Orthanc homepage
<https://orthanc.uclouvain.be/downloads/sources/orthanc-neuro/index.html>`__. As
an alternative, the `repository containing the source code
<https://orthanc.uclouvain.be/hg/orthanc-neuro/>`__ can be accessed using
Mercurial.

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancNeuro`` that
contains the neuroimaging plugin for Orthanc.

Pre-compiled Linux Standard Base (LSB) binaries `can be downloaded
<https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc-neuro/index.html>`__.

Pre-compiled binaries for `Microsoft Windows <https://orthanc.uclouvain.be/downloads/windows-32/orthanc-neuro/index.html>`__
and `macOS <https://orthanc.uclouvain.be/downloads/macos/orthanc-neuro/index.html>`__ are available as well.

Furthermore, the :ref:`Docker images <docker>`
``jodogne/orthanc-plugins`` and ``osimis/orthanc`` also contain the
plugin.


Usage
-----

Configuration
^^^^^^^^^^^^^

.. highlight:: json

Here is a minimal sample :ref:`configuration file <configuration>` to
use this plugin::

  {
    "Plugins" : [
      "/home/user/OrthancNeuro/Build/libOrthancNeuro.so"
    ]
  }

Orthanc must of course be restarted after the modification of its
configuration file.

If you wish to convert DICOM instances using the JPEG2k transfer
syntax, don't forget to also enable the :ref:`GDCM plugin <gdcm>`.


Conversion to NIFTI
^^^^^^^^^^^^^^^^^^^

When the plugin is enabled, the built-in **Orthanc Explorer** user
interface will provide a yellow button entitled ``Export to NIfTI`` at
the series and instance levels.

The same feature is accessible to external software through the **REST
API of Orthanc** at the following URIs:

* ``/series/{id}/nifti`` to convert the DICOM series whose
  :ref:`Orthanc ID <orthanc-ids>` is ``{id}`` to one uncompressed
  NIfTI-1 file (file extension ``.nii``).

* ``/series/{id}/nifti?compress`` to convert the DICOM series whose
  :ref:`Orthanc ID <orthanc-ids>` is ``{id}`` to one gzip-compressed
  NIfTI-1 file (file extension ``.nii.gz``).

* ``/instances/{id}/nifti`` to convert the DICOM instance whose
  :ref:`Orthanc ID <orthanc-ids>` is ``{id}`` to one uncompressed
  NIfTI-1 file (file extension ``.nii``).

* ``/instances/{id}/nifti?compress`` to convert the DICOM instance whose
  :ref:`Orthanc ID <orthanc-ids>` is ``{id}`` to one gzip-compressed
  NIfTI-1 file (file extension ``.nii.gz``).
