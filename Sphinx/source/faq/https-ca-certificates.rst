.. _https-ca-certificates:


How to configure the HttpsCACertificates parameter?
===================================================

In somes cases, Orthanc may have to query some third-party services
thanks to HTTPS requests (distant :ref:`DICOMweb server <dicomweb>`, 
:ref:`object storage <object-storage>`,...).

Orthanc relies on `cURL <https://curl.se/>`_ for such queries.

Starting with Orthanc 1.12.6 and provided that Orthanc has been built with
libcurl > 8.2.0, if ``HttpsCACertificates`` is left empty in the Orthanc
configuration file, Orthanc uses the operating system native CA store to
validate the certificates received from the distant servers (cURL
"--ca-native" option). In most of the setups, this is perfectly fine and 
the servers certificates are validated correctly.

However, one could face some troubles, especially on **Microsoft
Windows** setups.

To fix them, download the CA certificate store (in PEM format) from the
`cURL project <https://curl.haxx.se/docs/caextract.html>`__.

.. highlight:: json

And then, store it on the drive and modify your configuration file according to
(file path to adapt)::

  {
    "HttpsCACertificates" : "C:\\Program Files\\Orthanc Server\\resources\\cacert.pem"
  }


On **GNU/Linux distributions**, you will most probably find a file
named ``ca-certificates.crt`` somewhere within the ``/etc/`` folder.
For instance, on Ubuntu/Debian derivatives::

  {
    "HttpsCACertificates" : "/etc/ssl/certs/ca-certificates.crt"
  }
