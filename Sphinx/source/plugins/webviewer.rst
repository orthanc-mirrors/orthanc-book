.. _webviewer:


Web Viewer plugin
=================

.. contents::

This **official** plugin extends Orthanc with a Web viewer of medical images.

For general information, check out the `official homepage of the
plugin <http://www.orthanc-server.com/static.php?page=web-viewer>`__.


Compilation
-----------

.. highlight:: bash

The procedure to compile these plugins is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancWebViewer``
that contains the Web viewer plugin.  Pre-compiled binaries for
Microsoft Windows `are also available
<http://www.orthanc-server.com/browse.php?path=/plugin-webviewer>`__.

*Remark:* Some older build instructions are also available in the
`source distribution
<https://bitbucket.org/sjodogne/orthanc-webviewer/src/default/Resources/BuildInstructions.txt>`__.


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
      "/home/user/OrthancWebViewer/Build/libOrthancWebViewer.so"
    ]
  }

.. highlight:: text

Orthanc must of course be restarted after the modification of its
configuration file. The log will contain an output similar to::

  # Orthanc ./Configuration.json 
  W0226 16:59:10.480226  7906 main.cpp:636] Orthanc version: mainline
  [...]
  W0226 16:59:10.519664  7906 PluginsManager.cpp:258] Registering plugin 'web-viewer' (version 1.0)
  W0226 16:59:10.519696  7906 PluginsManager.cpp:148] Initializing the Web viewer
  W0226 16:59:10.520004  7906 PluginsManager.cpp:148] Web viewer using 6 threads for the decoding of the DICOM images
  W0226 16:59:10.520021  7906 PluginsManager.cpp:148] Storing the cache of the Web viewer in folder: OrthancStorage/WebViewerCache
  W0226 16:59:10.522011  7906 PluginsManager.cpp:148] Web viewer using a cache of 100 MB
  [...]
  W0226 16:59:10.530807  7906 main.cpp:516] HTTP server listening on port: 8042
  W0226 16:59:10.581029  7906 main.cpp:526] DICOM server listening on port: 4242
  W0226 16:59:10.581066  7906 main.cpp:533] Orthanc has started

Once a :ref:`DICOM series <model-world>` is opened using Orthanc
Explorer, a yellow button entitled ``Orthanc Web Viewer`` will show
up. It will open the Web viewer for that particular series.  See also
the demonstration video on `official homepage of the plugin
<http://www.orthanc-server.com/static.php?page=web-viewer>`__.


Advanced options
----------------

.. highlight:: json

The configuration of the Web viewer can be fine-tuned by adding some options::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancWebViewer/Build/libOrthancWebViewer.so"
    ],
    "WebViewer" : {
      "CachePath" : "WebViewerCache",
      "CacheSize" : 10,
      "Threads" : 4,
      "EnableGdcm" : false
    }
  }

* ``CachePath`` specifies the location of the cache of the Web
  viewer. By default, the cache is located inside the storage
  directory of Orthanc.
* ``CacheSize`` specifies the maximum size for the cached images, in
  megabytes. By default, a cache of 100 MB is used.
* ``Threads`` specifies the number of threads that are used by the
  plugin to decode the DICOM images.
* ``EnableGdcm`` specifies whether `GDCM
  <https://sourceforge.net/projects/gdcm/>`__ should be used to decode
  DICOM images, replacing the built-in decoder of Orthanc that
  internally uses `DCMTK <http://dicom.offis.de/dcmtk.php.en>`__.
  This is notably necessary to deal with DICOM images encoded using
  `JPEG2000 <https://en.wikipedia.org/wiki/JPEG_2000>`__, as this
  format is not readily supported by the core version of DCMTK.  By
  default, this option is set to ``true``.

As a complement to the ``EnableGdcm`` option, you also have the
possibility to restrict the GDCM decoder to some specific `transfer
syntaxes
<http://dicom.nema.org/medical/dicom/current/output/html/part05.html#chapter_10>`__
using the ``RestrictTransferSyntaxes`` option.  For instance, the
following configuration would use GDCM to decode JPEG 2000 images,
while using DCMTK to decode the other transfer syntaxes::

  {
    [...]
    "WebViewer" : {
      "EnableGdcm" : true,
      "RestrictTransferSyntaxes" : [
        "1.2.840.10008.1.2.4.90",   // JPEG 2000 Image Compression (Lossless Only)	 
        "1.2.840.10008.1.2.4.91",   // JPEG 2000 Image Compression 	 
        "1.2.840.10008.1.2.4.92",   // JPEG 2000 Part 2 Multicomponent Image Compression (Lossless Only)
        "1.2.840.10008.1.2.4.93"    // JPEG 2000 Part 2 Multicomponent Image Compression
      ]
    }
  }


Frequently Asked Questions
--------------------------

* If **Orthanc does not start anymore** after a hard shutdown, this
  might reflect a corruption in the cache of the Web viewer. In such a
  case, it is safe to remove the folder that contains the cache. By
  default, this folder is called
  ``OrthancStorage/WebViewerCache/``. Of course, don't remove the
  folder ``OrthancStorage/``, as it contains the DICOM files.
