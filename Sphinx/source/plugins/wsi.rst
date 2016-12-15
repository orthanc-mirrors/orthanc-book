.. _wsi:


Whole-Slide Microscopic Imaging
===============================

.. contents::

The Orthanc project provides three **official tools** to support DICOM
for whole-slide microscopic imaging (WSI):

1. A so-called "DICOM-izer" command-line tool that converts
   whole-slide images to DICOM series, following `Supplement 145
   <ftp://medical.nema.org/medical/dicom/final/sup145_ft.pdf>`__.
2. A plugin that extends Orthanc with a Web viewer of whole-slide
   images for digital pathology. 
3. Another command-line tool that converts a DICOM series stored
   in Orthanc, to a standard hierarchical TIFF image.

For general information, check out the `official homepage of the
framework <http://www.orthanc-server.com/static.php?page=wsi>`__. 


Compilation
-----------

.. highlight:: bash

The procedure to compile the WSI framework is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  # Firstly, compile the command-line tools
  $ mkdir Applications/Build
  $ cd Applications/Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make
  # Secondly, compile the plugin
  $ mkdir ../../ViewerPlugin/Build
  $ cd ../../ViewerPlugin/Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make  

The compilation will produce 3 binaries:

* ``Applications/Build/OrthancWSIDicomizer``, which contains the DICOM-izer.
* ``Applications/Build/OrthancWSIDicomToTiff``, which contains the DICOM-to-TIFF converter.
* ``ViewerPlugin/Build/OrthancWSI``, which is a shared library containing the plugin for Orthanc.

Note that pre-compiled binaries for Microsoft Windows `are available
<http://www.orthanc-server.com/browse.php?path=/whole-slide-imaging>`__.


Installation of the plugin
--------------------------

.. highlight:: json

You of course first have to :ref:`install Orthanc <compiling>`. Once
Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/orthanc-wsi/ViewerPlugin/Build/libOrthancWSI.so"
    ]
  }

Orthanc must of course be restarted after the modification of its
configuration file. The WSI plugin has no specific configuration
option.

Once a :ref:`DICOM series <model-world>` is opened using Orthanc
Explorer, a yellow button entitled ``Whole-Slide Imaging Viewer`` will
show up for whole-slide images. It will open the WSI viewer for that
particular series. This behavior can be seen on the Orthanc Explorer
running on our `WSI demonstration server
<http://wsi.orthanc-server.com/orthanc/app/explorer.html>`__.



Command-line tools
------------------

.. highlight:: bash

The command-line tools ``OrthancWSIDicomizer`` and
``OrthancWSIDicomToTiff`` provide documentation of all their options
if started with the ``--help`` parameter::

  $ OrthancWSIDicomizer --help
  $ OrthancWSIDicomToTiff --help

In this section, we review the most common usages of these tools.


Transcoding a DICOM image
^^^^^^^^^^^^^^^^^^^^^^^^^

The most simple usage consists in converting some whole-slide image to
DICOM, then uploading it to Orthanc::

  $ OrthancWSIDicomizer Source.tif

This command will transcode some `hierarchical, tiled TIFF
<https://en.wikipedia.org/wiki/TIFF>`__ image called ``Source.tif``,
and push the output DICOM files to the default Orthanc server (running
on ``localhost`` and listening to HTTP port ``8042``) using its
:ref:`REST API <rest>`. This operation is fast, as no re-encoding
takes place: If the source TIFF image contains JPEG tiles, these tiles
will be written as such.


Re-encoding a DICOM image
^^^^^^^^^^^^^^^^^^^^^^^^^




Proprietary file formats
^^^^^^^^^^^^^^^^^^^^^^^^

Out-of-the-box, the DICOM-izer supports standard hierarchical TIFF
images. Some commonplace image formats (PNG and JPEG) can be
DICOM-ized as well. However, whole-slide images can come in many
proprietary file formats. To transcode such images, the DICOM-izer
relies upon the `OpenSlide toolbox <http://openslide.org/>`__.  

For this feature to work, you have to tell the command-line tool where
it can find the OpenSlide shared library. GNU/Linux distributions
generally provide packages containing the OpenSlide shared library
(under Debian/Ubuntu, simply install the ``libopenslide0`` package)::

  $ OrthancWSIDicomizer --openslide=libopenslide.so CMU-1-JP2K-33005.svs

Precompiled Microsoft Windows binaries of this shared library can be
found on the `OpenSlide homepage <http://openslide.org/download/>`__::

  $ OrthancWSIDicomizer --openslide=libopenslide-0.dll CMU-1-JP2K-33005.svs

Note that this operation implies the re-encoding of the source image
from the proprietary file format, which is much more time-consuming
than simply transcoding a TIFF image.



Specifying a DICOM dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^


Converting DICOM to TIFF
^^^^^^^^^^^^^^^^^^^^^^^^


REST API
--------

