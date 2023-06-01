.. _https:

HTTPS encryption with Orthanc
=============================

.. contents::

Overview
--------

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

**Warning:** If you have installed Orthanc using the official package
of a GNU/Linux distribution of the Debian family (such as Ubuntu),
make sure that the ``libssl-dev`` package is installed. Otherwise,
Orthanc will fail to start with the error message ``The TCP port of
the HTTP server is privileged or already in use``. This is because
Civetweb (the embedded HTTP server of Orthanc) cannot find the
``/usr/lib/x86_64-linux-gnu/libcrypto.so`` shared library (`reference
<https://groups.google.com/g/orthanc-users/c/5N1K9iniBoA/m/EXiYrKt3BQAJ>`__).

        
Examples
--------

Securing Orthanc using self-signed certificate
..............................................
        
.. highlight:: bash
               
Here are instructions to create a simple self-signed SSL certificate
that is suitable for test environments thanks to the `OpenSSL
<https://en.wikipedia.org/wiki/Openssl>`_ command-line tools::

    $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/private.key -out /tmp/certificate.crt
    $ cat /tmp/private.key /tmp/certificate.crt > /tmp/certificate.pem

**Important:** While invoking ``openssl``, make sure to set the option
``Common Name (e.g. server FQDN or YOUR name)`` to the name of your
server. For testing on your local computer, you would set this option
to value ``localhost``.

The file ``/tmp/certificate.crt`` can be publicly distributed. The
files ``/tmp/private.key`` and ``/tmp/certificate.pem`` must be kept
secret and must be stored securely.
    
Some interesting references about generating self-signed certificates
can be found `here <http://www.devsec.org/info/ssl-cert.html>`__,
`here <https://www.akadia.com/services/ssh_test_certificate.html>`__,
and `here
<https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files>`__.

.. highlight:: json
               
Once the certificate is generated, you can start Orthanc using the
following minimal configuration file::

  {
    "SslEnabled" : true,
    "SslCertificate" : "/tmp/certificate.pem"
  }      


Querying Orthanc using HTTPS
............................

.. highlight:: txt

If you contact Orthanc using a HTTP client, you will see that
encryption is enabled::

  $ curl http://localhost:8042/studies
  curl: (52) Empty reply from server

Nothing is returned from the Orthanc server using the HTTP protocol,
as it must contacted using the HTTPS protocol. You have to provide the
``https`` prefix::
  
  $ curl https://localhost:8042/studies
  curl: (60) SSL certificate problem: self signed certificate
  More details here: https://curl.haxx.se/docs/sslcerts.html

  curl failed to verify the legitimacy of the server and therefore could not
  establish a secure connection to it. To learn more about this situation and
  how to fix it, please visit the web page mentioned above.

The HTTPS client now complains, as it was not provided with our
self-signed certificate. For the query to succeed, you must provide
the public certificate ``/tmp/certificate.crt`` that was generated
above to the HTTPS client::

  $ curl --cacert /tmp/certificate.crt https://localhost:8042/studies
  [ "66c8e41e-ac3a9029-0b85e42a-8195ee0a-92c2e62e" ]
  
  
Configuring Orthanc peers
.........................

.. highlight:: json

Let us configure a second instance of Orthanc on the localhost that
will act as a client (i.e., an :ref:`Orthanc peer <peers>`) to the
HTTPS-protected Orthanc server. One would create the following
configuration file::

  {
    "HttpPort" : 8043,
    "DicomPort" : 4343,
    "OrthancPeers" : {
      "https" : [ "https://localhost:8042/" ]
    }
  }


.. highlight:: bash

The values of the ``HttpPort`` and ``DicomPort`` options are set to
non-default values in order to avoid a collision with the
HTTPS-protected Orthanc. Let us now trigger a query from our Orthanc
client to the Orthanc server using the REST API of the Orthanc
client::

  $ curl http://localhost:8043/peers/https/system
  {
    "Details" : "libCURL error: Problem with the SSL CA cert (path? access rights?)",
    "HttpError" : "Internal Server Error",
    "HttpStatus" : 500,
    [...]
  }

.. highlight:: json

Just like the cURL command-line client, the Orthanc client complains
about the fact it wasn't provided with the HTTPS public certificate.
The certificate must be provided by adapting the configuration file as
follows::

 {
    "HttpPort" : 8043,
    "DicomPort" : 4343,
    "HttpsCACertificates" : "/tmp/certificate.crt",
    "OrthancPeers" : {
      "https" : [ "https://localhost:8042/" ]
    }
  }


.. highlight:: bash

Using this new configuration, the query will succeed::

  $ curl http://localhost:8043/peers/https/system
  {
    "ApiVersion" : 6,
    "DicomAet" : "ORTHANC",
    "DicomPort" : 4242,
    "HttpPort" : 8042,
    [...]
  }


Securing Orthanc peers with mutual TLS authentication
.....................................................
        
.. highlight:: json
               
Once HTTPS is enabled, Orthanc can also be configured to accept incoming
connections based on a certificate provided by the client.

Server side, this is configured via::

  {
    "SslVerifyPeers": true,
    "SslTrustedClientCertificates": "trustedClientCertificates.pem"
  }

``SslTrustedClientCertificates`` shall contain a list of certificates
that are trusted.  This can be a list of individual self-signed certificates
or this can contain a list of trusted root CAs.

Client side, this is configured via::

  {
    "OrthancPeers" : {
      "orthanc-b" : {
        "Url" : "https://localhost:8043",
        "CertificateFile" : "client-crt.pem",
        "CertificateKeyFile" : "client-key.pem",
        "CertificateKeyPassword": ""
      }
    }
  }
	  
Note that the same kind of configuration is also available for 
:ref:`DICOMweb client <dicomweb-client>`.

An example of such a setup with instructions to generate the
certificates is available `here
<https://github.com/orthanc-server/orthanc-setup-samples/src/master/docker/tls-mutual-auth/>`__.


.. _client-certificate-web-browser:

Securing Orthanc with a client certificate and access it using a Web browser
............................................................................

.. highlight:: bash

Firstly, create a PEM certificate for the Orthanc HTTPS server, and another
PKCS12 certificate for the client::

  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout server.key -out server.crt -subj "/C=BE/CN=localhost"
  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout client.key -out client.crt -subj "/C=BE/CN=localhost"
  $ cat server.key server.crt > server.pem
  $ openssl pkcs12 -export -in client.crt -inkey client.key -out client.p12

In the last step, you'll have to provide a password (that can be
empty).
  
.. highlight:: bash

Secondly, start Orthanc using the following configuration file for Orthanc::

  {
    "SslEnabled" : true,
    "SslCertificate" : "server.pem",
    "SslVerifyPeers": true,
    "SslTrustedClientCertificates": "client.crt"
  }

Thirdly, install the PKCS12 client-side certificate ``client.p12`` in
your Web browser. For instance, check out `these instructions for
Mozilla Firefox
<https://security.stackexchange.com/questions/163199/firefox-certificate-can-t-be-installed>`__.

You are then able to access Orthanc using HTTPS encryption, with
cryptographic identification of a client Web browser. Note that
because the certificate is self-signed, the Web browser will warn
about a potential security risk.

