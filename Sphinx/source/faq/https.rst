.. highlight:: bash
.. _https:

HTTPS encryption with Orthanc
=============================

It is highly desirable to enable HTTPS (SSL) encryption with Orthanc
to protect its REST API, as it provides access to medical
information. To this end, you have two possibilites:

1. Put Orthanc behind an enterprise-ready HTTPS server such as
   :ref:`Apache <apache>`, :ref:`nginx <nginx>` or :ref:`Microsoft IIS <iis>`.
2. For simple deployments, use Orthanc :ref:`built-in HTTPS server <https-builtin>`.

**You should always favor the first option**. The second option might make
sense in the context of an hospital Intranet, i.e. the Orthanc server
is not publicly accessible from the Internet.


.. _https-builtin:

Built-in encryption
-------------------

To enable the built-in HTTP server of Orthanc, you need to:

1. Obtain a `X.509 certificate <https://en.wikipedia.org/wiki/X.509>`_
   in the `PEM format
   <https://en.wikipedia.org/wiki/X.509#Certificate_filename_extensions>`_.
2. Prepend this certificate with the content of your private key. 
3. Modify the ``SslEnabled`` and ``SslCertificate`` variables in the
   :ref:`Orthanc configuration file <configuration>`.

Here are simple instructions to create a self-signed SSL certificate
that is suitable for test environments with the `OpenSSL
<https://en.wikipedia.org/wiki/Openssl>`_ command-line tools::

    $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out certificate.crt
    $ cat private.key certificate.crt > certificate.pem

Some interesting references about this topic can be found `here
<http://www.devsec.org/info/ssl-cert.html>`__, `here
<http://www.akadia.com/services/ssh_test_certificate.html>`__, and
`here
<http://stackoverflow.com/questions/991758/how-to-get-an-openssl-pem-file-from-key-and-crt-files>`__.
