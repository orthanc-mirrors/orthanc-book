.. _debian-packages:
.. highlight:: bash


Orthanc packages for Debian/Ubuntu
==================================

.. toctree::
   :hidden:

   docker-osimis.rst
   

.. contents::
   :depth: 3


Introduction
------------

Orthanc is available as offical `Debian 
<https://packages.debian.org/search?keywords=orthanc&searchon=names&exact=1&suite=all&section=all>`__
and `Ubuntu 
<https://packages.ubuntu.com/search?keywords=orthanc&searchon=names&suite=all&section=all>`__
packages.  Most of the official plugins are also available as separate packages.

Note that the installed versions depend on the OS version.  If you absolutely need 
the latest Orthanc version, you should:

* Use the latest `unstable Debian release <https://wiki.debian.org/DebianUnstable>`__.

* Use the `LSB binaries <https://lsb.orthanc-server.com/>`__.

* Use :ref:`Docker <docker>`.

* :ref:`Compile Orthanc by yourself <compiling>`.

* Advanced users: :ref:`replace the binaries from the package by the LSB binaries <replace-binaries>`.

Installation
------------

Prerequisite: make sure to update your package definition before installing::

  $ sudo apt update

To install Orthanc and its plugins::

  $ sudo apt install orthanc
  $ sudo apt install orthanc-dicomweb
  $ sudo apt install orthanc-gdcm
  $ sudo apt install orthanc-imagej
  $ sudo apt install orthanc-mysql
  $ sudo apt install orthanc-postgresql
  $ sudo apt install orthanc-python
  $ sudo apt install orthanc-webviewer
  $ sudo apt install orthanc-wsi

Starting/Stopping the service
-----------------------------

Once installed, Orthanc is started as a service.  To start/stop/restart, use::

  $ sudo service orthanc start
  $ sudo service orthanc stop
  $ sudo service orthanc restart


Accessing the logs
------------------

:ref:`Logs <log>` are available in ``/var/log/orthanc/``.


Configuration
-------------

Orthanc reads its :ref:`configuration file
<configuration>` from the ``/etc/orthanc/`` folder.



Replacing the package from the service by the LSB binaries
----------------------------------------------------------

.. _replace-binaries:

If you're stuck with an old version of Orthanc, you may try to
replace the binaries by the LSB binaries.  Note that there might
be some inconsistencies between the plugins version and you should 
do that at your own risk.

This can be done with this sequence of commands::

  $ sudo service orthanc stop
  $ sudo wget https://lsb.orthanc-server.com/orthanc/1.8.0/Orthanc --output-document /usr/sbin/Orthanc
  $ sudo rm -f /usr/share/orthanc/plugins/*.so
  $ sudo wget https://lsb.orthanc-server.com/orthanc/1.8.0/libServeFolders.so --output-document /usr/share/orthanc/plugins/libServeFolders.so
  $ sudo wget https://lsb.orthanc-server.com/orthanc/1.8.0/libModalityWorklists.so --output-document /usr/share/orthanc/plugins/libModalityWorklists.so
  $
  $ sudo wget https://lsb.orthanc-server.com/plugin-dicom-web/1.3/libOrthancDicomWeb.so --output-document /usr/share/orthanc/plugins/libOrthancDicomWeb.so
  $ ...
  $ sudo service orthanc restart

