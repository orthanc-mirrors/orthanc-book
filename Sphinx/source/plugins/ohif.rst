.. _ohif:


OHIF plugin
===========

.. contents::

This **official** plugin by the `ICTEAM institute of UCLouvain
<https://uclouvain.be/en/research-institutes/icteam>`__ extends
Orthanc with the `OHIF <https://ohif.org/>`__ extensible Web imaging
platform.


Usage
-----

This plugin adds a dedicated button to Orthanc Explorer, which
provides an easy, fast access to the OHIF viewers (click on the image
to view a demo video):

.. image:: ../images/OHIF.png
           :align: center
           :width: 800
           :target: https://www.youtube.com/watch?v=-lzddzq9iT4
|

The plugin greatly simplifies the deployment of OHIF, as it does not
necessitate the setup of any reverse proxy.


Compilation
-----------

.. highlight:: bash

Official releases can be `downloaded from the Orthanc homepage
<https://www.orthanc-server.com/browse.php?path=/plugin-ohif>`__. As
an alternative, the `repository containing the source code
<https://orthanc.uclouvain.be/hg/orthanc-ohif/>`__ can be accessed
using Mercurial.

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
on most GNU/Linux distributions, provided Docker is installed::

  $ mkdir Build
  $ cd Build
  $ ../Resources/CreateOHIFDist.sh
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``libOrthancOHIF.so``
that contains the OHIF plugin for Orthanc.

Pre-compiled Linux Standard Base (LSB) binaries `are available for
download <https://lsb.orthanc-server.com/plugin-ohif/>`__.

Pre-compiled binaries for Microsoft Windows and macOS `are also
available
<https://www.orthanc-server.com/browse.php?path=/plugin-ohif>`__.

Furthermore, the :ref:`Docker images <docker>`
``jodogne/orthanc-plugins`` and ``osimis/orthanc`` also contain the
plugin. Debian and Ubuntu packages can be found in the
:ref:`standalone repository <binaries>`
``https://debian.orthanc-labs.com/``.


Configuration
-------------

.. highlight:: json

Here is a minimal sample :ref:`configuration file <configuration>` to
use this plugin::

  {
    "Plugins" : [
      "/home/user/orthanc-ohif/Build/libOHIF.so"
    ]
  }

Orthanc must of course be restarted after the modification of its
configuration file.


Using DICOMweb
^^^^^^^^^^^^^^

By default, the plugin uses the `DICOM JSON data source
<https://v3-docs.ohif.org/configuration/datasources/dicom-json/>`__ of
OHIF. This data source is optimized to provide the fastest access to
the DICOM images, while requiring no additional plugin. However, in
order to deliver fast access, the OHIF plugin will cache additional
information about each DICOM instance in the Orthanc database, which
results in a larger size of the Orthanc database (an additional 1KB is
roughly needed per instance).

It is also possible to enable the `DICOMweb data source
<https://v3-docs.ohif.org/configuration/dataSources/dicom-web>`__. In
this case, the :ref:`DICOMweb plugin of Orthanc <dicomweb>` must also
be loaded. It can also be useful to load the :ref:`GDCM plugin <gdcm>`
if the images use a compressed transfer syntax.

The advantages of using DICOMweb over the default DICOM JSON are:

* More standard-compliant.

* The OHIF study list is accessible, notably as a button on the
  welcome screen of Orthanc Explorer.

* No additional space is used in the Orthanc database.
  
Here is a minimal configuration file to use DICOMweb::

  {
    "Plugins" : [
      "/home/user/orthanc-ohif/Build/libOHIF.so",
      "/home/user/orthanc-dicomweb/Build/libOHIF.so"
    ],
    "OHIF" : {
      "DataSource" : "dicom-web"
    }
  }
  

Router basename
^^^^^^^^^^^^^^^

If Orthanc is not branched at the root of a Web server thanks of the
presence of a reverse proxy, the configuration option
``RouterBasename`` must be adapted.

For instance, if Orthanc is running at address
``https://host.com/imaging/demo/orthanc/``, the following
configuration file must be used for OHIF to work::

  {
    "Plugins" : [
      "/home/user/orthanc-ohif/Build/libOHIF.so"
    ],
    "OHIF" : {
      "RouterBasename" : "/imaging/demo/orthanc/ohif/"
    }
  }

The default value of ``RouterBasename`` is ``/ohif/``.


Preloading
^^^^^^^^^^

