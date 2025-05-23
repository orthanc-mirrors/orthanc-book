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

* Make sure that the :ref:`configuration files <configuration>`
  containing confidential information or private keys (typically
  ``RegisteredUsers``) are only readable by the user that runs
  Orthanc.

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

       
.. _security_http:

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

* Check that ``AuthenticationEnabled`` is set to ``true`` to force the 
  users to authenticate. The authorized users are listed in the option
  ``RegisteredUsers``.  Note that, if the option ``AuthenticationEnabled`` 
  is not provided, the authentication will be enabled as soon 
  as ``RemoteAccessAllowed`` is enabled.

* Enable :ref:`HTTPS encryption <https>` to prevent the stealing of
  medical data or passwords, even on the Intranet.

* If Orthanc is put on a server that can be contacted from Internet,
  put Orthanc behind a :ref:`reverse proxy <https>`, and let this
  reverse proxy take care of the HTTPS encryption.

* Enable :ref:`Client certificate authentication <https>` between multiple
  Orthanc peers.

* Consider turning of the :ref:`embedded WebDAV server <webdav>` by
  setting configuration option ``WebDavEnabled`` to ``false``.

* Ensure that ``/tools/execute-script`` is disabled by leaving the configuration
  ``ExecuteLuaEnabled`` to its default ``false`` value.

* Ensure that the REST API can not write to the filesystem (e.g. in the
  ``/instances/../export`` route) by leaving the configuration
  ``RestApiWriteToFileSystemEnabled`` to its default ``false`` value.

* Make sure to run Orthanc as a non-privileged user with read-write access only 
  for the storage area.

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
  ``/tools/execute-script`` and ``/instances/../export`` URIs. 
  The first URI can indeed be used by a malicious user to execute any 
  system command on the computer as the user that runs Orthanc.  The second
  URI can be used by a malicious user to overwrite system files possibly
  with malicious DICOM files that may lead to execution of system commands.

* Consider implementing a :ref:`higher-level application
  <improving-interface>` (e.g. in PHP, Java, Django...) that takes
  care of user authentication/authorization, and that is the only one
  to be allowed to contact the Orthanc REST API. In particular, you
  must create a higher-level application so as to properly deal with
  `CSRF attacks
  <https://en.wikipedia.org/wiki/Cross-site_request_forgery>`__:
  Indeed, as explained in the introduction, Orthanc is a microservice
  that is designed to be used within a secured environment.

* Configuration option ``OrthancExplorerEnabled`` should be set to
  ``false`` in Internet-facing deployments.
  
* For advanced scenarios, you might have interest in the
  :ref:`advanced authorization plugin <authorization>`. Similarly,
  developers of :ref:`plugins <plugins>` could be interested by the
  ``OrthancPluginRegisterIncomingHttpRequestFilter2()`` function
  provided by the Orthanc plugin SDK.

* Don't forget that, if you are using a Database Server to store your
  index, you can deploy 
  :ref:`multiple Orthanc instances connected to the same DB <multiple-writers>`.
  You may therefore have one Orthanc that is public facing with a very strict
  secure configuration and one Orthanc that is not public facing and less
  secured that is accessible e.g. only to your backend application or your
  scripts.

**Remark:** These parameters also apply to the :ref:`DICOMweb server plugin <dicomweb>`.


Securing the DICOM server
-------------------------

.. highlight:: json

Besides its REST API that is served through its embedded HTTP/HTTPS
server, Orthanc also acts as a :ref:`DICOM server <dicom-protocol>`
(more precisely, as a DICOM SCP).

In general, the DICOM protocol should be disabled if running Orthanc
on a cloud server, except if you use a VPN (cf. `reference
<https://groups.google.com/d/msg/orthanc-users/yvHexxG3dTY/7s3A7EHVBAAJ>`__)
or a SSH tunnel (cf. `reference
<https://www.howtogeek.com/168145/how-to-use-ssh-tunneling/>`__). Favor
HTTPS for transfering medical images across sites (see above). You can
turn off DICOM protocol by setting the configuration option
``DicomServerEnabled`` to ``false``.

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
  to validate the IP address of the remote modalities (note that
  hostnames cannot be used in ``DicomModalities`` when this option is
  enabled: The ``Host`` values should only contain IP addresses).

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
  

Starting with Orthanc 1.9.0, `DICOM TLS encryption
<https://www.dicomstandard.org/using/security/>`__ is supported by
Orthanc. If you need to share DICOM instances between sites, but if
you don't want to use DICOMweb or Orthanc peers over HTTPS, you must
enable :ref:`DICOM TLS in Orthanc <dicom-tls>` to ensure secure
exchanges.

As a workaround for the releases <= 1.8.2 of Orthanc that don't
support DICOM TLS, `it has been reported
<https://www.digihunch.com/2020/11/medical-imaging-web-server-deployment-pipeline/>`__
that the "*SSL Termination for TCP Upstream Servers*" feature of nginx
can be used to emulate DICOM TLS. Another option is to use `stunnel
<https://www.stunnel.org/>`__.


Securing the storage
--------------------

In general, for security, Orthanc should store its database index
(PostgreSQL, SQLite...) and its :ref:`storage area <orthanc-storage>`
for DICOM files on an `on-premises, self-hosted infrastructure
<https://en.wikipedia.org/wiki/On-premises_software>`__ with `disk
encryption
<https://en.wikipedia.org/wiki/Disk_encryption>`__. Similarly, Orthanc
itself should ideally run on your own on-premises infrastructure, and
not on a virtual machine that is managed by a public cloud solution
provider.

Depending on your jurisdiction, it might be possible to move the
storage area to a `cloud-based object storage
<https://en.wikipedia.org/wiki/Object_storage>`__, by using the
:ref:`dedicated storage plugins <object-storage>`. :ref:`Orthanc-side
encryption <client-side-encryption>` should be enabled in such a
situation.

In any case, make sure to get legal advice that is very specific to
the legislation of the countries where you are active (for
illustration, check out the recent debates over the `privacy shield
<https://en.wikipedia.org/wiki/EU%E2%80%93US_Privacy_Shield>`__ in
Europe). Make sure to understand the implications of using cloud-based
object storage, of using virtual machines in the cloud to store health
data, of using managed database servers (even with so-called
"encryption-at-rest" features)...

As a free and open-source project, the Orthanc ecosystem cannot be
taken as liable for any security breach or data leak in your
deployments, for any misconfiguration, for any bad handling of
personal/health data, for any bypassing of regulatory requirements,
for not being compliant with your local legislation, or for any
similar stuff: Orthanc is just software, security is your
responsibility.
