.. _plugins:

Plugins
=======

.. contents::

Overview
--------

The core of Orthanc can be extended through **plugins**. A plugin
takes the form of a shared library (``.DLL`` under Windows, ``.so``
under GNU/Linux, ``.dylib`` under Apple OS X...). A plugin can do
various things, among others:

* Serving new **Web applications** that have full access to the REST
  API of Orthanc, which makes easy to handle DICOM images from
  JavaScript code.
* Replacing **the way DICOM images are decoded** (e.g. the official
  :ref:`Web viewer plugin <webviewer>` introduces the decoding of
  JPEG2000 images, which is not available in the core of Orthanc).
* Replacing the default **database back-end** of Orthanc (that is
  built upon SQLite) by another (:ref:`PostgreSQL <postgresql>`,
  :ref:`MySQL <mysql>`, SQL Server...).
* Creating **new REST APIs** on the top of the Orthanc built-in API (as in
  in the official :ref:`DICOMweb <dicomweb>` plugin).
* **Reacting** to the arrival of new DICOM images or other
  DICOM-related events so as to carry on automated processing.
* ...

Developers external to the official Orthanc project are :ref:`invited
to contribute <contributing>` to the C/C++ part of Orthanc by creating
third-party plugins.  A specific section of the Orthanc Book explains
:ref:`how to create new Orthanc plugins <creating-plugins>`.

.. _plugins-official:

Index of the official plugins
-----------------------------

Viewers
^^^^^^^

.. toctree::
   :maxdepth: 1

   plugins/stone-webviewer.rst
   plugins/orthanc-explorer-2.rst
   plugins/ohif.rst
   plugins/volview.rst
   plugins/osimis-webviewer.rst
   plugins/webviewer.rst


Standards
^^^^^^^^^

.. toctree::
   :maxdepth: 1

   plugins/dicomweb.rst
   plugins/worklists-plugin.rst
   plugins/wsi.rst
   plugins/neuro.rst
   plugins/stl.rst


Databases
^^^^^^^^^

.. toctree::
   :maxdepth: 1

   plugins/postgresql.rst
   plugins/mysql.rst
   plugins/object-storage.rst
   plugins/google-cloud-platform.rst    
   plugins/odbc.rst


Languages
^^^^^^^^^

.. toctree::
   :maxdepth: 1

   plugins/python.rst
   plugins/java.rst


Artificial intelligence
^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   plugins/tcia.rst
   Mammography plugin <https://github.com/jodogne/orthanc-mammography>

Tools
^^^^^

.. toctree::
   :maxdepth: 1

   plugins/advanced-storage.rst
   plugins/authorization.rst
   plugins/delayed-deletion-plugin.rst
   plugins/gdcm.rst
   plugins/housekeeper.rst
   plugins/indexer.rst
   plugins/multitenant-dicom.rst
   plugins/serve-folders.rst
   plugins/transfers.rst


.. _plugins-contributed:

Index of the contributed plugins
--------------------------------

C/C++ plugins
^^^^^^^^^^^^^

* `AWS S3 storage plugin
  <https://github.com/radpointhq/orthanc-s3-storage>`__: This plugin
  by `Radpoint <https://radpoint.pl/>`__ makes Orthanc store its
  DICOM files into an `Amazon S3 bucket
  <https://en.wikipedia.org/wiki/Amazon_S3>`__.

* `DWV Orthanc Plugin
  <https://github.com/ivmartel/dwv-orthanc-plugin>`__: This plugin by
  Yves Martelli is based on `dwv
  <https://github.com/ivmartel/dwv/wiki>`__ and extends Orthanc with a
  Web viewer of DICOM images.

* Another Web viewer is provided courtesy of `Emsy Chan
  <https://groups.google.com/d/msg/orthanc-users/EC5Z2KaM4Hs/MG3KkzhCDAAJ>`__.

* `VPI Reveal <https://www.vpireveal.com/>`__ provides a plugin to
  "write the DICOM records in a normal Windows-readable file hierarchy
  (patient-study-series-DICOM file) at a location called
  ``VPIStorage`` that can then be imported into VPI Reveal."  `Check
  out their source code
  <https://github.com/jodogne/OrthancContributed/tree/master/Plugins/orthancVPIRevealPlugin>`__.

* `Doc Cirrus <https://www.doc-cirrus.com/>`__ is working on `MongoDB
  <https://en.wikipedia.org/wiki/MongoDB>`__ database plugins. Check
  out their `source code
  <https://github.com/Doc-Cirrus/orthanc-mongodb>`__ and the
  `associated description
  <https://github.com/jodogne/OrthancContributed/tree/master/Plugins/orthanc-mongodb>`__.


Python plugins
^^^^^^^^^^^^^^

* Julian Hartig maintains a `Python plugin
  <https://github.com/crispinus2/orthanc-gdt>`__ called
  ``orthanc-gdt``, in order to glue Orthanc to the `GDT interface most
  German AIS <https://en.wikipedia.org/wiki/XDT>`__
  (Arztinformationssysteme - as opposed to e.g. the RIS used by
  radiologists) use for communicating with external applications and
  devices. This topic is further discussed on the `Orthanc Users forum
  <https://groups.google.com/d/msg/orthanc-users/NO7MnWzKsAc/5hEVxymWBQAJ>`__.

* Stephen Douglas Scotti maintains an `integrated Docker package
  <https://github.com/sscotti/PACS_Integration>`__, that provides a
  portal application using Laravel (which demonstrates pagination and
  some other features), and some MPPS and MWL features.

* Walco van Loon maintains `Orthanc Server Extensions
  <https://github.com/walkIT-nl/orthanc-server-extensions>`__ as *"A
  simple Orthanc python plugin based framework to extend Orthanc's
  feature set with testable python scripts."*. Check out the original
  announcement on the `Orthanc Users forum
  <https://groups.google.com/g/orthanc-users/c/q3Tncx3b6os/m/iFLq85fKAgAJ>`__.

* Oskar Bożek maintains `orthanc-radiant
  <https://github.com/boskar/orthanc-radiant/>`__ as an Orthanc plugin
  written in Python for invoking ``radiant://`` URI scheme from
  Orthanc Explorer. Check out the original announcement on the
  `Orthanc Users forum
  <https://discourse.orthanc-server.org/t/radiant-dicom-viewer-uri-integration-plugin/5589?u=jodogne>`__.


Rust plugins
^^^^^^^^^^^^

As the Rust language can produce shared libraries that are binary
compatible with the `C ABI
<https://en.wikipedia.org/wiki/Application_binary_interface>`__, it is
possible to create plugins using Rust:

* Andrew Webber provides `Rust plugins
  <https://github.com/andrewwebber/orthanc-rust-plugins>`__ showcasing
  integration with Orthanc, notably a S3 storage (CRUD) and a change
  notification. Check out the original announcement on the `Orthanc
  Users forum
  <https://groups.google.com/g/orthanc-users/c/bDNBLMqXlEk/m/sGgzS5ZVBwAJ>`__.
  
  
Other
^^^^^

* Check out the `OrthancContributed repository on GitHub
  <https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__, that
  might contain plugins that are not tracked in this list.

* **Important:** Do not hesitate to `contact us
  <https://www.orthanc-server.com/static.php?page=contact>`__ if you
  have developed a plugin so that we can promote it in the list above!
