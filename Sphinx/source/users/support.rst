.. _support:

Asking for support
==================

.. contents::
   :depth: 3


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
   <https://discourse.orthanc-server.org>`__.
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
services <https://osimis.io/en/orthanc-support-contract>`__ in order to get
the feature implemented faster.
   
   
.. _support-mwe:

Discussing a minimal working example
------------------------------------
   
If none of these resources help, you can consider sending a message to
the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__. 
In such a situation, you **must** provide a `minimal working example
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
  <https://dicom.offis.de/dcmtk.php.en>`__ (notably ``storescu``),
  `dicom3tools <https://www.dclunie.com/dicom3tools.html>`__ (notably
  ``dciodvfy``), `dcm4che command-line tools
  <https://www.dcm4che.org/>`__ (notably ``storescu``), `GDCM
  <http://gdcm.sourceforge.net/>`__ (notably ``gdcmscu``), or Python
  scripts (notably using ``pydicom``).
* In the case of DICOM networking problems, the logs from the remote
  modality.
* If applicable, a screenshot is worth a thousand words.
* If you report a crash, if applicable, a :ref:`core file <crash>`.
* The `OHIF viewer <https://ohif.org/>`__ can `connect to Orthanc
  <https://docs.ohif.org/history/v1/connecting-to-image-archives/orthanc-with-docker.html>`__
  using the DICOMweb plugin of Orthanc, but is a fully separate
  project. As a consequence, questions regarding OHIF must be asked on
  the `dedicated discussion group
  <https://groups.google.com/g/cornerstone-platform>`__ or on the
  `dedicated bug tracker
  <https://github.com/OHIF/Viewers/issues>`__. The core developers of
  Orthanc will happily fix the :ref:`DICOMweb plugin <dicomweb>`, but
  it is necessary for the reporter to identify the discrepancy wrt.
  DICOMweb standard by providing a minimal working example as
  explained above.


All this information is mandatory, as it allows other members of the
Orthanc community to **reproduce your problem independently of your
setup**. If we can't reproduce your issue, we can't provide any
support!

In addition, please note that the original author of Orthanc
(Sébastien Jodogne), as a free software advocate, will only personally
deal with issues that are reproducible on recent GNU/Linux
distributions (typically, on Ubuntu 18.04 LTS or through Docker).


.. _support-minquality:

Required minimal quality of a message in the Orthanc Users discussion forum
--------------------------------------------------------

While posting a message on the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__, you should not be surprised if 
your message does not get any response if it does not meet these minimal 
quality requirements:

* Before posting, are you sure you have made everything possible to :ref:`analyze <support-resources>` 
  and solve the issue by yourself?  This includes, searching the web or the forum 
  to see if the topic has already been discussed.
* :ref:`Describe your issue <support-mwe>` with as much details as possible.
* Review your message as if you were the one who should help you - 
  would you understand your problem?
* Be polite and respectful, say ``hello``, and adhere to the `code of conduct 
  <https://discourse.orthanc-server.org/faq>`__.


.. _support-tracker:

Using the bug tracker
---------------------

If you are **sure** that you are reporting a yet unknown bug, you can
consider directly introducing a `bug report on our issue tracker
<https://bugs.orthanc-server.com/enter_bug.cgi>`__. Beware however
that your issue might be closed if too vague or if not reproducible.
As a consequence, it is strongly advised to use the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__ in the
first place.


.. _support-freelancers:

Finding professional assistance
-------------------------------

If you face a problem you cannot solve by yourself, please follow this
decision chart:

1. If you have a **reproducible issue** for which you can provide a
   :ref:`minimal working example <support-mwe>` using only free and
   open-source tools, use the `Orthanc Users discussion forum
   <https://discourse.orthanc-server.org>`__.

2. If you need an **additional feature implemented in Orthanc**, and
   if you are ready to pay, get in touch with the `Orthanc Team
   <https://orthanc.team>`__ or with `Osimis
   <mailto:orthanc-support@osimis.io>`__, the commercial partners of
   the Orthanc project.

3. If you are part of a **scientific team** and would like to setup a
   research project using Orthanc, including about AI, get in touch
   with `Sébastien Jodogne's research lab
   <https://www.info.ucl.ac.be/~sjodogne/>`__ at the UCLouvain
   university.
   
4. If you are not able to reproduce an issue by yourself, if you are
   looking for personalized help related to deployments/training/...,
   or if you need **proximity support in your language/timezone**,
   here is a list of freelancers/companies:

   * **Worldwide**:
   
     * `Orthanc Team (Alain Mazy & Benoît Crickboom) <https://orthanc.team>`__ (French/English, Belgium)

   * **Europe**:

     * `Adrian Schiopu <sc.callisto.srl@gmail.com>`__ (Romania)
     * `Krzysztof Turkiewicz <http://www.deeveeloop.pl/>`__ (Polish/English, Poland)
     * `Salim Kanoun <https://github.com/salimkanoun>`__ (French/English/Arabic, France)
     * `Stephen D. Scotti <https://www.medinformatics.eu>`__ (English, Austria)

   * **North America**:
       
     * `Gabriel Couture <https://github.com/gacou54/>`__ (French/English, Canada)
     * `Mohannad Hussain <https://www.linkedin.com/in/mohannadhussain/>`__ (English, Canada)
     * `Oliver Tsai <mailto:oliver@futurepacs.com>`__ (English/Spanish/French, Toronto)
     * `Yi Lu <https://www.linkedin.com/in/digihunch/>`__ (English, Canada)

   * **South America**:
       
     * `Claudio Arenas <mailto:dentista.arenas@gmail.com>`__ (Spanish/English, Chile)
     * `Fernando Sánchez <https://integraper.com/?page_id=529>`__ (English/Spanish, Peru)
     * `Gustavo Fernandez <https://www.linkedin.com/in/gfernandezguirland/>`__ (Spanish/Portuguese, Uruguay)
     * `Iván Kuschevatzky <mailto:ivankuche@gmail.com>`__ (English/Spanish, Argentina)
     * `Luiz Eduardo Guida Valmont <https://www.linkedin.com/in/luizvalmont/>`__ (English/Portuguese, Brazil)
     * `William Sanchez Luis <mailto:williamsanchezluis@gmail.com>`__ (English/Spanish, Venezuela)

   * **Africa**:

     * `Abdrahman Elkafil <mailto:elkafil@nextbehealthcare.com>`__ (English/French/Arabic, Belgium and Morocco)
     * `Olakunle Dada <mailto:holakunle69@gmail.com>`__ (English/French, Nigeria)

   * **Asia**:
     
     * `Ajay Rana <https://smarthms.in/>`__ (English/Hindi/Punjabi, India)
     * `Phong Tran Duc <http://www.itechcorp.com.vn/>`__ (English/Vietnamese, Vietnam)
     * `Rana Asim Wajid <http://ethosmed.com/>`__ (English/Urdu/Punjabi, Pakistan)
     * `Yash Sonalia <mailto:sonaliayash@gmail.com>`__ (English/Hindi/Bengali, India)

   * **Oceania**:
     
     * `James Manner <https://binary.com.au/>`__ (English, Australia)

   Get in touch with `Sébastien Jodogne
   <mailto:s.jodogne@orthanc-labs.com>`__ if you want to be included
   in this list.
 
