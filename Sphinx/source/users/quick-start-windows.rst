.. _quick-start-windows:

Quickstart Guide for Windows
============================

Orthanc is a lightweight, open-source DICOM server ideal for medical imaging professionals. This guide will help you quickly set up and run Orthanc on a Windows machine.

Step 1: Download Orthanc
------------------------

1. **Visit the Orthanc Website**

   Navigate to the `Orthanc downloads website <https://www.orthanc-server.com/download-windows.php>`_.

2. **Download the Windows Installer**

   Identify your OS version 64 or 32 bits (note: very likely 64 bits) and download the latest version of the Orthanc installer (``.exe`` file).

Step 2: Install Orthanc
-----------------------

1. **Run the Installer**
   Locate the downloaded installer file and double-click it to start the installation process.  Note that the installer is not signed and you might
   have to click on ``More info`` and ``Run anyway``

.. image:: ../images/win-quick-start-protect.png
           :align: center
           :width: 60%

2. **Follow the Installation Wizard**

* Accept the license agreement.
* Choose the installation directory (default ``C:\Program Files\Orthanc Server`` is usually fine).
* Select the folder in which Orthanc will store its data files (default ``C:\Orthanc`` is usually fine).
* Select the plugins to install.  Although you might not need all of them, they are all selected by default and this is fine : plugins that are not explicitly enabled do not consume any resources.
* Complete the installation by following the prompts.

.. image:: ../images/win-quick-start-inst.png
           :align: center
           :width: 40%

Step 3: Orthanc is running !
----------------------------

At this stage, Orthanc is running as a Windows Service which means that it will start everytime your Windows machine starts.

Orthanc User Interface is accessible at `http://localhost:8042/ui/app/ <http://localhost:8042/ui/app/>`_.  Orthanc is currently empty

.. image:: ../images/win-quick-start-orthanc-empty.png
           :align: center
           :width: 80%

Step 4: Upload and view your first DICOM images !
-------------------------------------------------

The easiest way to feed Orthanc with DICOM images is through the ``upload`` menu of the User interface.

.. image:: ../images/win-quick-start-orthanc-upload.png
           :align: center
           :width: 40%

Once this is done, your DICOM images will appear in the Study List and you'll be able to browse them and visualize them with one of the pre-installed viewers.
Remember that we have installed all plugins ?  Therefore, you'll have the choice between 4 viewers:

* The :ref:`Stone Web viewer <stone_webviewer>`
* The :ref:`OHIF viewer <ohif>`
* :ref:`Volview <volview>`

.. image:: ../images/win-quick-start-orthanc-study-list.png
           :align: center
           :width: 80%

Step 5: Configure Orthanc
-------------------------

Orthanc is configured through a `JSON <https://en.wikipedia.org/wiki/JSON>`__ configuration file and comes with a default configuration that is suitable for quick testing. 
However, at some point, you might probably need to customize the settings.

1. **Locate the Configuration Files**

   The Windows configuration is split under multiple configuration files and are typically stored in ``C:\Program Files\Orthanc\Configuration\``.
   ``orthanc.json`` is the main configuration file.  Its complete documentation is available `here <https://orthanc.uclouvain.be/hg/orthanc/file/tip/OrthancServer/Resources/Configuration.json>`__.
   Each :ref:`plugin <plugins>` has its own configuration file documented in the plugin documentation.

.. image:: ../images/win-quick-start-config-files.png
            :align: center
            :width: 40%

2. **Edit the Configuration File**

   To edit a configuration file, you must start your editor with ``Run as administrator``.  
   We recommend to edit your configuration file with an editor such as `Notepad++ <https://notepad-plus-plus.org/>`_.
   It shall warn you that this file can be edited only by an admin, and will suggest you to restart Notepad++ as an admin such that you'll be
   able to save it.

   Configure settings such as:
   
   * **HTTP Server Port**: ``"HttpPort": 8042`` (default is 8042)
   * **DICOM Server Port**: ``"DicomPort": 4242`` (default is 4242)
   * **Database Storage Path**: ``"StorageDirectory": "OrthancStorage"``
   Save your changes.

   **Remark 1:** When specifying paths under Microsoft Windows,
   backslashes (i.e. ``\``) should be either escaped by doubling them (as
   in ``\\``), or replaced by forward slashes (as in ``/``).

   **Remark 2:** In JSON, every ``{}`` and every ``,`` counts !  Orthanc will refuse to
   start if the file is not in a valid JSON format.  There are numerous online JSON validators to validate your
   JSON.

3. **Restart Orthanc service**

   To take the configuration changes into account, Orthanc must be restarted.  This is done through the
   ``services`` panel (type the ``Windows`` key and search for ``services``).  Locate Orthanc and right click ``Restart``


.. image:: ../images/win-quick-start-services.png
            :align: center
            :width: 70%

4. **Check it is running correctly**

   Open the User Interface at `http://localhost:8042/ui/app/ <http://localhost:8042/ui/app/>`_ to validate that Orthanc is running correctly after your changes.
   If not, you should check the :ref:`Orthanc logs <log>` in ``C:\\Program Files\\Orthanc Server\\Logs``.


Next steps
----------

Now that you know how to configure Orthanc, here are a few suggested sections to continue your exploration:

* :ref:`Connect Orthanc to a DICOM modality <configure-modality>`
* Connect a DICOMWeb client e.g. :ref:`Osirix <integrate-osirix-using-dicomweb>`
* Learn to use the Orthanc Rest API :ref:`Rest API <rest>`
* Start to customize Orthanc through :ref:`Lua scripting <lua>`
* Extend Orthanc through a :ref:`Python plugin <python-plugin>`
* And learn much more by reading the :ref:`Orthanc book <orthanc-book>`