.. _dicom-tls:

Configuring DICOM TLS
=====================

.. contents::
   :depth: 3

Starting with release 1.9.0, Orthanc supports the encryption of the
DICOM protocol using `DICOM TLS
<https://www.dicomstandard.org/using/security/>`__. This allows the
secure exchange of medical images between different sites, even if
using the DICOM protocol.

Configuration
-------------

.. highlight:: bash

To enable DICOM TLS, each DICOM modality must have been assigned with
a `X.509 certificate
<https://en.wikipedia.org/wiki/X.509>`__. Obtaining such a certificate
from a `recognized certification authority
<https://en.wikipedia.org/wiki/Certificate_authority>`__ is obviously
out of the scope of the Orthanc project. Here is a simple command-line
to generate a self-signed certificate using the `OpenSSL
<https://www.openssl.org/>`__ command-line tools::

  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout orthanc.key -out orthanc.crt -subj "/C=BE/CN=localhost"

Obviously, you must adapt the arguments to your setup (notably the
``subj`` argument that generates a certificate for Belgium for the
server whose DNS address is ``localhost``). This command line will
generate two files using the `PEM file format
<https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail>`__:
``orthanc.crt`` is the newly-generated certificate, and
``orthanc.key`` contains the private key that protects the
certificate. The ``orthanc.crt`` can be openly distributed, but
``orthanc.key`` must be kept secret (it should only be placed on the
modality using the corresponding certificate).

Once ``orthanc.crt`` and ``orthanc.key`` have been generated, all the
modalities that will be in touch with Orthanc (either as SCP or as
SCU) through DICOM TLS must be identified, and their public
certificates must be collected. All those certificates must be
concatenated into a single file in order to tell Orthanc which
modalities can be trusted.

Concretely, if one has collected ``a.crt``, ``b.crt`` and ``c.crt`` as
the certificates (in the PEM format) for trusted remote DICOM
modalities, a ``trusted.crt`` file can be generated as follows::

  $ cat a.crt b.crt c.crt > trusted.crt

Once the three files ``orthanc.crt``, ``orthanc.key`` and
``trusted.crt`` are available, setting the following
:ref:`configuration options <configuration>` will enable DICOM TLS in
**Orthanc SCP**:

* ``DicomTlsEnabled`` must be set to ``true``.
* ``DicomTlsCertificate`` must be set to ``orthanc.crt``.
* ``DicomTlsPrivateKey`` must be set to ``orthanc.key`` (note that
  this private key must not be password-protected).
* ``DicomTlsTrustedCertificates`` must be set to ``trusted.crt``.

If Orthanc acts as a **DICOM SCU** against one remote DICOM modality,
and if this remote modality is protected by DICOM TLS, the
``UseDicomTls`` field must be set to ``true`` in the definition of the
modality in the configuration file of Orthanc (cf. the
``DicomModalities`` option). The file indicated by
``DicomTlsCertificate`` will be used to authentify Orthanc by the
remote modality: This modality must thus include ``orthanc.crt`` in
its list of trusted certificates.


**Remark 1:** Pay attention not to confuse the configuration options
related to HTTPS encryption, with the options related to DICOM TLS.
In Orthanc, HTTPS and DICOM TLS are not obliged to use the same
encryption certificates.

**Remark 2:** Orthanc SCU and Orthanc SCP share the same set of
trusted certificates.

**Important:** `DCMTK 3.6.4 seems to have an issue with DICOM TLS
<https://forum.dcmtk.org/viewtopic.php?t=5073>`__, which produces the
errors ``DUL secure transport layer: no suitable signature algorithm``
(in the DICOM SCP) and ``DUL secure transport layer: sslv3 alert
handshake failure`` (in the DICOM SCU). Make sure to use either DCMTK
3.6.2 or DCMTK 3.6.6. In particular, Debian Buster (10) will use DCMTK
3.6.4 and should be avoided in non-static builds of Orthanc, or if
using the DCMTK command-line tools.



Examples
--------

Using DCMTK
^^^^^^^^^^^

.. highlight:: bash

Let us generate one certificate for Orthanc, and one certificate for
DCMTK::

  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout orthanc.key -out orthanc.crt -subj "/C=BE/CN=localhost"
  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout dcmtk.key -out dcmtk.crt -subj "/C=BE/CN=localhost"

.. highlight:: json

Let us start Orthanc using the following minimal configuration file::

  {
    "DicomTlsEnabled" : true,
    "DicomTlsCertificate" : "orthanc.crt",
    "DicomTlsPrivateKey" : "orthanc.key",
    "DicomTlsTrustedCertificates" : "dcmtk.crt",
    "DicomModalities" : {
      "dmctk" : {
        "Host" : "localhost",
        "Port" : 4242,
        "AET" : "DCMTK",
        "UseDicomTls" : true
      }
    }  
  }

.. highlight:: text

It is then possible to trigger a secure C-ECHO SCU request from DCMTK
to Orthanc as follows::

  $ echoscu -v -aet DCMTK localhost 4242 +tls dcmtk.key dcmtk.crt +cf orthanc.crt 
  I: Requesting Association
  I: Association Accepted (Max Send PDV: 16372)
  I: Sending Echo Request (MsgID 1)
  I: Received Echo Response (Success)
  I: Releasing Association


Using dcm4che
^^^^^^^^^^^^^

.. highlight:: bash

To use the dcm4che command-line tools instead of DCMTK, the two
certificates must first be converted from `X.509
<https://en.wikipedia.org/wiki/X.509>`__ to `PKCS #12
<https://en.wikipedia.org/wiki/PKCS_12>`__::

  $ openssl pkcs12 -export -out orthanc.p12 -in orthanc.crt -inkey orthanc.key
  $ openssl pkcs12 -export -out dcm4che.p12 -in dcmtk.crt -inkey dcmtk.key

For this example, you can let the ``Export Password`` as an empty
string in the two calls above. Then, here is how to trigger a secure
C-STORE SCU request to send the ``sample.dcm`` file from dcm4che to
Orthanc::

  $ ~/Downloads/dcm4che-5.23.3/bin/storescu -c ORTHANC@localhost:4242 --tls \
   --trust-store ./orthanc.p12 --key-store ./dcm4che.p12 --trust-store-pass "" --key-store-pass "" sample.dcm

**Remarks:**

* The empty strings provided to the ``--trust-store-pass`` and
  ``--key-store-pass`` options correspond to the empty strings
  provided to ``Export Password``.

* Disclaimer: In this setup, ``orthanc.p12`` contains the private key
  of the Orthanc server. It is unclear how to remove this private key
  that should be unknown to the DICOM client for security reasons.
   

Secure TLS connections without certificate
------------------------------------------

In Orthanc <= 1.9.2, the remote DICOM modalities are required to
provide a valide DICOM TLS certificate (which corresponds to the
default ``--require-peer-cert`` option of the DCMTK command-line
tools).

Starting from Orthanc 1.9.3, it is possible to allow connections
to/from remote DICOM modalities that do not provide a DICOM TLS
certificate (which corresponds to the ``--verify-peer-cert`` option of
DCMTK). This requires setting the :ref:`configuration option
<configuration>` ``DicomTlsRemoteCertificateRequired`` of Orthanc to
``false``.

.. highlight:: bash

As an example, let us generate one single certificate that is
dedicated to Orthanc::

  $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout orthanc.key -out orthanc.crt -subj "/C=BE/CN=localhost"


.. highlight:: json

Let us start Orthanc using the following minimal configuration file::

  {
    "DicomTlsEnabled" : true,
    "DicomTlsCertificate" : "orthanc.crt",
    "DicomTlsPrivateKey" : "orthanc.key",
    "DicomTlsTrustedCertificates" : "orthanc.crt",
    "DicomTlsRemoteCertificateRequired" : false
  }

.. highlight:: text

Note that the ``DicomTlsTrustedCertificates`` is set to a dummy value,
because this option must always be present. It is then possible to
connect to Orthanc without SCU certificate as follows::

  $ echoscu -v localhost 4242 --anonymous-tls +cf /tmp/k/orthanc.crt 
  I: Requesting Association
  I: Association Accepted (Max Send PDV: 16372)
  I: Sending Echo Request (MsgID 1)
  I: Received Echo Response (Success)
  I: Releasing Association


**Remark:** Importantly, if the remote DICOM modality provides an
invalid DICOM TLS certificate, Orthanc will never accept the
connection.
