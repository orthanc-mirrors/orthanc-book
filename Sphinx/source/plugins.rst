.. _plugins:

Plugins
=======

.. contents::

Overview
--------

The core of Orthanc can be extended through **plugins**. A plugin
takes the form of a shared library (``.DLL`` under Windows, ``.so``
under Linux, ``.dylib`` under Apple OS X...). A plugin can do various
things, among others:

* Serving new **Web applications** that have full access to the REST
  API of Orthanc, which makes easy to handle DICOM images from
  JavaScript code.
* Replacing **the way DICOM images are decoded** (e.g. the official
  :ref:`Web viewer plugin <webviewer>` introduces the decoding of
  JPEG2000 images, which is not available in the core of Orthanc).
* Replacing the default **database back-end** of Orthanc (that is built
  upon SQLite) by another (:ref:`PostgreSQL <postgresql>`, MySQL, SQL Server...).
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

.. toctree::
   :maxdepth: 1

   plugins/webviewer.rst
   plugins/dicomweb.rst
   plugins/postgresql.rst
   plugins/worklists-plugin.rst
   plugins/serve-folders.rst


.. _plugins-contributed:

Index of the contributed plugins
--------------------------------

* `Osimis <http://osimis.io/>`__ maintains an evolution of the
  official Web viewer plugin. The Osimis plugin adds tools for
  measuring, for viewing multiple series, and for split-pane.  `Check
  out their source code
  <https://bitbucket.org/osimis/osimis-webviewer-plugin>`__.
* `DWV Orthanc Plugin
  <https://github.com/ivmartel/dwv-orthanc-plugin>`__: This plugin by
  Yves Martelli is based on `dwv
  <https://github.com/ivmartel/dwv/wiki>`__ and extends Orthanc with a
  Web viewer of DICOM images.
* Another Web viewer is provided courtesy of `Emsy Chan
  <https://groups.google.com/d/msg/orthanc-users/EC5Z2KaM4Hs/MG3KkzhCDAAJ>`__.

*Remark:* Do not hesitate to `contact us
<http://www.orthanc-server.com/static.php?page=contact>`__ if you have
developed a plugin so that we can include it in the list above!
