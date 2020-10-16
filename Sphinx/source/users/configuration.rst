.. _configuration:
.. highlight:: bash

Configuration of Orthanc
========================

Configuring Orthanc simply consists in providing a configuration file.
Orthanc has numerous configuration that are documented in the `default
configuration file
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.8.0/OrthancServer/Resources/Configuration.json>`_. This
file is in the `JSON <https://en.wikipedia.org/wiki/JSON>`_ file
format. You can generate this file file with the following call::

    $ Orthanc --config=Configuration.json

The default configuration file would:

* Create a DICOM server with the DICOM AET (Application Entity Title)
  ``ORTHANC`` that listens on the port 4242.
* Create a HTTP server for the REST API that listens on the port 8042.
* Store the Orthanc database in a folder called ``OrthancStorage``.

However, we recommend that you start from an empty configuration file
and only specify the options for which you don't wan't to use
the default value.  In example, a simple configuration file would be::

    {
        "Name": "My archive",
        "HttpPort": 80,
        "DicomAet": "ARCHIVE",
        "DicomPort": 104
    }

It's also a very good practice to split your configuration files per topic.
In example, have a ``dicom.json`` for everything that is related to DICOM,
a ``http.json`` for all HTTP related configurations, one file per plugin...  
This is how the configuration files are provided with the Windows Installer.

Once your configuration file is ready, start Orthanc by giving it the path to the 
configuration file path as a command-line argument.  If you use multiple configuration
files, you may provide the path to the folder containing all configuration files 
(all ``.json`` files will be loaded)::

    $ Orthanc ./Configuration.json
    $ Orthanc ./config/


*Remark:* When specifying paths under Microsoft Windows, backslashes
(i.e. ``\``) should be either escaped by doubling them (as in ``\\``),
or replaced by forward slashes (as in ``/``).
*Remark:* When installing Orthanc with the Windows Installer, you won't be
able to edit your files unless you start your editor with ``Run as administrator``.
We recommend to edit your configuration file with an editor such as `Notepad++ <https://notepad-plus-plus.org/>`_.  
It shall warn you that this file can be edited only by an admin, and will suggest you 
to restart Notepad++ as an admin such that you'll be able to save it.

 
To obtain more diagnostic, you can use the ``--verbose`` or the
``--trace`` options::

    $ Orthanc ./Configuration.json --verbose
    $ Orthanc ./Configuration.json --trace

