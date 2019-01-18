.. _configuration:
.. highlight:: bash

Configuration of Orthanc
========================

Configuring Orthanc simply consists in copying and adapting the
`default configuration file
<https://bitbucket.org/sjodogne/orthanc/raw/Orthanc-1.5.2/Resources/Configuration.json>`_. This
file is in the `JSON <https://en.wikipedia.org/wiki/JSON>`_ file
format. You can generate a sample configuration file with the
following call::

    $ Orthanc --config=Configuration.json

Then, start Orthanc by giving it the path to the modified
Configuration.json path as a command-line argument::

    $ Orthanc ./Configuration.json

The default configuration file would:

* Create a DICOM server with the DICOM AET (Application Entity Title)
  ``ORTHANC`` that listens on the port 4242.
* Create a HTTP server for the REST API that listens on the port 8042.
* Store the Orthanc database in a folder called ``OrthancStorage``.

*Remark:* When specifying paths under Microsoft Windows, backslashes
(i.e. ``\``) should be either escaped by doubling them (as in ``\\``),
or replaced by forward slashes (as in ``/``).

To obtain more diagnostic, you can use the ``--verbose`` or the
``--trace`` options::

    $ Orthanc ./Configuration.json --verbose
    $ Orthanc ./Configuration.json --trace

Starting with Orthanc 0.9.1, you can also start Orthanc with the path
to a directory. In such a case, Orthanc will load all the files with a
``.json`` extension in this directory, and merge them to construct the
configuration file. This allows to split the global configuration into
several files.
