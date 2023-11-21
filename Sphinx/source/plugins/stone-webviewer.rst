.. _stone_webviewer:


Stone Web Viewer plugin
=======================

.. contents::

This plugin extends Orthanc with a Web viewer of medical images, with
more advanced features than the basic :ref:`Orthanc Web viewer plugin
<webviewer>`.

For general information and a demonstration, check out the `official
homepage of the plugin
<https://www.orthanc-server.com/static.php?page=stone-web-viewer>`__.
Also `check out the source code
<https://orthanc.uclouvain.be/hg/orthanc-stone/file/default/Applications/StoneWebViewer>`__.


How to get it
-------------

The Stone Web viewer is part of the `Windows installers
<https://www.orthanc-server.com/download-windows.php>`__ (since
release 20.12.0 of the installers).

For GNU/Linux users, the Stone Web viewer is part of the
:ref:`official Docker images <docker>`. Precompiled LSB binaries
(Linux Standard Base) are `available as well
<https://lsb.orthanc-server.com/stone-webviewer/>`__.

The compilation process is quite complex since it requires using the
`Emscripten <https://emscripten.org/>`__ compiler toolchain. The full
build instructions are available in the `source code
<https://orthanc.uclouvain.be/hg/orthanc-stone/file/StoneWebViewer-2.5/Applications/StoneWebViewer/WebAssembly/NOTES.txt>`__.


Usage
-----

On Microsoft Windows or if you are using the
``jodogne/orthanc-plugins`` :ref:`Docker images <docker>`, the plugin
is enabled by default and will work out-of-the-box.

.. highlight:: bash

The ``osimis/orthanc`` :ref:`Docker images <docker-osimis>` are more
suited to devops needs, as they allow to start a minimal Docker
environment as follows::

  $ docker run -p 4242:4242 -p 8042:8042 -e STONE_WEB_VIEWER_PLUGIN_ENABLED=true -e DICOM_WEB_PLUGIN_ENABLED=true --rm osimis/orthanc:21.6.2


.. highlight:: json

On plain GNU/Linux distributions (i.e. if not using Docker), the Stone
Web viewer will only work with the LSB binaries (Linux Standard Base)
of the Orthanc server that can be downloaded from `here
<https://lsb.orthanc-server.com/orthanc/>`__ (this setup will work
with most recent GNU/Linux distributions). The Stone Web viewer also
requires the `DICOMweb plugin
<https://lsb.orthanc-server.com/plugin-dicom-web/>`__ to be installed.

Once the binaries are installed, you must change the
:ref:`configuration file <configuration>` to tell Orthanc where it can
find the plugin: This is done by properly modifying the ``Plugins``
option. You could for instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/xxx/Downloads/libStoneWebViewer.so",
      "/home/user/xxx/Downloads/libOrthancDicomWeb.so"
    ]
  }

.. highlight:: text

Orthanc must of course be restarted after the modification of its
configuration file. 

Once a :ref:`DICOM study <model-world>` is opened using Orthanc
Explorer, a yellow button entitled ``Stone Web Viewer`` will show
up. It will open the Web viewer for that particular study.  See also
the interactive demonstration on the `official homepage of the plugin
<https://www.orthanc-server.com/static.php?page=stone-web-viewer>`__.

Advanced options
----------------

* The configuration of the Web viewer can be fine-tuned by adapting
  some **advanced options** in the `configuration file
  <https://orthanc.uclouvain.be/hg/orthanc-stone/file/StoneWebViewer-2.5/Applications/StoneWebViewer/WebApplication/configuration.json>`__.

* The source distribution of the Stone Web viewer contains a
  `NOTES.txt file
  <https://orthanc.uclouvain.be/hg/orthanc-stone/file/StoneWebViewer-2.5/Applications/StoneWebViewer/NOTES.txt>`__
  that discusses the differences with the :ref:`Osimis Web viewer
  <osimis_webviewer>` as well as **advanced features** of the software
  (opening multiple studies, authorization, display of OsiriX
  annotations...).

* Also, check out our `TODO file
  <https://orthanc.uclouvain.be/hg/orthanc-stone/file/default/TODO>`__
  that is used to track **future features**.
   

.. _stone_webviewer_troubleshooting:

Troubleshooting
---------------

- `Some users
  <https://groups.google.com/g/orthanc-users/c/RfQJFgkOUYY/m/d1uGW7APBgAJ>`__
  have reported that some versions of Google Chrome and Chromium (in
  particular release 97.0.4692.71) don't properly support
  **drag-and-drop**. This is *not* an issue in Stone Web viewer, but
  an issue in Chrome/Chromium (cf. `issue 1284605
  <https://bugs.chromium.org/p/chromium/issues/detail?id=1284605>`__).
  This problem can be overcome in 3 different ways:

  1. Upgrade your Web browser (releases >= 98.0.x should run fine).

  2. Replace drag-and-drop by clicking on the "drop a series here"
     area, then clicking on the series you want to load.

  3. Disable the option "Use system title bar and borders" in the
     settings of Chrome/Chromium, as depicted in the following
     screenshot:
     
     .. image:: ../images/stone-webviewer-google-issue.png
           :align: center
           :width: 800


FAQ
---

- **Can I use the Stone Viewer in a medical environment?**

  The Stone Viewer is not a Medical Device; it is not CE marked or FDA
  approved. The Stone Viewer is free and open-source software that
  cannot be used for diagnostic or therapeutic purposes.

  However, the viewer can be used as a communication tool that allows
  researchers, teachers, technicians, medical physicists, general
  practitioner or patients to visualize medical images for information
  only.

  Check out your local regulations to ensure you're using it in a
  legal manner.

- **Can the Stone Web Viewer display DICOM-SR (structured reports)?**

  The Stone Web viewer doesn't provide built-in support for
  DICOM-SR. However, it can display DICOM-SR that have been beforehand
  converted to PDF.

  To this end, you could for instance first use the ``dsr2html``
  command-line tool that is provided by the `DCMTK project
  <https://support.dcmtk.org/docs/mod_dcmsr.html>`__ to convert the
  structured report to HTML, then use a HTML-to-PDF converter such as
  `wkhtmltopdf <https://wkhtmltopdf.org/>`__, and finally convert the
  PDF to DICOM using the ``/tools/create-dicom`` route in the `REST
  API of Orthanc
  <https://orthanc.uclouvain.be/api/index.html#tag/System/paths/~1tools~1create-dicom/post>`__.
  It would be easy to automate this workflow using a :ref:`Python
  plugin <python-plugin>`.

  If you have an interest in DICOM-SR, the Orthanc community would
  love to have access to sample DICOM files that could be used to
  enhance the support of structured reports in the Stone Web viewer.
  If you have such sample files, please post them to the `Orthanc
  Users <https://groups.google.com/g/orthanc-users>`__ discussion
  forum.

- **What video formats are supported by the Stone Web Viewer?**

  The set of codecs supported by the Stone Viewer is an intersection
  of the sets of codecs supported by the `DICOM standard
  <http://dicom.nema.org/medical/dicom/current/output/chtml/part05/PS3.5.html>`__
  and those supported by the `web browsers
  <https://developer.mozilla.org/en-US/docs/Web/Media/Formats>`__.
  In short, this mostly comes down to just MPEG-4.

  Note that video playing is not supported using the plain DICOMweb
  protocol: The Stone Web viewer will use the :ref:`REST API of
  Orthanc <rest>` to play videos.
  
- **How do Osimis Web viewer and Stone Web viewer compare?**

  The two viewers use a very similar user interface. However, their
  internal architecture is totally different:

  - Stone Web viewer is a combination of C++, :ref:`Stone of Orthanc
    <stone>`, WebAssembly, DICOMweb and Vue.js.

  - Osimis Web viewer is a combination of JavaScript, `Cornerstone
    <https://cornerstonejs.org/>`__, :ref:`Orthanc REST API <rest>`
    and Angular.
    
  The Osimis Web viewer is deprecated and superseded by the Stone Web
  viewer, as the Stone of Orthanc library allows to use a single C++
  codebase between mobile apps, desktop software and Web applications.

  Some features from the Osimis Web viewer are not available (yet),
  such as creating custom annotations or the Live Share feature.

- **How can I migrate from Osimis Web viewer to Stone Web viewer?**

  Full instructions are provided in the `source distribution
  <https://orthanc.uclouvain.be/hg/orthanc-stone/file/StoneWebViewer-2.5/Applications/StoneWebViewer/NOTES.txt>`__.

- **What are the future plans?**

  The internal use of :ref:`Stone of Orthanc library <stone>` gives us
  a lot of flexibility to implement new advanced features, such as 3D
  rendering (MPR, reslicing, image fusion...), DICOM-RT support,
  storage of annotations/measurements, viewer for mobile devices,
  internationalization (translation)...

  We are looking for :ref:`industrial sponsors <contributing>` to
  implement such new features in the Stone Web viewer.
