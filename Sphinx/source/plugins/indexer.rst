.. _indexer:


Folder Indexer plugin
=====================

.. contents::

This **official** plugin by the `ICTEAM institute of UCLouvain
<https://orthanc.uclouvain.be/>`__ uses Orthanc to publish filesystems
containing medical images as a DICOM modality.

The plugin continuously synchronizes the content of an Orthanc server
with the content of a filesystem, which can then be accessed, through
Orthanc, based on the :ref:`DICOM model of the real world <model-world>`.
The indexed DICOM resources are immediately available in a Web
interface and in a Web viewer, and can be queried/retrieved by DICOM
clients. The DICOM files are **not** copied, so this solution has a
very small footprint in terms of storage requirements.

.. note:: 
  This plugin now has an alternative implementation as part of the
  :ref:`Advanced storage <advanced-storage>` plugin.


Compilation
-----------

.. highlight:: bash

Official releases can be `downloaded from the Orthanc homepage
<https://orthanc.uclouvain.be/downloads/sources/orthanc-indexer/index.html>`__. As
an alternative, the `repository containing the source code
<https://orthanc.uclouvain.be/hg/orthanc-indexer/>`__ can be accessed using
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
<https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc-indexer/index.html>`__.

Pre-compiled binaries for `Microsoft Windows <https://orthanc.uclouvain.be/downloads/windows-32/orthanc-indexer/index.html>`__
and `macOS <https://orthanc.uclouvain.be/downloads/macos/orthanc-indexer/index.html>`__ available as well.

Furthermore, the :ref:`Docker images <docker>`
``jodogne/orthanc-plugins`` and ``orthancteam/orthanc`` also contain the
plugin.


Usage
-----

.. highlight:: json

Here is a minimal sample :ref:`configuration file <configuration>` to
use this plugin::

  {
    "Plugins" : [
      "/home/user/OrthancIndexer/Build/libOrthancIndexer.so"
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

Some remarks:

* This plugin cannot be used together with other custom storage area
  plugins (such as :ref:`cloud object storage <object-storage>`).

* Even if the folder indexer plugin is in use, you can still add other
  DICOM files using the :ref:`REST API <rest>` or the :ref:`DICOM
  network protocol <dicom-protocol>`. Such files would be stored in
  the ``OrthancStorage`` :ref:`usual folder <orthanc-storage-area>`.

