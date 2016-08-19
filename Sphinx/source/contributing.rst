.. _contributing:

Contributing to Orthanc
=======================

If you find Orthanc useful and wish to contribute to its development,
here are some tasks you can take in charge that would greatly help us:

* Use Orthanc in the real life. ;)
* Report possible problems together with sample DICOM images on the
  `issue tracker
  <https://bitbucket.org/sjodogne/orthanc/issues?status=new&status=open>`_.
* Answer questions posted to the `mailing list
  <https://groups.google.com/forum/#!forum/orthanc-users>`_.
* Index external contributions on the "`Orthanc Contributed
  <https://github.com/jodogne/OrthancContributed>`_" GitHub
  repository, via pull requests.
* Provide documentation and use cases (e.g. on `GitHub <https://github.com/jodogne/OrthancContributed>`_).
* Share maintenance scripts (e.g. on `GitHub <https://github.com/jodogne/OrthancContributed>`_).
* Advertise about Orthanc, and answer the `survey <http://www.orthanc-server.com/static.php?page=blog#survey>`_.
* Package Orthanc and its associated plugins for more UNIX or
  GNU/Linux distributions (e.g. RHEL, CentOS, SUSE...).
* Improve and translate the `Wikipedia page
  <https://en.wikipedia.org/wiki/Orthanc_(software)>`_ about Orthanc.
* Interface Orthanc with other software (e.g. 3D Slicer,
  Matlab/Octave, Python, Horos, dicompyler...). Check the `already
  supported frameworks <http://www.orthanc-server.com/static.php?page=resources>`_.
* Develop :ref:`C/C++ plugins extending the Orthanc core <plugins>`.  Here are some ideas
  of possible plugins:

  * Check the right-hand column of the `official roadmap <https://trello.com/b/cjA9X1wM/orthanc-roadmap>`__.
  * Create a :ref:`more advanced Web interface <improving-interface>` than the built-in Orthanc Explorer.
  * Extend the :ref:`sample modality worklist plugin <worklist>` so that it manages the worklists
    (i.e. add/remove items) with a REST API or HL7 messages, instead of reading them from 
    some folder on the filesystem.

* Have a look at the `Orthanc Wishlist board <https://trello.com/b/gcn33tDM/orthanc-wishlist>`__,
  where users can submit their ideas for the future features of Orthanc.

Always remember that he **recommended way of contributing to the source code of Orthanc is
by creating C/C++ plugins**. If the current plugin SDK is insufficient
for you to develop some feature as a plugin, do not hesitate to
request an extension to the Orthanc SDK on the `mailing list
<https://groups.google.com/forum/#!forum/orthanc-users>`_.

The University Hospital of Liège will also happily accept **external
patches** in the core of Orthanc and in its associated official
plugins, provided they are put in the public domain. Such patches must
be sent to the `mailing list
<https://groups.google.com/forum/#!forum/orthanc-users>`_ (*not* via a
pull request).
