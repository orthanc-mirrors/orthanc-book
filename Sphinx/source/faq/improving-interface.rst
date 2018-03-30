.. _improving-interface:

Orthanc Explorer is not user-friendly enough for my use
=======================================================

Orthanc is designed as a lightweight service for medical imaging,
where the word *service* must be understood in the sense of
`service-oriented architectures
<https://en.wikipedia.org/wiki/Service-oriented_architecture>`__.  As
a consequence, Orthanc is conceived as a robust back-end server
(command-line) that aims to provide the most simple and generic
support of DICOM. To state it differently, **the primary focus of the
Orthanc project is not on the user interface**.

However, Orthanc comes out-of-the-box with :ref:`Orthanc Explorer
<orthanc-explorer>`, its default Web user interface. **Orthanc
Explorer is designed for administrative, low-level purpose.** It is
also used by the development team to test the features of Orthanc as
they get introduced in the REST API. Orthanc Explorer is mainly
targeted towards an English-speaking technical audience (notably
system/network engineers, `PACS
<https://en.wikipedia.org/wiki/Picture_archiving_and_communication_system>`__
managers, medical physicists, and researchers).

**Non-technical audience** (physicists, patients, administrative
staff...) **might expect an user interface that is more user-friendly
than Orthanc Explorer**, and/or that integrates more features (such as
language translations, sorting resources, access control lists,
tagging images, beautiful layout, tunable anonymization, modification
of instances, paging if many patients, handling of timeouts,
login/logout...). If you need such a more advanced `user experience
<https://en.wikipedia.org/wiki/User_experience>`__ so that Orthanc
better fits your clinical workflow, you will have to develop a
separate, custom Web interface on the top of the :ref:`rest`, maybe as
a `plugin
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__. Any
front-end Web developer could take care of this task using well-known
JavaScript frameworks (such as Meteor, AngularJS, Ember.js...).

It is possible that an official plugin that provides a more advanced
user interface will be developed in the future (provided we find
funding for this development). In the meantime, you can also contact a
company that provides **commercial support on the top of Orthanc** and
that might have developed an advanced user interface. Currently,
`Osimis <http://osimis.io/>`_ is the only company ensuring such
corporate services, but others might show up in the future. A `contact
form <http://www.orthanc-server.com/orthanc-pro.php>`_ is available on
the official Web page of Orthanc.

**Update (2017-10-03):** A team of Master students from `ULiège
<https://www.uliege.be/>`__ is currently working on creating a
revamped version of Orthanc Explorer. You can get in touch with them
on the `public discussion forum
<https://groups.google.com/d/msg/orthanc-users/oOyKTmfs-J0/B6eyBJcvCAAJ>`__.
