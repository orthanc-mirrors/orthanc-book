.. _support:

Asking for support
==================

.. _support-resources:

Analyzing your problem
----------------------

When you face a problem, you should first check out the following
resources:

1. Make sure that you use the `latest version of Orthanc
   <http://www.orthanc-server.com/download.php>`__.
2. Make sure to :ref:`check all the content of the Orthanc Book
   <orthanc-book>`, and notably to :ref:`understand the basics of
   DICOM <dicom-guide>`.
3. Carefully read your :ref:`log files in verbose mode <log>`.
4. In the case of DICOM networking problems, carefully read the log
   files from your remote modality. If you are :ref:`using Orthanc
   against a proprietary system <proprietary>`, contact the support
   team from the vendor of this system: You pay them to solve your
   setup issues.
5. Follow the :ref:`general troubleshooting guide <troubleshooting>`.
6. If the problem is related to the DICOM network protocol, follow
   the :ref:`DICOM troubleshooting guide <dicom>`.
7. Have a look at **all** the :ref:`frequently asked questions (FAQs)
   <faq>` that are already available in the Orthanc Book.
8. Make a search for similar problem previously discussed in the
   `Orthanc Users discussion forum
   <https://groups.google.com/forum/#!forum/orthanc-users>`__.
9. Check out the ``Pending changes in the mainline`` section of the
   `NEWS file
   <https://hg.orthanc-server.com/orthanc/file/default/NEWS>`__, as
   your issue might already be solved in the mainline of Orthanc (i.e.
   in the cutting-edge version of Orthanc since the last stable
   official release).
10. Carefully read the `TODO file
    <https://hg.orthanc-server.com/orthanc/file/default/TODO>`__ that
    contains our roadmap, as you might be requesting a feature that is
    currently pending in our backlog (i.e. not implemented yet).
11. Look for similar issue in the `official bug tracker
    <https://bugs.orthanc-server.com/query.cgi>`__ (make sure to
    select ``All`` in the ``Status`` field, as your issue might
    already have been solved).


Importantly, for all the features that are pending in the ``TODO``
file, if you are a company, please consider `buying professional
services <https://www.osimis.io/en/services.html>`__ in order to get
the feature implemented faster.
   
   
.. _support-mwe:

Discussing a minimal working example
------------------------------------
   
If none of these resources help, you can consider sending a message to
the `Orthanc Users discussion forum
<https://groups.google.com/forum/#!forum/orthanc-users>`__. In such a
situation, you **must** provide a `minimal working example
<https://en.wikipedia.org/wiki/Minimal_working_example>`__, which means that
you must provide all the following information:

* Context and full textual description of your issue. When talking
  about DICOM networking issues, carefully describe the imaging
  modalities into play (including their manufacturers) and your
  network topology.
* The observed vs. expected results.
* Full :ref:`configuration files <configuration>`.
* Full logs as produced by Orthanc in :ref:`verbose mode <log>`.
* Sample DICOM files.
* A sequence of command lines that lead to your problem. These command
  lines must only use commands that are available as free and
  open-source software, that are cross-platform (:ref:`proprietary
  software does not help <proprietary>`), and that are preferably
  calls the :ref:`REST API of Orthanc <rest>`. The most useful
  commands are `cURL <https://en.wikipedia.org/wiki/CURL>`__, `DCMTK
  <https://dicom.offis.de/dcmtk.php.en>`__, `dicom3tools
  <https://www.dclunie.com/dicom3tools.html>`__, `dcm4che command-line
  tools <https://www.dcm4che.org/>`__, or Python scripts.
* In the case of DICOM networking problems, the logs from the remote
  modality.
* If applicable, a screenshot is worth a thousand words.
* If you report a crash, if applicable, a :ref:`core file <crash>`.

All this information is mandatory, as it allows other members of the
Orthanc community to **reproduce your problem independently of your
setup**. If we can't reproduce your issue, we can't provide any
support!

In addition, please note that the original author of Orthanc
(Sébastien Jodogne), as a free software advocate, will only personally
deal with issues that are reproducible on recent GNU/Linux
distributions (typically, on Ubuntu 18.04 LTS or through Docker).


.. _support-tracker:

Using the bug tracker
---------------------

If you are **sure** that you are reporting a yet unknown bug, you can
consider directly introducing a `bug report on our issue tracker
<https://bugs.orthanc-server.com/enter_bug.cgi>`__. Beware however
that your issue might be closed if too vague or if not reproducible.
As a consequence, it is advised to first use the discussion forum.
