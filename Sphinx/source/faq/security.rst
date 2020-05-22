.. _security:

Securing Orthanc
================

.. contents::

Orthanc is a microservice for medical imaging. Out-of-the-box, it
makes the assumption that it runs on the localhost, within a secured
environment. As a consequence, care must be taken if deploying Orthanc
in a insecure environment, especially if it is run as a public-facing
service on Internet. This page provides instructions to secure Orthanc
through its :ref:`configuration options <configuration>`.


General configuration
---------------------

As for any service running on a computer, you should:

* Make sure to run the Orthanc service as a separate user. In
  particular, never run Orthanc as the ``root`` user on GNU/Linux, or
  as the ``Administrator`` user on Microsoft Windows.

* Contact your network administrators to setup `Intranet firewalls
  <https://en.wikipedia.org/wiki/Firewall_(computing)>`__, so that
  only trusted computers can contact Orthanc through its REST API 
  or through the DICOM protocol.

Care must also be taken about some configuration options specific to
Orthanc:

* ``LimitFindResults`` and ``LimitFindInstances`` should not be set to
  zero to avoid making Orthanc unresponsive on large databases by a
  malicious user that would make many lookups within Orthanc. A value
  of ``100`` should be a good compromise.

* ``HttpsVerifyPeers`` should be set to ``true`` to secure outgoing
  connections to remote HTTPS servers (such as when Orthanc is acting
  as a :ref:`DICOMweb client <dicomweb-client>`).

* Make sure to understand the implications of the
  ``OverwriteInstances`` option.

* You might also be interested in checking the options related to
  :ref:`performance optimization <scalability>`.



Securing the HTTP server
------------------------

.. highlight:: lua

Orthanc publishes a :ref:`REST API <rest>` that provides full
programmatic access to its content, in read/write. This means for
instance that a malicious user could delete the entire content of the
server, or could inspect confidential medical data.

By default, the HTTP server is restricted to the localhost to prevent
such attacks from the outside world. However, as soon as external
access is granted by setting the ``RemoteAccessAllowed`` configuration
option to ``true``, you should:

* Set ``AuthenticationEnabled`` to ``true`` to force the users to
  authenticate. The authorized users are listed in the option
  ``RegisteredUsers``.

* Enable :ref:`HTTPS encryption <https>` to prevent the stealing of
  medical data or passwords, even on the Intranet.

* If Orthanc is put on a server that can be contacted from Internet,
  put Orthanc behind a :ref:`reverse proxy <https>`, and let this
  reverse proxy take care of the HTTPS encryption.
  
* Setup rules that define, for each authorized user, which resources
  it can access, and through which HTTP method (GET, POST, DELETE
  and/or PUT). This can be done by defining a :ref:`filter written in
  Lua <lua-filter-rest>`. Here is a sample Lua filter that
  differentiates between an administrator user (``admin``) who has
  full access on the localhost only, and a generic user (``user``)
  that has only read-only access::

    function IncomingHttpRequestFilter(method, uri, ip, username, httpHeaders)
      if method == 'GET' and (username == 'user' or username == 'admin') then
        -- Read-only access (only GET method is allowed)
        return true
      elseif username == 'admin' and ip == '127.0.0.1' then
        -- Read-write access for administrator (any HTTP method is allowed on localhost)
        return true
      else
        -- Access is disallowed by default
        return false
      end
    end

  Very importantly, make sure to protect ``POST`` access to the
  ``/tools/execute-script`` URI. This URI can indeed be used by a
  malicious user to execute any system command on the computer as the
  user that runs Orthanc.

* Consider implementing a :ref:`higher-level application
  <improving-interface>` (e.g. in PHP, Java, Django...) that takes
  care of user authentication/authorization, and that is the only one
  to be allowed to contact the Orthanc REST API. In particular, you
  must create a higher-level application so as to properly deal with
  `CSRF attacks
  <https://en.wikipedia.org/wiki/Cross-site_request_forgery>`__:
  Indeed, as explained in the introduction, Orthanc is a microservice
  that is designed to be used within a secured environment.

* For advanced scenarios, you might have interest in the
  :ref:`advanced authorization plugin <authorization>`. Similarly,
  developers of :ref:`plugins <plugins>` could be interested by the
  ``OrthancPluginRegisterIncomingHttpRequestFilter2()`` function
  provided by the Orthanc plugin SDK.


**Remark:** These parameters also apply to the :ref:`DICOMweb server plugin <dicomweb>`.


Securing the DICOM server
-------------------------

.. highlight:: json

Besides its REST API that is served through its embedded HTTP/HTTPS
server, Orthanc also acts as a :ref:`DICOM server <dicom-protocol>`
(more precisely, as a DICOM SCP).

In general, the DICOM protocol should be disabled if running Orthanc
on a cloud server, except if you use a VPN (cf. `reference
<https://groups.google.com/d/msg/orthanc-users/yvHexxG3dTY/7s3A7EHVBAAJ>`__).
Favor HTTPS for transfering medical images across sites (see
above). You can turn off DICOM protocol by setting the configuration
option ``DicomServerEnabled`` to ``false``.

The DICOM modalities that are known to Orthanc are defined by setting
the ``DicomModalities`` configuration option. Out-of-the-box, Orthanc
accepts C-ECHO and C-STORE commands sent by unknown modalities, but
blocks C-FIND and C-MOVE commands issued by unknown modalities.

To fully secure the DICOM protocol, you should:

* Set the ``DicomAlwaysAllowEcho`` configuration option to ``false``
  to disallow C-ECHO commands from unknown modalities.

* Set the ``DicomAlwaysAllowStore`` configuration option to ``false``
  to disallow C-STORE commands from unknown modalities.

* Set the ``DicomCheckModalityHost`` configuration option to ``true``
  to validate the IP and hostname address of the remote modalities.

* For each modality that is defined in ``DicomModalities``,
  selectively specify what DICOM commands are allowed to be issued by
  the SCU of this modality by setting the suboptions ``AllowEcho``,
  ``AllowFind``, ``AllowMove``, ``AllowStore`` and ``AllowGet``. For instance, a
  modality could be allowed to C-STORE images, but be disallowed to
  C-FIND the content of Orthanc. Here is a sample configuration to
  define a single modality that is only allowed to send DICOM
  instances to Orthanc::

    {
      "DicomModalities" : {
        "untrusted" : {
          "AET" : "CT",
          "Port" : 104,
          "Host" : "192.168.0.10",
          "AllowEcho" : false,
          "AllowFind" : false,
          "AllowMove" : false,
          "AllowGet" : false,
          "AllowStore" : true
        }
      }
    }

  **Note:** These configuration suboptions only affect the behavior of
  the DICOM SCP of Orthanc (i.e. for incoming connections). Orthanc
  will always be able to make outgoing DICOM SCU connections to these
  modalities, independently of the value of these suboptions.

* Consider implementing a :ref:`filter implemented in Lua
  <lua-filter-rest>` to restrict which modalities can C-STORE images
  within Orthanc, and which kind of images are accepted by Orthanc.

* Consider setting ``DicomCheckCalledAet`` to ``true`` to force proper
  configuration of remote modalities.
  

**Remark:** As of Orthanc 1.7.0, `DICOM TLS encryption
<https://www.dicomstandard.org/using/security/>`__ is not supported
yet. We are looking for :ref:`an industrial sponsor <contributing>` to
get this feature implemented, as it is useful in enterprise and cloud
environments.
