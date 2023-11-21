.. _licensing:


Licensing of the Orthanc ecosystem
==================================

.. contents::


Philosophy
----------

The objectives of the Orthanc ecosystem is to share technical
knowledge about :ref:`DICOM <dicom-guide>`, to build a consistent
platform for developing medical imaging software, and to foster
scientific collaborations in medical imaging by subscribing to the
`open-science paradigm
<https://en.wikipedia.org/wiki/Open_science>`__. To this end, Orthanc
is provided as free and open-source software to the benefit of the
worldwide community of medical imaging.

In order to support this objective of global knowledge sharing, the
Orthanc project enforces reciprocity. If someone finds Orthanc useful
to her academic work or to her business, the community of medical
imaging should gain an advantage from this use by enlarging the
knowledge base. This virtuous circle guarantees the fact that Orthanc
will be developed in a sustainable way in the long-term, to the
benefit of all stakeholders. Predatory behaviors should be prevented,
while preserving the freedoms of the users of Orthanc, including the
commercial uses.

According to this philosophy, the University Hospital of Liège decided
to release the Orthanc ecosystem under the `GPLv3+ license
<https://www.gnu.org/licenses/gpl-3.0.en.html>`__ in 2012. The GPL is
a strong copyleft license that is recognized worldwide, and that is
designed to enforce reciprocity.

As Orthanc is lightweight and designed for Web applications and for
sharing medical images over Internet, it has been quickly deployed on
cloud platforms in order to host large amount of data. Orthanc
considers this use as very legitimate, for instance for scientific
purpose (think of open-data databases) or for societal needs (think of
teleradiology platforms in developing countries). Unfortunately, the
GPL does not protect from predatory commercial behaviors over cloud
platforms because of the so-called "`ASP loophole
<https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License>`__",
that does not enforce derived versions of a free and open-source
software running on a server to be given back to the community.

For this reason, the plugins that provide scalability-related or
cloud-related features (for instance the :ref:`PostgreSQL
<postgresql>` and :ref:`Web viewer <webviewer>` plugins that are
necessary for Web applications distributed at a large scale) were
released under the stronger `AGPLv3+ licence
<https://www.gnu.org/licenses/why-affero-gpl.en.html>`__.
This license protects the community of medical imaging by ensuring
that the features included in Orthanc instances running in remote
servers are publicly available as well.


Guidelines
----------

Over the years, it was observed that people fear the use of GPL and
AGPL licenses, that are wrongly considered as preventing commercial
uses. This is most often a wrong assumption, given that the Orthanc
server is a standalone executable, not a software library.

The following table provides a simple summary of the most common
situations, and indicates whether the use is **accepted ("Yes"),
forbidden ("No"), or restricted ("Dual license")**:

+-----------------------------------------------------+--------------------------------------------------------------------------------------------+
|                                                     | Mode of distribution of the third-party system, or of the third-party plugin/script        |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| Usage of the Orthanc ecosystem                      | Permissive    | GPLv3 | AGPLv3 | Internal use | Proprietary software   | Proprietary cloud |
|                                                     | (MIT, BSD,    |       |        |              | distributed to clients | platform or Web   |
|                                                     | Apache...)    |       |        |              |                        | portal            |
+=====================================================+===============+=======+========+==============+========================+===================+
| Using Orthanc as such, even if some AGPL-licensed   | N/A           | N/A   | N/A    | Yes          | Yes                    | Yes               |
| plugin is installed                                 |               |       |        |              |                        |                   |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| Calling Orthanc from a third-party system           | Yes           | Yes   | Yes    | Yes          | Yes                    | Yes               |
| (using REST API or DICOM protocol), even if some    |               |       |        |              |                        |                   |
| AGPL-licensed plugin is installed                   |               |       |        |              |                        |                   |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| Creating a :ref:`C/C++ plugin <plugins>`,           |               |       |        |              |                        |                   |
| creating a :ref:`Lua script <lua>`, or              |               |       |        |              |                        |                   |
| creating a :ref:`Python plugin <python-plugin>`.    |               |       |        |              |                        |                   |
| 2 possible cases:                                   |               |       |        |              |                        |                   |
+----+------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
|    | Case 1: No AGPL-licensed plugin is in use      | No            | Yes   | Yes    | Yes          | Dual license           | Yes               |
+----+------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
|    | Case 2: Some AGPL-licensed plugin is in use    | No            | Yes   | Yes    | Yes          | Dual license           | Dual license      |
+----+------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| Using a derived version of the GPL-licensed         | No            | Yes   | Yes    | Yes          | Dual license           | Yes               |
| code of Orthanc, or using a derived version of      |               |       |        |              |                        |                   |
| some GPL-licensed plugin, or reusing their original |               |       |        |              |                        |                   |
| code in a third-party system                        |               |       |        |              |                        |                   |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| Using a derived version of some AGPL-licensed       | No            | No    | Yes    | Yes          | Dual license           | Dual license      |
| plugin, or reusing its original code in a           |               |       |        |              |                        |                   |
| third-party system                                  |               |       |        |              |                        |                   |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+
| **For viewers**: Using a derived version of the     | No            | No    | Yes    | Yes          | Dual license           | Dual license      |
| :ref:`Orthanc Web Viewer <webviewer>`, of the       |               |       |        |              |                        |                   |
| :ref:`Osimis Web Viewer <osimis_webviewer>`, of the |               |       |        |              |                        |                   |
| :ref:`Stone Web Viewer <stone>`, or of the sample   |               |       |        |              |                        |                   |
| applications of Stone of Orthanc (AGPL license)     |               |       |        |              |                        |                   |
+-----------------------------------------------------+---------------+-------+--------+--------------+------------------------+-------------------+

.. raw:: html

   <p align="center">
     <a href="mailto:info@osimis.io?subject=Request for a dual license">
       <b>Click here to request a dual license</b>
     </a>
   </p>

    
**Notes:**

* The wording "third-party system" is very broad, as it encompasses
  many possibilities. It can for instance be a Web application, a
  heavyweight desktop application, an automated script, or more
  generally any system that takes advantage of Orthanc as a service in
  its global architecture.

* If your use case falls in a "**Dual license**" cell, please get in
  touch with `Osimis <https://www.osimis.io/>`__, the commercial
  partner of the Orthanc project that is the only entity entitled to
  grant a `license exception
  <https://www.fsf.org/blogs/rms/selling-exceptions>`__ to your
  company for the Orthanc core and its :ref:`associated official
  plugins <plugins-official>`.

* If you reuse code from Orthanc or one of its associated plugins, you
  must mention the copyright of the Orthanc project.

* An Orthanc plugin cannot be licensed under a permissive license
  (MIT, BSD, Apache...) because it cannot run independently of the
  Orthanc SDK, which implies that the plugin and the Orthanc core form
  a single combined program, which in turn means that the plugin
  should be licensed under GPLv3 by `copyleft
  <https://en.wikipedia.org/wiki/Copyleft>`__ contamination. Check out
  the `license compatibility matrix on Wikipedia
  <https://en.wikipedia.org/wiki/License_compatibility#Compatibility_of_FOSS_licenses>`__.
  Here is the corresponding entry about this topic in the `GPL FAQ
  <https://www.gnu.org/licenses/gpl-faq.en.html#GPLPlugins>`__: *"If
  the main program dynamically links plug-ins, and they make function
  calls to each other and share data structures, we believe they form
  a single combined program, which must be treated as an extension of
  both the main program and the plug-ins. [...] If the main program
  and the plugins are a single combined program then this means you
  must license the plug-in under the GPL or a GPL-compatible free
  software license and distribute it with source code in a
  GPL-compliant way."*

* If you deal with medical applications in Europe, note that Osimis
  sells **CE-approved** versions of a Web viewer plugin.

* You are kindly invited to cite the `reference paper about Orthanc
  <https://link.springer.com/article/10.1007/s10278-018-0082-y>`__
  in your scientific work.

* This is our own simplified, technical interpretation of the GPLv3+
  and AGPLv3+ in the very specific context of Orthanc. It is not
  intended to be a complete guide to copyleft licensing. Please get in
  touch with the `Free Software Foundation <https://www.fsf.org/>`__
  for more legal information.


.. _cla:

Contributing to the code of Orthanc
-----------------------------------

Contributed vs. internal code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is important to make the distinction between contributed code and
internal code:

* **Contributed code** refers to source code that takes advantage of
  Orthanc and/or that extends Orthanc, such as new :ref:`plugins
  <plugins>`, :ref:`Lua scripts <lua>`, or any higher-level
  application that uses the :ref:`REST API <rest>` of Orthanc. This
  code can live outside of the official source repositories of the
  Orthanc ecosystem. External contributors can distribute such
  contributed code on whatever platform they prefer, in a way that is
  fully uncoupled from the Orthanc project, and keep the intellectual
  property of their developments. Such contributors are however kindly
  invited to index their contributions in the `dedicated repository on
  GitHub <https://github.com/jodogne/OrthancContributed>`__, and
  contributed plugins should also be indexed in the :ref:`Orthanc Book
  <plugins-contributed>`.

* **Internal code** refers to source code that only makes sense if
  embedded within the Orthanc core or within one of the official
  plugins. This includes new features and bugfixes. The way to
  contribute to the internal code of the Orthanc ecosystem is
  described in the sections below.


**Important:** You should always favor the :ref:`creation of a new
plugin <creating-plugins>` over modifications to the internal code
(see below)!



Contributor License Agreement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is necessary for the Orthanc project to make sure that the internal
code of Orthanc can be interfaced with proprietary systems, as those
are still unfortunately everywhere in the healthcare market. This
forces us to require all the intellectual property over the source
code of Orthanc to be centralized, with the University Hospital of
Liège, the Osimis company and the UCLouvain university acting as the
official guardians of the whole Orthanc ecosystem. This centralization
also enables the dual licensing scheme described above, which in turn
allows Osimis to collect money from the industry in order to fund
further free and open-source development of the Orthanc ecosystem to
the benefit of the worldwide community of medical imaging, according
to a virtuous cycle.

As a consequence, before any code can be accepted into the official
repositories of Orthanc, the individual code contributors must sign a
`Contributor License Agreement (CLA)
<https://en.wikipedia.org/wiki/Contributor_License_Agreement>`__. Here
is the procedure:

1. Download the individual CLA (ICLA) form from the `Orthanc homepage
   <https://www.orthanc-server.com/resources/2019-02-12-IndividualContributorLicenseAgreementOrthanc.pdf>`__.
  
2. Print the document, then write down your signed initials on pages 1
   and 2, and sign page 3.

3. Return a scanned copy of the document to e-mail ``orthanc-legal@osimis.io``.

4. Wait for confirmation from the Osimis company.

**Important:** This form is only valid for individual contributors
acting as physical persons. If your company wishes to become
contributor as a juridical person, please request a Corporate CLA at
the same e-mail address: ``orthanc-legal@osimis.io``.


.. _submitting_code:

Submitting code
^^^^^^^^^^^^^^^

Once the CLA onboarding process has succeeded, use `Mercurial
<https://en.wikipedia.org/wiki/Mercurial>`__ to fork the official
repository of interest. All the repositories are centralized on our
`self-hosted Mercurial server <https://orthanc.uclouvain.be/hg/>`__.

A :ref:`dedicated page <repositories>` explains how to submit
:ref:`simple patches <hg-patch>` or :ref:`full branches <hg-bundle>`.

**Some words of warning:**

* It is your responsibility to make sure that you have the
  intellectual property over all the source code you commit into
  Orthanc.

* In the case of a doubt wrt. a potential contribution, please discuss
  it on the `Orthanc Users discussion forum
  <https://discourse.orthanc-server.org>`__
  discussion group before starting the actual development.
