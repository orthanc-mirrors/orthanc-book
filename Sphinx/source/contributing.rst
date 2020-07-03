.. _contributing:

Contributing to Orthanc
=======================

If you find Orthanc useful and wish to contribute to its development,
here are some tasks you can take in charge that would greatly help us:

* **Non-coding tasks**:
  
  - Use Orthanc in the real life. ;)
  - Advertise about Orthanc, notably on social networks (we are active
    on `Facebook <https://www.facebook.com/orthancdicom/>`__ and
    `Twitter <https://twitter.com/OrthancServer>`__).
  - Answer our `survey
    <https://www.orthanc-server.com/static.php?page=blog#survey>`_.
  - Improve and translate the `Wikipedia pages
    <https://en.wikipedia.org/wiki/Orthanc_(software)>`_ about Orthanc.
  - Cite the `reference paper about Orthanc
    <https://link.springer.com/article/10.1007/s10278-018-0082-y>`__
    in your research work.
  - Answer questions posted to the `mailing list
    <https://groups.google.com/forum/#!forum/orthanc-users>`_.
  - Improve the text of the `Orthanc Book and REST API documentation
    <https://hg.orthanc-server.com/orthanc-book/file/default>`__ (check
    out the instructions provided in the `README file
    <https://hg.orthanc-server.com/orthanc-book/file/default/README.md>`__,
    and send us a :ref:`simple patch <hg-patch>`).
  - Provide documentation and use cases (inside the dedicated `GitHub
    repository <https://github.com/jodogne/OrthancContributed>`_, via
    pull requests).
  - Index external contributions inside the `Links.md
    <https://github.com/jodogne/OrthancContributed/blob/master/Links.md>`_
    file.

* **Maintenance tasks**:
      
  - Report problems together with sample DICOM images and possible
    workarounds on the dedicated `issue tracker
    <http://bugs.orthanc-server.com/>`_.
  - Package Orthanc and its associated plugins for more UNIX or
    GNU/Linux distributions (e.g. Ubuntu PPA, RHEL, CentOS, openSUSE...).
  - Share your maintenance scripts or sample code inside the "`Orthanc Contributed
    <https://github.com/jodogne/OrthancContributed>`_" public GitHub
    repository, via pull requests.

* **Coding tasks**:
      
  - The Orthanc project will happily accept patches in the core of
    Orthanc and in its associated official plugins. Please read the
    :ref:`dedicated FAQ entry <cla>`.
  - Interface Orthanc with other software (e.g. 3D Slicer,
    Matlab/Octave, Python, Horos, dicompyler...). Check the `already
    supported frameworks <https://www.orthanc-server.com/static.php?page=resources>`_.
  - Develop :ref:`C/C++ plugins extending the Orthanc core <plugins>`.  Here are some ideas
    of possible plugins:
  
    + Create a :ref:`more advanced Web interface
      <improving-interface>` than the built-in Orthanc Explorer.
    + Extend the :ref:`sample modality worklist plugin <worklist>` so
      that it manages the worklists (i.e. add/remove items) with a
      REST API or HL7 messages, instead of reading them from some
      folder on the filesystem.
    + Have a look at the TODO file containing our `official roadmap
      <https://hg.orthanc-server.com/orthanc/file/default/TODO>`__.

  - Always remember that he **recommended way of contributing to the
    source code of Orthanc is by creating C/C++ plugins**. If the
    current plugin SDK is insufficient for you to develop some feature
    as a plugin, do not hesitate to request an extension to the
    Orthanc SDK on the `mailing list
    <https://groups.google.com/forum/#!forum/orthanc-users>`_.


* **Financial support**:

  - Buy commercial services:

    + Osimis provides `support packs
      <https://www.osimis.io/en/services.html>`__ dedicated to Orthanc.
    + Osimis can be hired to do `custom developments
      <https://www.orthanc-server.com/orthanc-pro.php>`__ related to medical imaging.
    + Currently, Osimis is the only company ensuring such corporate
      services according to an open-source business model, but others
      might show up in the future. `Please warn us
      <mailto:s.jodogne@orthanc-labs.com>`__ if your know about another such
      company!
