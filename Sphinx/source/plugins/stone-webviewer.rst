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
<https://hg.orthanc-server.com/orthanc-stone/file/default/Applications/StoneWebViewer>`__.


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
<https://hg.orthanc-server.com/orthanc-stone/file/StoneWebViewer-2.2/Applications/StoneWebViewer/WebAssembly/NOTES.txt>`__.


Usage
-----

On Microsoft Windows or if you are using the
``jodogne/orthanc-plugins`` :ref:`Docker images <docker>`, the plugin
is enabled by default and will work out-of-the-box.

.. highlight:: bash

The ``osimis/orthanc`` :ref:`Docker images <docker-osimis>` are more
suited to devops need, as they allow to start a minimal Docker
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

.. highlight:: json

The configuration of the Web viewer can be fine-tuned by adapting some
options in the `configuration file
<https://hg.orthanc-server.com/orthanc-stone/file/StoneWebViewer-2.2/Applications/StoneWebViewer/WebApplication/configuration.json>`__.


.. _stone_webviewer_troubleshooting:

Troubleshooting
---------------

- Users have reported that some versions of Google Chrome and Chromium
  (notably from the family of releases 97.0.x) don't properly support
  **drag-and-drop**. If drag-and-drop doesn't work, upgrade your Web
  browser. You can also replace drag-and-drop by clicking on the "drop a
  series here" area, then clicking on the series you want to load.


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
  <https://hg.orthanc-server.com/orthanc-stone/file/StoneWebViewer-2.2/Applications/StoneWebViewer/NOTES.txt>`__.

- **What are the future plans?**

  The internal use of :ref:`Stone of Orthanc library <stone>` gives us
  a lot of flexibility to implement new advanced features, such as 3D
  rendering (MPR, reslicing, image fusion...), DICOM-RT support,
  storage of annotations/measurements, viewer for mobile devices,
  internationalization (translation)...

  We are looking for :ref:`industrial sponsors <contributing>` to
  implement such new features in the Stone Web viewer.
