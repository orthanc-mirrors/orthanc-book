.. _indexer:


Folder Indexer plugin
=====================

.. contents::

This **official** plugin by the `ICTEAM institute of UCLouvain
<https://uclouvain.be/en/research-institutes/icteam>`__ uses Orthanc
to publish filesystems containing medical images as a DICOM modality.

The plugin continuously synchronizes the content of an Orthanc server
with the content of a filesystem. This way, the filesystem is
automatically organized according to the :ref:`DICOM model of the real
world <model-world>`, without any manual intervention. The indexed
DICOM resources are immediately available in a Web interface and in a
Web viewer, and can be queried/retrieved by DICOM clients. The DICOM
files are **not** copied, so this solution has a very small footprint
in terms of storage requirements.


Compilation
-----------

.. highlight:: bash

Official releases can be `downloaded from the Orthanc homepage
<https://www.orthanc-server.com/browse.php?path=/plugin-indexer>`__. As
an alternative, the `repository containing the source code
<https://hg.orthanc-server.com/orthanc-indexer/>`__ can be accessed using
Mercurial.

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancIndexer``
that contains the folder indexer plugin for Orthanc.

Pre-compiled Linux Standard Base (LSB) binaries `can be downloaded
<https://lsb.orthanc-server.com/plugin-indexer/>`__.

Pre-compiled binaries for Microsoft Windows and macOS `are also
available
<https://www.orthanc-server.com/browse.php?path=/plugin-indexer>`__.

Furthermore, the :ref:`Docker images <docker>`
``jodogne/orthanc-plugins`` and ``osimis/orthanc`` also contain the
plugin.


Usage
-----

.. highlight:: json

Here is a minimal sample :ref:`configuration file <configuration>` to
use this plugin::

  {
    "Plugins" : [
      "/home/user/OrthancTcia/Build/libOrthancTcia.so"
    ],
    "Indexer" : {
      "Enable" : true,
      "Folders" : [ "/home/user/DICOM" ],   // List of folders to synchronize
      "Interval" : 10                       // Delay between two synchronizations
    }
  }

Orthanc must of course be restarted after the modification of its
configuration file.

Once Orthanc is started, the folders are transparently synchronized
without any further interaction. You can start Orthanc with the
``--verbose-plugins`` command-line option in order to monitor the
synchronization process.
