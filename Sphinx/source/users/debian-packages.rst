.. _debian-packages:
.. highlight:: bash


Orthanc packages for Debian/Ubuntu
==================================

.. contents::
   :depth: 3


Introduction
------------

Orthanc is available as an official `Debian package
<https://packages.debian.org/search?keywords=orthanc&searchon=names&exact=1&suite=all&section=all>`__
that is continuously updated by the Orthanc core developers in the
`Debian Sid/unstable distribution
<https://wiki.debian.org/DebianUnstable>`__. This implies that Orthanc
is also available in the `Debian derivative distributions
<https://en.wikipedia.org/wiki/List_of_Linux_distributions#Debian-based>`__,
most notably in `Ubuntu
<https://packages.ubuntu.com/search?keywords=orthanc&searchon=names&suite=all&section=all>`__. Most
of the official plugins are also available as separate packages.

Note that the installed versions depend on the version of the Debian
distribution. If you absolutely need the latest Orthanc version, you
should:

* Use the bleeding-edge `Debian unstable
  <https://wiki.debian.org/DebianUnstable>`__, or use a Debian-based
  distro that derives from unstable (such as Kali Linux).

* Use the `LSB binaries <https://orthanc.uclouvain.be/downloads/linux-standard-base/index.html>`__.

* Use ``jodogne/orthanc`` :ref:`Docker images <docker>`.

* Use ``orthancteam/orthanc`` :ref:`Docker images <docker-orthancteam>`.

* :ref:`Compile Orthanc by yourself <compiling>`.

* Advanced users: :ref:`replace the binaries from the package by the
  LSB binaries <lsb-replace-debian-binaries>`.


**Note about backporting:** Bringing a new version of Orthanc to an
older Ubuntu/Debian release (typically, a LTS release) is known as
"backporting". The process for initiating a backport in `Ubuntu
<https://wiki.ubuntu.com/UbuntuBackports>`__ or in `Debian
<https://backports.debian.org/>`__ is publicly available, but the core
developers of Orthanc will not do this packaging task by themselves
because of a limited bandwidth: You are kindly invited to contribute!
  

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

.. _lsb-replace-debian-binaries:

If you're stuck with an old version of Orthanc, you may try to
replace the binaries by the LSB binaries.  Note that there might
be some inconsistencies between the plugins version and you should 
do that at your own risk.

This can be done with this sequence of commands::

  $ sudo service orthanc stop
  $ sudo wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/1.12.10/Orthanc --output-document /usr/sbin/Orthanc
  $ sudo chmod +x /usr/sbin/Orthanc
  $ sudo rm -f /usr/share/orthanc/plugins/*.so
  $ sudo wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/1.12.10/libServeFolders.so --output-document /usr/share/orthanc/plugins/libServeFolders.so
  $ sudo wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/1.12.10/libModalityWorklists.so --output-document /usr/share/orthanc/plugins/libModalityWorklists.so
  $
  $ sudo wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc-dicomweb/1.20/libOrthancDicomWeb.so --output-document /usr/share/orthanc/plugins/libOrthancDicomWeb.so
  $ ...
  $ sudo service orthanc restart

