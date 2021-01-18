.. _contributing:


Contributing to Orthanc
=======================

.. toctree::
   :hidden:

   unanswered-forum.rst


.. note:: Here are the main features we would like to get soon
          implemented as free and open-source code in the Orthanc
          ecosystem. To make this happen, **we need your financial
          support**!

          * **Orthanc Core**:

            - Improved scalability of PostgreSQL databases
            - :ref:`Improved Web user interface <improving-interface>`
            - :ref:`DICOM TLS <security>`
          
          * **Stone Web viewer**:
     
            - Annotations/measurements
            - Internationalization/translations
            - MPR volume rendering
            - Viewer dedicated to nuclear medicine and radiotherapy
            - Rendering of DICOM GSPS

          * **Plugins**:

            - Support of MSSQL databases
            - :ref:`Worklist plugin <worklist>` to interface with REST API, HL7 or Myrth
            
          Please `get in touch with Osimis <info@osimis.io>`__ if you
          want to sponsor these developments.
   
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

    - **Important**: A page list the :ref:`old questions that are not
      fully answered yet <unanswered_forum>`. Consider answering these
      topics too!
    
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
    GNU/Linux distributions (e.g. Ubuntu PPA, RHEL/`EPEL
    <https://fedoraproject.org/wiki/EPEL>`__, CentOS, openSUSE...).
  - Take ownership of the now-orphaned `Fedora package
    <https://src.fedoraproject.org/rpms/orthanc>`__.
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
    + Conversion to/from `NIfTI
      <https://www.sciencedirect.com/science/article/abs/pii/S0165027016300073?via%3Dihub>`__
      and/or `BIDS
      <https://en.wikipedia.org/wiki/Brain_Imaging_Data_Structure>`__,
      notably for neuroimaging.
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
    + Have a look at the TODO file containing our `official roadmap
      <https://hg.orthanc-server.com/orthanc/file/default/TODO>`__.
  
  - Always remember that he **recommended way of contributing to the
    source code of Orthanc is by creating C/C++/Python plugins, or by
    creating external software that use the REST API**. If the current
    plugin SDK is insufficient for you to develop some feature as a
    plugin, do not hesitate to request an extension to the Orthanc SDK
    on the `mailing list
    <https://groups.google.com/forum/#!forum/orthanc-users>`_.


* **Financial support**:

  - Osimis provides `support packs and professional development
    services <https://www.osimis.io/en/services.html>`__ around the
    Orthanc ecosystem and, more generally, around medical
    imaging. Buying such professional services is the best way to make
    the Orthanc project sustainable in the long term.
