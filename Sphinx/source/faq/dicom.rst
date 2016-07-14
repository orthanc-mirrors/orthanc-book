.. _dicom:

Troubleshooting DICOM communications
====================================

In general, communication problems between two DICOM modalities over a
computer network are related to the configuration of these
modalities. As preliminary debugging actions, you should:

* Make sure you use the `most recent version <http://www.orthanc-server.com/download.php>`_ of Orthanc.
* Make sure the two computers can "ping" each other.
* Turn off all the firewalls on the two computers (especially on Microsoft Windows).
* Write down on a paper the following information about each modality:

  * its IP address (avoid using symbolic names if possible to troubleshot any DNS problem),
  * its TCP port for DICOM communications (for Orthanc, cf. the ``DicomPort`` option), and
  * its AET (Application Entity Title - for Orthanc, cf. the ``DicomAet`` option).

* Carefully re-read all your configuration files. As far as Orthanc is
  concerned, the most important section is ``DicomModalities``: Make
  sure its content matches what you wrote on the paper at the step
  above.
* In the ``DicomModalities`` configuration section of Orthanc, have a
  look at the fourth parameter that can activate some patches for
  specific vendors.
* Have a look at the following options of Orthanc to enable the more fault-tolerant DICOM support:

  * ``DicomServerEnabled`` must be set to ``true``.
  * ``DicomCheckCalledAet`` should be set to ``false``.
  * All the transfer syntaxes should be set to ``true`` (see the
    options with a ``TransferSyntaxAccepted`` suffix).
  * Temporarily disable any Lua script and any plugin, i.e. set the
    options ``LuaScripts`` and ``Plugins`` both to the empty list.
  * ``DicomAssociationCloseDelay`` should be set to ``0``.

* Restart Orthanc with the ``--verbose`` option at command line, and
  carefully inspect the log. This might provide immediate debugging
  information. Make sure to read :ref:`how to generate an exploitable
  log <log>`.
* Issue a :ref:`DICOM C-Echo <dicom-echo>` from each modality to make
  sure the DICOM protocol is properly configured (sending a C-Echo
  from Orthanc Explorer is possible starting with Orthanc 0.9.3, in
  the "Query/Retrieve" page).
* If the two modalities succeed with C-Echo, but query/retrieve does not
  succeed, please carefully read the :ref:`dicom-move` section.

As a last resort, please contact the `mailing list
<https://groups.google.com/forum/#!forum/orthanc-users>`_ by sending a
detailed description of your problem, notably:

* What fails: The sending of a file (aka. C-Store SCU), the searching
  of a patient/study (aka. C-Find SCU), or the retrieve of a file
  (aka. C-Move SCU)? Is Orthanc acting as a client or as a server?
* Describe your network topology, as written above on your paper (IP
  address, port number, and AET for both modalities).
* Specify the operating system, the vendor, the DICOM software, and
  the version of each modality.
* Attach sample DICOM files, possibly anonymized.
* Attach the log of the two modalities. The :ref:`log must be
  generated <log>` with the ``--trace`` command-line option as far as
  Orthanc is concerned.
* Attach any screenshot that is useful to understand the problem.
