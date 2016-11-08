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

* :ref:`Compile Orthanc by yourself <compiling>`.
* `Download pre-compiled packages <http://www.orthanc-server.com/download.php>`__.
* :ref:`Use Docker <docker>`.
* External contributors are also maintaining `Vagrant VM for Orthanc
  <https://github.com/jodogne/OrthancContributed/blob/master/Links.md#vagrant>`__.


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
<https://bitbucket.org/sjodogne/orthanc/issues/21/dicom-files-missing-after-uploading-with>`__
that prevents Mozilla Firefox to correctly upload all DICOM files.


Uploading through the DICOM protocol
------------------------------------

Once Orthanc is up and running, any imaging modality can send
instances to Orthanc through the DICOM protocol (with the C-Store
command).

You can use the standard command-line tool ``storescu`` from the
`DCMTK software <http://dicom.offis.de/dcmtk.php.en>`__ to 
manually send DICOM images to Orthanc, for instance::

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

