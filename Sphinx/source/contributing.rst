.. _contributing:


Contributing to Orthanc
=======================

.. toctree::
   :hidden:

   unanswered-forum.rst


.. note:: Here are the main features we would like to get soon
          implemented as free and open-source code in the Orthanc
          ecosystem. To make this happen, **we need your support**!

          * **Orthanc Core**:

            - Continue improving the :ref:`Orthanc Explorer 2 <orthanc-explorer-2>` User Interface
            - Support of DICOM C-GET SCU
   
          * **Stone Web viewer**:

            - Save/load annotations
            - Internationalization/translations
            - MPR volume rendering
            - Viewer dedicated to nuclear medicine and radiotherapy
            - Rendering of DICOM GSPS

          * **Plugins**:

            - :ref:`Worklist plugin <worklist>` to interface with REST API, HL7 or Mirth
            
          Please `get in touch with Sébastien Jodogne's research lab
          <https://uclouvain.be/fr/repertoires/sebastien.jodogne>`__
          if you want to use such features in the context of
          **research projects or scientific publications**, or `get in
          touch with the Orthanc Team <info@orthanc.team>`__ if you
          want to **financially sponsor** these developments.
   
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
  - Answer questions posted to the `Orthanc Users discussion forum
    <https://discourse.orthanc-server.org>`__.

    - **Important**: A page list the :ref:`old questions that are not
      fully answered yet <unanswered_forum>`. Consider answering these
      topics too!
    
  - Improve the text of the `Orthanc Book and REST API documentation
    <https://orthanc.uclouvain.be/hg/orthanc-book/file/default>`__ (check
    out the instructions provided in the `README file
    <https://orthanc.uclouvain.be/hg/orthanc-book/file/default/README.md>`__,
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
    <https://orthanc.uclouvain.be/bugs/>`_.
  - Package Orthanc and its associated plugins for more UNIX or
    GNU/Linux distributions (e.g. Ubuntu PPA, RHEL/`EPEL
    <https://fedoraproject.org/wiki/EPEL>`__, CentOS, openSUSE...).
  - Take ownership of the now-orphaned `Fedora package
    <https://src.fedoraproject.org/rpms/orthanc>`__. Check out the
    related `issue 1677806
    <https://bugzilla.redhat.com/show_bug.cgi?id=1677806>`__ and
    `issue 1843127
    <https://bugzilla.redhat.com/show_bug.cgi?id=1843127>`__.
  - Take care of :ref:`Debian/Ubuntu backporting <debian-packages>`.
  - Share your maintenance scripts or sample code inside the "`Orthanc Contributed
    <https://github.com/jodogne/OrthancContributed>`_" public GitHub
    repository, via pull requests.
  - Help with the integration of Orthanc together with our friend free
    and open-source projects, notably `GNU Health
    <https://www.orthanc-server.com/resources/orthanccon2019/GNUHealthCon-02-AxelBraun.pdf>`__,
    but also `OpenEMR
    <https://community.open-emr.org/t/project-pacs-server-integration/13706/15>`__,
    `GNUmed <https://en.wikipedia.org/wiki/GNUmed>`__...
    

* **Coding tasks**:
      
  - Have a look at the TODO file containing our `official roadmap
    <https://orthanc.uclouvain.be/hg/orthanc/file/default/TODO>`__.
  - The Orthanc project will happily accept patches in the core of
    Orthanc and in its associated official plugins. Please read the
    :ref:`dedicated FAQ entry <cla>`.
  - Interface Orthanc with other software (e.g. 3D Slicer,
    Matlab/Octave, Python, Horos, dicompyler...). Check the `already
    supported frameworks <https://www.orthanc-server.com/static.php?page=resources>`_.
  - Develop :ref:`C/C++/Python plugins extending the Orthanc core <plugins>`.  Here are some ideas
    of possible plugins:
  
    + Create a :ref:`more advanced Web interface
      <improving-interface>` than the built-in Orthanc Explorer.
    + Extend the :ref:`sample modality worklist plugin <worklist>` so
      that it manages the worklists (i.e. add/remove items) with a
      REST API or HL7 messages, instead of reading them from some
      folder on the filesystem.
    + `Encapsulate a video into a DICOM file
      <https://stackoverflow.com/questions/28698888/creating-h-264-avc-dicom-file-with-dcmtk/28737338#28737338>`__
      by calling some REST route, similarly to the
      ``/tools/create-dicom`` :ref:`route to encapsulate PDF <pdf>`.
    + Similarly to video and PDF (cf. item above), `wrap/unwrap a STL
      (3D mesh) to/from a DICOM file
      <http://dicom.nema.org/medical/dicom/2020b/output/chtml/part03/sect_A.85.html>`__
      by calling some REST route. This is notably useful for dentistry
      (dental implants) or orthopaedics, yet even cutting-edge
      research about 3D-printing of organs. In complement, provide a
      `FreeCAD extension
      <https://twitter.com/sjodogne/status/1299632772915625984>`__ to
      import/export such STL files from/to Orthanc.
    + Create a plugin to edit DICOM files (add, update or remove DICOM tags).
    + Create samples of :ref:`Python plugins <python-plugin>` or :ref:`Java plugins <java-plugin>` to take
      care of HL7 messages, especially for :ref:`merging patients
      <split-merge>` (which is a `typical HL7 event
      <https://twitter.com/ZeClint/status/1192086039160086529?s=20>`__
      to be handled by the PACS, not by the RIS). Reference: Events
      ``Axx`` of Chapter 3 ("Patient Administration") in the HL7 v2.9
      specification. ``ADT`` messages have also been `discussed in the
      past on the Orthanc forum
      <https://groups.google.com/g/orthanc-users/c/Spjtcj9vSPo/m/ktUArWxUDQAJ>`__.
    + Create a `DICOM proxy
      <https://groups.google.com/g/orthanc-users/c/15dYEm4Tguw/m/PoldpTOQAQAJ>`__
      (to share a single connection on a PACS by several DICOM
      clients/viewers), or a `DICOMweb proxy
      <https://groups.google.com/g/orthanc-users/c/AQ6qs0TgO6I/m/WxdOVEeKBAAJ>`__
      (to turn a DICOM-only PACS into a DICOMweb server). This could
      be done as a :ref:`Python plugin <python-plugin>` or as a :ref:`Java plugin <java-plugin>` by wrapping
      the C-FIND and C-MOVE callbacks in the Python API.
    + Get involved in the call for ideas by Salim Kanoun about a
      `DICOM router built on the top of Orthanc
      <https://groups.google.com/g/orthanc-users/c/tx7E1RQuKIY/m/_GsrRZljBgAJ>`__.
  
  - Always remember that he **recommended way of contributing to the
    source code of Orthanc is by creating C/C++/Python plugins, or by
    creating external software that use the REST API**. If the current
    plugin SDK is insufficient for you to develop some feature as a
    plugin, do not hesitate to request an extension to the Orthanc SDK
    on the `Orthanc Users discussion forum
    <https://discourse.orthanc-server.org>`__.


* **Financial support**: 

  - Check out our :ref:`FAQ about donations <donations>`.
  
  - Since February 2022, you are invited to fund the Orthanc project
    through its `Open Collective <https://opencollective.com/orthanc>`__
    page.  The funds collected there will help us maintain Orthanc,
    release new features and answer questions on the Orthanc Users Group.

  - Buying professional services is also a good way to make the Orthanc project 
    sustainable in the long term.  Check out the :ref:`professional services provided by our
    community <support-freelancers>`.
