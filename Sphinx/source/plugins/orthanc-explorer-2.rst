.. _orthanc-explorer-2:


Orthanc Explorer 2 plugin
=========================

.. contents::

   
Introduction
------------

This plugin provides a new User Interface (UI) to Orthanc.  It aims at being
more user-friendly, more configurable and more evolutive than the default
Orthanc UI which was developed mainly for testing/administrative purpose.

.. image:: ../images/OE2-screenshot-study-list.png
           :align: center
           :width: 1000px

|

Note that a major difference between the legacy UI and Orthanc Explorer 2 (OE2)
is that OE2 works only at the study level, not the patient level.  The main page is
the study list in which, of course, you can apply a filter to display only the studies of a single patient.


How to get it ?
---------------

The source code is available on `GitHub <https://github.com/orthanc-server/orthanc-explorer-2>`__.

Binaries are included in:

- The `osimis/orthanc Docker image <https://hub.docker.com/r/osimis/orthanc>`__
- The `Windows Installer <https://orthanc.osimis.io/win-installer/OrthancInstaller-Win64-latest.exe>`__ (only for 64bits platform)
- The `MacOS packages <https://orthanc.osimis.io/osx/stable/orthancAndPluginsOSX.stable.zip>`__

Release notes are available `here <https://github.com/orthanc-server/orthanc-explorer-2/blob/master/release-notes.md>`__.

Depending on the configuration, the plugin can replace the default Orthanc UI you are redirected to when accessing orthanc at `http://localhost:8042/ <http://localhost:8042/>`__.
In any case, the new and old UI can coexist:

- Orthanc Explorer 2 is available at `http://localhost:8042/ui/app/ <http://localhost:8042/ui/app/>`__
- Legacy UI remains available at `http://localhost:8042/app/explorer.html <http://localhost:8042/app/explorer.html>`__


Configuration
-------------

.. highlight:: json

The plugin must be configured through a configuration file.  The minimal configuration to include in your orthanc configuration file is::

  "OrthancExplorer2" : {
    "Enable": true,
    "IsDefaultOrthancUI": true
  }

There are many more options that are documented in the 
`default configuration file <https://github.com/orthanc-server/orthanc-explorer-2/blob/master/Plugin/DefaultConfiguration.json>`__.

Main features you can configure:

- Root URL
- Whether OE2 becomes the default Orthanc UI
- Configure the side menu
- Configure the actions available on the resources
- Configure the columns of the main study list


Advanced features
-----------------

You may open the OE2 interface directly on a specific study or patient by specifying DICOM Tags directly in the URL.
e.g::

    http://localhost:8042/ui/app/#/filtered-studies?PatientID=00000169
    http://localhost:8042/ui/app/#/filtered-studies?StudyDate=20220512-20220513&ModalitiesInStudy=CR\DX
    http://localhost:8042/ui/app/#/filtered-studies?StudyInstanceUID=1.2.3
    http://localhost:8042/ui/app/#/filtered-studies?StudyInstanceUID=1.2.3&expand
    http://localhost:8042/ui/app/#/filtered-studies?StudyInstanceUID=1.2.3&expand=study
    http://localhost:8042/ui/app/#/filtered-studies?StudyInstanceUID=1.2.3&expand=series



Roadmap
-------

Main elements of the roadmap are listed hereunder (not in the order of implementation):

- Multiple language support
- Mobile friendly
- Allow edition of DICOM Tags
- Query-retrieve interface for dicom-web servers & remote DICOM servers
- Open other viewers from UI (Radiant, Osirix, MedDream, OHIF, ...)

A full list of `ideas` is stored directly in the repository's `TODO <https://github.com/orthanc-server/orthanc-explorer-2/blob/master/TODO>`__


Bug reports & support
---------------------

As usual, you can get support and report issues from the `Orthanc Users group <https://groups.google.com/g/orthanc-users>`__.

You may also directly introduce bugs or feature requests in `GitHub <https://github.com/orthanc-server/orthanc-explorer-2/issues>`__.

The plugin is currently maintained by Alain Mazy from `Orthanc.team <https://orthanc.team/>`__ who, like many of you, enjoys 
receiving a salary for his work.  Feel free to hire him if you need a specific feature or bug fixed.

Donations to `Open Collective <https://opencollective.com/orthanc>`__ may also be used to maintain/develop this plugin.
