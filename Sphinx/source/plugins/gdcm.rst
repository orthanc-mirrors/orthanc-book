.. _gdcm:


GDCM plugin for Orthanc
=======================

.. contents::

This **official** plugin extends Orthanc with a decoder/transcoder of
DICOM images that takes advantage of the `Grassroots GDCM library
<https://en.wikipedia.org/wiki/GDCM>`__.

This plugin notably replaces the built-in decoder/transcoder of
Orthanc that internally uses `DCMTK
<https://dicom.offis.de/dcmtk.php.en>`__. This is notably necessary to
deal with DICOM images encoded using `JPEG2000
<https://en.wikipedia.org/wiki/JPEG_2000>`__, as this format is not
readily supported by the core version of DCMTK.


History
-------

Originally, this plugin was a sample snippet that was shipped with the
source code of Orthanc versions below 1.7.0, in the folder
``Plugins/Samples/GdcmDecoder/``. This sample code was itself bundled
in the :ref:`Orthanc Web viewer <webviewer>` (up to release 2.5) and
in the :ref:`Osimis Web viewer <osimis_webviewer>` plugins (up to
releases 1.3.x).

In May 2020, starting with Orthanc 1.7.0, as a part of the large
refactoring necessary to implement :ref:`transcoding <transcoding>`,
the GDCM plugin was migrated as separate plugin. The reasons are
twofold:

* To avoid redundancies between the two viewers, and to improve
  performance by avoiding multiple calls to GDCM on unsupported DICOM
  instances.

* To uncouple the viewers and the :ref:`DICOMweb <dicomweb>` plugins
  from the dependency on GDCM. This notably allows to more easily
  follow new releases of the GDCM library.
     

Compilation
-----------

.. highlight:: bash

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancGdcm`` that
contains the GDCM decoder/transcoder plugin. Pre-compiled binaries for
Microsoft Windows `are also available
<https://www.orthanc-server.com/browse.php?path=/plugin-gdcm>`__.

*Remark:* Some older build instructions are also available in the
`source distribution
<https://hg.orthanc-server.com/orthanc-gdcm/file/default/Resources/BuildInstructions.txt>`__.


Usage
-----

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
      "/home/user/OrthancGdcm/Build/libOrthancGdcm.so"
    ]
  }

.. highlight:: text

Orthanc must of course be restarted after the modification of its
configuration file. Carefully inspect the :ref:`logs <log>` to make
sure that the GDCM plugin is properly loaded.


Advanced options
----------------

.. highlight:: json

The configuration of the GDCM plugin can be fine-tuned by adding some options::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancGdcm/Build/libOrthancGdcm.so"
    ],
    "Gdcm" : {
      "Enable" : false,
      "Throttling" : 4
    },
    "BuiltinDecoderTranscoderOrder" : "After"
  }

* ``Enable`` specifies whether the GDCM decoder/transcoder is enabled.
  By default, this option is set to ``true``.

* ``Throttling`` specifies the maximum number of threads that can
  simultaneously call the GDCM decoder/transcoder. This is useful to
  avoid uncontrolled CPU or RAM usage if many people are connected to
  the same Orthanc server. By default, no throttling is applied, and
  an unrestricted number of threads can call GDCM simultaneously.

* ``BuiltinDecoderTranscoderOrder`` is a configuration option of the
  Orthanc core (i.e. outside of the ``Gdcm`` section) that can be used
  to control whether the built-in DCMTK decoder/transcoder is applied
  before or after GDCM.

As a complement to the ``Enable`` option, you also have the
possibility to restrict the GDCM decoder/transcoder to some specific
`transfer syntaxes
<http://dicom.nema.org/medical/dicom/current/output/html/part05.html#chapter_10>`__
using the ``RestrictTransferSyntaxes`` option. For instance, the
following configuration would use GDCM to decode JPEG 2000 images,
while using DCMTK to decode the other transfer syntaxes::

  {
    [...]
    "Gdcm" : {
      "Enable" : true,
      "RestrictTransferSyntaxes" : [
        "1.2.840.10008.1.2.4.90",   // JPEG 2000 Image Compression (Lossless Only)	 
        "1.2.840.10008.1.2.4.91",   // JPEG 2000 Image Compression 	 
        "1.2.840.10008.1.2.4.92",   // JPEG 2000 Part 2 Multicomponent Image Compression (Lossless Only)
        "1.2.840.10008.1.2.4.93"    // JPEG 2000 Part 2 Multicomponent Image Compression
      ]
    }
  }
