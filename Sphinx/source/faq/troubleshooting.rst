.. _troubleshooting:

Troubleshooting
===============

* Always make sure you use the `most recent version
  <http://www.orthanc-server.com/download.php>`_ of Orthanc.
* **I cannot login to Orthanc Explorer**: For security reasons, access
  to Orthanc from remote hosts is disabled by default. Only the
  localhost is allowed to access Orthanc. You have to set the
  ``RemoteAccessAllowed`` option in the :ref:`configuration file
  <configuration>` to ``true``. It is then strongly advised to set
  ``AuthenticationEnabled`` to ``true`` and to add a user to the
  ``RegisteredUsers`` option, also in the configuration file.
* **Orthanc Explorer is slow under Windows on the localhost**: You
  have to disable the IPv6 support. This is a Windows-specific problem
  that is discussed `here
  <http://superuser.com/questions/43823/google-chrome-is-slow-to-localhost>`
  and `here
  <http://stackoverflow.com/questions/1726585/firefox-and-chrome-slow-on-localhost-known-fix-doesnt-work-on-windows-7>`.
* Under Windows, Orthanc creates the "OrthancStorage" folder, and
  crashes with the error "**SQLite: Unable to open the database**":
  Your directory name is either too long, or it contains special
  characters. Please try and run Orthanc in a folder with a simple
  name such as ``C:\Orthanc``.
