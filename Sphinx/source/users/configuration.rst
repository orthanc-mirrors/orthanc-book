.. _configuration:

Configuration of Orthanc
========================

.. highlight:: bash

Configuring Orthanc simply consists in providing a configuration file.
Orthanc has numerous configuration that are documented in the `default
configuration file
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.5/OrthancServer/Resources/Configuration.json>`_. This
file is in the `JSON <https://en.wikipedia.org/wiki/JSON>`_ file
format. You can generate this file file with the following call::

    $ Orthanc --config=Configuration.json

The default configuration file would:

* Create a DICOM server with the DICOM AET (Application Entity Title)
  ``ORTHANC`` that listens on the port 4242.
* Create a HTTP server for the REST API that listens on the port 8042.
* Store the Orthanc database in a folder called ``OrthancStorage``.

.. highlight:: json

However, we recommend that you start from an empty configuration file
and only specify the options for which you don't wan't to use
the default value.  In example, a simple configuration file would be::

    {
        "Name": "My archive",
        "HttpPort": 80,
        "DicomAet": "ARCHIVE",
        "DicomPort": 104
    }

It's also a very good practice to split your configuration files per
topic.  In example, have a ``dicom.json`` for everything that is
related to DICOM, a ``http.json`` for all HTTP related configurations,
one file per plugin.  This is how the configuration files are provided
with the Windows Installer.

.. highlight:: bash

Once your configuration file is ready, start Orthanc by giving it the path to the 
configuration file path as a command-line argument.  If you use multiple configuration
files, you may provide the path to the folder containing all configuration files 
(all ``.json`` files will be loaded)::

    $ Orthanc ./Configuration.json
    $ Orthanc ./config/


**Remark 1:** When specifying paths under Microsoft Windows,
backslashes (i.e. ``\``) should be either escaped by doubling them (as
in ``\\``), or replaced by forward slashes (as in ``/``).

**Remark 2:** When installing Orthanc using the `official Windows
installers <https://www.orthanc-server.com/download-windows.php>`__,
you won't be able to edit your files unless you start your editor with
``Run as administrator``. We recommend to edit your configuration file
with an editor such as `Notepad++ <https://notepad-plus-plus.org/>`_.
It shall warn you that this file can be edited only by an admin, and
will suggest you to restart Notepad++ as an admin such that you'll be
able to save it.

**Remark 3:** The official Windows installers include a `Windows
service <https://en.wikipedia.org/wiki/Windows_service>`__ that
automatically starts Orthanc during the startup of Microsoft
Windows. You can control the parameters of the service by typing
``services.msc`` at a command-line prompt. The Windows service of
Orthanc will do its best to cleanly stop Orthanc at the shutdown of
Windows, but `there are some caveats
<https://orthanc.uclouvain.be/bugs/show_bug.cgi?id=48>`__.
 
**Remark 4:** To obtain more diagnostic, you can use the ``--verbose``
or the ``--trace`` options::

    $ Orthanc ./Configuration.json --verbose
    $ Orthanc ./Configuration.json --trace

To learn more about the Orthanc logs, :ref:`check out the dedicated
page <log>`.


.. _orthanc-environment-variables:

Environment variables
---------------------

.. highlight:: json

Starting with Orthanc 1.5.0, the configuration file can include the
value of environment variables. Consider the following configuration::

  {
    "Name" : "${ORTHANC_NAME}"
  }


.. highlight:: bash

In this case, once Orthanc starts, the configuration option ``Name``
will be read from the value of the environment variable
``ORTHANC_NAME``. For instance::

  $ ORTHANC_NAME=Hello ./Orthanc Configuration.json
  $ curl http://localhost:8042/system
  {
    "Name" : "Hello",
    [...]
  }


.. highlight:: json

It is also possible to set a default value if the environment variable
is not set. Here is the syntax in the configuration file::

  {
    "Name" : "${ORTHANC_NAME:-DefaultName}"
  }


.. highlight:: bash

If the environment variable ``ORTHANC_NAME`` is not set, here is the
result::

  $ ./Orthanc Configuration2.json
  $ curl http://localhost:8042/system
  {
    "Name" : "DefaultName",
    [...]
  }
