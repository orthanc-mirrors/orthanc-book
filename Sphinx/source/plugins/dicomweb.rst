.. _dicomweb:


DICOMweb plugin
===============

.. contents::

This **official** plugin extends Orthanc with support of the `DICOMweb
protocols <https://en.wikipedia.org/wiki/DICOMweb>`__. More precisely,
the plugin introduces a basic, reference implementation of WADO-URI,
WADO-RS, QIDO-RS and STOW-RS, following `DICOM PS3.18
<http://dicom.nema.org/medical/dicom/current/output/html/part18.html>`__.

For general information, check out the `official homepage of the
plugins <http://www.orthanc-server.com/static.php?page=dicomweb>`__.

The full standard is not implemented yet, the supported features are
`tracked in the repository
<https://bitbucket.org/sjodogne/orthanc-dicomweb/src/default/Status.txt>`__. Some
integration tests are `available separately
<https://bitbucket.org/sjodogne/orthanc-tests/src/default/Plugins/DicomWeb/Run.py>`__.


Compilation
-----------

.. highlight:: text

The procedure to compile these plugins is similar of that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON
  $ make

The compilation will produce a shared library ``OrthancDicomWeb`` that
contains the DICOMweb plugin.  Pre-compiled binaries for Microsoft
Windows `are also available
<http://www.orthanc-server.com/browse.php?path=/plugin-dicom-web>`__.
A package for `Apple's Mac OS X
<http://localhost/~jodogne/orthanc/static.php?page=download-mac>`__ is
available courtesy of `Osimis <http://osimis.io/>`__.


Usage
-----

.. highlight:: json

You of course first have to :ref:`install Orthanc <binaries>`. Once
Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancDicomWeb/Build/libOrthancDicomWeb.so"
    ]
  }

The root of the DICOMweb REST API is then accessible at ``http://localhost:8042/dicom-web/``.


Options
-------

.. highlight:: json

Several configuration options are also available, and are listed in
the example below::

  {
    "DicomWeb" : {
      "Enable" : true,         // Whether DICOMweb support is enabled
      "Root" : "/dicom-web/",  // Root URI of the DICOMweb API (for QIDO-RS, STOW-RS and WADO-RS)
      "EnableWado" : true,     // Whether WADO-URI (aka. WADO) support is enabled
      "WadoRoot" : "/wado",    // Root URI of the WADO-URI (aka. WADO) API
      "Host" : "localhost",    // Hard-codes the name of the host for subsequent WADO-RS requests
      "Ssl" : false            // Whether HTTPS should be used for subsequent WADO-RS requests
    }
  }

