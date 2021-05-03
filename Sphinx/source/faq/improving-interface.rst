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
Explorer is designed for development, low-level purpose.** It is
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
login/logout, Web diffusion to patients/physicians...). If you need
such a more advanced `user experience
<https://en.wikipedia.org/wiki/User_experience>`__ so that Orthanc
better fits your clinical workflow, you will have to develop a
separate, custom Web interface on the top of the :ref:`rest`, maybe as
a `plugin
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__. Any
front-end Web developer could take care of this task using well-known
JavaScript frameworks (such as Angular, Vue.js...).

It is possible that an official plugin that provides a more advanced
user interface will be developed in the future (provided we find
funding for this development). In the meantime, you can also contact
**Osimis**, the commercial partner of the Orthanc project, by using
the `contact form <https://www.orthanc-server.com/orthanc-pro.php>`_
that is available on the official Web page of Orthanc.

Finally, have a look to the following **related projects**:

* In 2017-2018, a team of Master students from `ULiège
  <https://www.uliege.be/>`__ has done some work about creating a
  revamped version of Orthanc Explorer. Check out the `related
  discussion
  <https://groups.google.com/d/msg/orthanc-users/oOyKTmfs-J0/B6eyBJcvCAAJ>`__
  on the Orthanc Users forum.

* `Orthanc Tools <https://github.com/salimkanoun/Orthanc_Tools>`__, a
  desktop Java interface around the REST API of Orthanc by Salim
  Kanoun. Orthanc Tools was notably showcased during `OrthancCon 2019
  <https://www.orthanc-server.com/static.php?page=conference-schedule>`__.
  
* `OrthancToolsJS <https://github.com/salimkanoun/Orthanc-Tools-JS>`__
  is the successor of the now-deprecated Orthanc Tools. This Web
  interface was also created by Salim Kanoun. For more information,
  including link to a demo server, `check out the announcement
  <https://groups.google.com/forum/#!msg/orthanc-users/L1BqXbD900E/CB8wOnQ_AwAJ>`__
  on the discussion group.

* The `Orthanc Manager <https://github.com/id-05/OrthancManager>`__
  Android application. `Check out the announcement
  <https://groups.google.com/forum/#!msg/orthanc-users/ToG4kbhK4Ss/CdFaexyvBwAJ>`__
  on the discussion group.

* `Elessar Theme for Orthanc <https://github.com/Terabuck/Elessar>`__
  by Ludwig Moreno. This PHP project notably provide a green and dark
  grey theme, and translation in 14 languages. `Check out the full
  announcement
  <https://groups.google.com/g/orthanc-users/c/Kkxqx6ZW2yw/m/dFbTuHZHCQAJ>`__
  on the discussion group.

* `Menba <https://github.com/fidelio33b/menba>`__ is a Web interface
  built on the top of the REST API of Orthanc. It is written using
  `Django <https://www.djangoproject.com/>`__ and `Bootstrap
  <https://getbootstrap.com/>`__, and takes advantage of `Celery
  <https://docs.celeryproject.org/en/stable/getting-started/introduction.html>`__
  and `AMQP
  <https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol>`__
  to handle the asynchronous tasks.

* Last but not least, as written above, please consider buying the
  `professional development services by Osimis
  <https://www.osimis.io/en/services.html>`__. Osimis can help medical
  and hospital audience with the deployment of a **certified,
  integrated clinical environment** around Orthanc. In turn, the money
  you pay will contribute to make the Orthanc project sustainable in
  the long term.
