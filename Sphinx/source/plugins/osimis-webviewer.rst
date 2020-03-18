.. _osimis_webviewer:


Osimis Web Viewer plugin
========================

.. contents::

This plugin by Osimis extends Orthanc with a Web viewer of medical
images, with more advanced features than the basic :ref:`Orthanc Web
viewer plugin <webviewer>`. The Osimis plugin adds tools for
measuring, for viewing multiple series, and for split-pane.

For general information, check out the `official homepage of the
plugin
<http://www.orthanc-server.com/static.php?page=osimis-web-viewer>`__.
Also `check out the source code
<https://bitbucket.org/osimis/osimis-webviewer-plugin>`__.


How to get it
-------------

The Osimis Web viewer is part of the `Windows installers
<https://www.orthanc-server.com/download-windows.php>`__.

For Linux users, you'll find it in the `osimis/orthanc <https://hub.docker.com/repository/docker/osimis/orthanc>`__ 
docker images or you can download the LSB binary `here <http://orthanc.osimis.io/lsb/plugin-osimis-webviewer/releases/1.3.1/libOsimisWebViewer.so>`__.

The compilation process is quite complex since it requires to build
first the frontend and then the backend.  All information can be found
in the `source code
<https://bitbucket.org/osimis/osimis-webviewer-plugin>`__.


Usage
-----

.. highlight:: json

On Windows, the plugin is enabled by default.

If you're using the ``osimis/orthanc`` docker image, you'll have
to define the WVB_ENABLED `environment variable <https://osimis.atlassian.net/wiki/spaces/OKB/pages/26738689/How+to+use+osimis+orthanc+Docker+images#Howtouseosimis/orthancDockerimages?-OsimisWebViewer>`__.
to ``true``

On Linux, the Osimis Web viewer will only work with LSB orthanc binaries
that can be downloaded from `here <https://lsb.orthanc-server.com/>`__ and
that will work with most recent Linux distros.

Once Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/xxx/Downloads/libOsimisWebViewer.so"
    ]
  }

.. highlight:: text

Orthanc must of course be restarted after the modification of its
configuration file. 

Once a :ref:`DICOM study <model-world>` is opened using Orthanc
Explorer, a yellow button entitled ``Osimis Web Viewer`` will show
up. It will open the Web viewer for that particular study.  See also
the demonstration video on `official homepage of the plugin
<https://www.orthanc-server.com/static.php?page=osimis-web-viewer>`__.

Advanced options
----------------

.. highlight:: json

The configuration of the Web viewer can be fine-tuned by adding some in
the `configuration file <https://bitbucket.org/osimis/osimis-webviewer-plugin/src/master/doc/default-configuration.json>`__.

FAQ
---

- **Can I use the Osimis Viewer in a medical environment ?**

  The Osimis Viewer is not CE marked or FDA approved and can not be used to produce a diagnostic.
  However, the viewer can be used by:

  - Patients
  - General practioner to explain a pathology to their patients
  - Technicians to check the content/quality of studies
  - Researchers
  - Teachers
  
  Check your local regulations to ensure you're using it in a legal manner.

- **What video formats are supported by the Osimis Web Viewer ?**

  The set of codecs supported by the Osimis Viewer is an intersection of the sets of codecs supported by 
  the `DICOM standard <http://dicom.nema.org/medical/dicom/current/output/chtml/part05/PS3.5.html>`__ 
  and those supported by the `web browsers <https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats>`__.
  In short, this mostly comes down to just MPEG-4.
  
- **Where are the annotations stored ?**

  Annotations are stored in :ref:`metadata <metadata>` (id ``9999``) in a custom format.  Note that annotation 
  storage is disabled by default and can be enabled by setting ``"AnnotationStorageEnabled": true``
  in the configuration file.

