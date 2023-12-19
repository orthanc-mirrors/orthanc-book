.. highlight:: bash
.. _cookbook:

Quickstart
==========

.. contents::
   :depth: 2


.. _binaries:

Obtaining binaries
------------------

To obtain the Orthanc binaries, you have several possibilities:

* `Download pre-compiled packages <https://www.orthanc-server.com/download.php>`__.
* Use ``jodogne/orthanc`` :ref:`Docker images <docker>`.
* Use ``osimis/orthanc`` :ref:`Docker images <docker-osimis>`.
* On GNU/Linux, use precompiled packages for :ref:`Debian/Ubuntu
  <debian-packages>` (courtesy of DebianMed and Sébastien Jodogne), or
  for `openSUSE <https://software.opensuse.org/search?q=orthanc>`__
  (courtesy of Axel Braun).
* On GNU/Linux, use our `LSB binaries
  <https://orthanc.uclouvain.be/downloads/linux-standard-base/index.html>`__ (Linux Standard Base), that
  should easily and immediately run on most distributions. Those
  binaries are statically linked together with all their third-party
  dependencies. Don't forget to execute ``chmod +x ./Orthanc`` in
  order to be able to run the main Orthanc executable.
* :ref:`Compile Orthanc by yourself <compiling>`.
* External contributors are also maintaining `Vagrant VM for Orthanc
  <https://github.com/jodogne/OrthancContributed/blob/master/Links.md#user-content-vagrant>`__.

.. highlight:: bash

Furthermore, if you are running Debian 9 (stretch), Debian 10
(buster), Debian 11 (bullseye), Debian 12 (bookworm), Ubuntu 18.04 LTS
(bionic), Ubuntu 20.04 LTS (focal), or Ubuntu 22.04 LTS (jammy) on an
**AMD64 architecture**, Sébastien Jodogne maintains a **standalone
Debian repository** that provides the latest versions of the LSB
binaries. For instance, here is how to install the :ref:`Stone Web
viewer <stone_webviewer>` on a barebone Docker setup::

  # docker run --rm -t -i -p 8042:8042 -p 4242:4242 debian:9

  $ apt update
  $ DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common wget curl nano gnupg apt-transport-https

  $ apt install --upgrade ca-certificates
  $ wget -qO - https://debian.orthanc-labs.com/archive.key | apt-key add -
  $ apt-add-repository "deb https://debian.orthanc-labs.com/ `grep VERSION_CODENAME /etc/os-release | cut -d'=' -f 2` main"

  $ apt clean && apt update
  $ apt install orthanc-stone-webviewer
  $ /etc/init.d/orthanc start

Note that this standalone Debian repository **does not** contain the
:ref:`Python plugin <python-plugin>` and the :ref:`Java plugin
<java-plugin>`, because these plugins must be dynamically linked
against the system-wide version of your Python or Java runtime
environment. You should install the ``orthanc-python`` or
``orthanc-java`` package from your native Debian/Ubuntu distribution
if available, or compile the plugin from sources.


.. _orthanc-explorer:

Opening Orthanc Explorer
------------------------

The most straightforward way to use Orthanc consists in opening
**Orthanc Explorer**, the embedded administrative interface of
Orthanc, with a Web browser.  Once Orthanc is running, open the
following URL: http://localhost:8042/app/explorer.html. Please note
that:

* The port number 8042 depends on your :ref:`configuration
  <configuration>`.
* Orthanc Explorer does not work with Microsoft Internet
  Explorer. Please use Mozilla Firefox, Google Chrome, Apple Safari,
  or `any WebKit-based Web browser <https://en.wikipedia.org/wiki/WebKit>`__.
 

Uploading DICOM files
---------------------

The Orthanc Explorer interface contains a user-friendly page to upload
DICOM files. You can reach the upload page at
http://localhost:8042/app/explorer.html#upload. Then, you can drag and
drop your DICOM files and click on the Upload button.

You can `watch this video tutorial
<https://www.youtube.com/watch?v=4dOcXGMlcFo&hd=1>`__ that shows how
to upload files to Orthanc through Orthanc Explorer with Chromium.

**Important:** There is currently a `known issue
<https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=21>`__ that might
prevent Mozilla Firefox to correctly upload all DICOM files if using
drag-and-drop.


Uploading through the DICOM protocol
------------------------------------

Once Orthanc is up and running, any imaging modality can send
instances to Orthanc through the DICOM protocol (with the C-Store
command).  Check :ref:`this tutorial <configure-modality>` to 
connect your modality to Orthanc.

You can also use the standard command-line tool ``storescu`` from the
`DCMTK software <https://dicom.offis.de/dcmtk.php.en>`__ to manually
send DICOM images to Orthanc, for instance::

    $ storescu -aec ORTHANC localhost 4242 *.dcm

will send all the files with ".dcm" extension to the instance of
Orthanc that is running on the ``localhost``, whose application entity
title (AET) is ``ORTHANC``, and whose DICOM port is
``4242``. Obviously, all these parameters depend on your
:ref:`configuration <configuration>`. Please check the :ref:`FAQ
<dicom>` if you encounter any problem.


Next steps
----------

1. Read the general introduction ":ref:`dicom-guide`".
2. Have a look at your :ref:`configuration file <configuration>`.
3. Drive Orthanc through its :ref:`REST API <rest>`.
4. Automate DICOM tasks with :ref:`Lua scripts <lua>`.

