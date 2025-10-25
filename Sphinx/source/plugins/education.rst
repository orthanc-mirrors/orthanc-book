.. _education:


Education plugin for Orthanc
============================

.. contents::


The Education plugin turns Orthanc into a tool for sharing medical
images with students for **educational purposes**. The plugin also
supports the **LTI 1.3 protocol**, allowing access from Learning
Management Systems such as Moodle.

The images can be displayed using the **Web viewers** that are
integrated as plugins for Orthanc (i.e., :ref:`Stone Web viewer
<stone_webviewer>`, :ref:`OHIF <ohif>`, and :ref:`Kitware VolView
<volview>`). The plugin also includes support for **virtual
microscopy**: It facilitates the DICOM-ization of whole-slide images
and offers a Web-based viewer through an intuitive interface to the
:ref:`whole-slide imaging primitives <wsi>` of Orthanc.

The Education plugin requires the version of Orthanc to be above or
equal to 1.12.9. It is released under the AGPL license. Note that this
plugin overwrites the way users are authenticated by Orthanc.

This development was partially funded by the `Virtual Hospital grant
<https://www.virtual-hospital.org/>`__ at `Louvain School of
Engineering (EPL) <https://www.uclouvain.be/facultes/epl>`__.


Overview
--------

The Orthanc plugin supports two modes of operation. The **standalone
mode** allows Orthanc to operate as a Web server for sharing
collections of medical images with learners. In this mode, instructors
can provide learners with a URL linking to a Web page that lists the
images in the collection, allowing them to view the images using their
preferred Web viewer. The following screenshot shows this page:

.. image:: education/standalone.png
           :align: center
           :width: 800

|

The second mode of operation integrates Orthanc with a **Learning
Management System (LMS)**, such as Moodle. This integration is
implemented according to the LTI protocol 1.3. Click on the following
image to view a demo video:

.. image:: education/moodle.jpeg
           :align: center
           :width: 800
           :target: https://www.youtube.com/watch?v=GD-oPukwxyc

|

In this video, the left portion of the screen presents the
administrative interface of the Education plugin, used to associate
medical images with **collections of images** (those collections are
referred to as "projects"). The right portion displays the Moodle user
interface, enabling learners to access the images and open Web viewers
managed by Orthanc. Contrarily to the standalone mode,

Both modes of operation include a **permission system** ensuring that
learners can only view images they are authorized to
access. Additionally, the Education plugin supports multiple
collections, which can be associated with different instructors.


Compilation
-----------

.. highlight:: bash

Official releases of the plugin can be `downloaded from the Orthanc
homepage
<https://orthanc.uclouvain.be/downloads/sources/orthanc-education/index.html>`__. As
an alternative, the `repository containing the source code
<https://orthanc.uclouvain.be/hg/orthanc-education/file/default>`__
can be accessed using Mercurial.

The procedure to compile this plugin is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
on most GNU/Linux distributions::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library
``libOrthancEducation.so`` that contains the Education plugin for
Orthanc.

Pre-compiled Linux Standard Base (LSB) binaries `are available for
download <https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc-education/index.html>`__.
Pre-compiled binaries for `Microsoft Windows <https://orthanc.uclouvain.be/downloads/windows-64/orthanc-education/index.html>`__
and `macOS <https://orthanc.uclouvain.be/downloads/macos/orthanc-education/index.html>`__ are available as well.

Furthermore, the :ref:`Docker images <docker>`
``jodogne/orthanc-plugins`` and ``orthancteam/orthanc`` also contain the
plugin. Debian and Ubuntu packages can be found in the
:ref:`standalone repository <binaries>`
``https://debian.orthanc-labs.com/``.


Terminology
-----------

This section introduces the various concepts that are necessary to
understand how the Education plugin for Orthanc works.


User management
^^^^^^^^^^^^^^^

The Education plugin for Orthanc makes the distinction between 3
categories of users:

* **Administrators** are responsible for the configuration of Orthanc
  and for the management of the collections of medical images
  (referred to as "projects"). It is up to the administrators to
  upload the DICOM images, to create the projects, to dispatch the
  images among the different projects, and to associate projects with
  instructors and learners.  To this end, administrators have access
  to the administrative interface of the Education plugin, as well as
  to :ref:`Orthanc Explorer <orthanc-explorer>` and :ref:`Orthanc
  Explorer 2 <orthanc-explorer-2>`.

* **Standard users** represent either instructors (teachers) or
  learners (students). These users cannot modify the configuration of
  the platform, upload medical images, or distribute images across
  projects. Instructors can modify project-specific settings based on
  their pedagogical objectives, such as controlling project visibility
  or selecting which viewers are available for a given project. A user
  may act as an instructor in certain projects and as a learner in
  others. For this reason, the "teacher vs. learner" terminology is
  avoided, as it implies a fixed role for each user.

* **Guest users** are users who are not authenticated by the
  platform. They behave like learners but can only access projects
  with public visibility. This functionality can be used to publish
  massive open online courses (MOOCs) through the standalone mode of
  operation.

The way the Education plugin authenticates administrators and standard
users is specified in the :ref:`configuration file of Orthanc
<configuration>`. The authentication process for administrators can
differ from the one used for standard users. As of release 1.0 of the
Education plugin, the following authentication mechanisms are
available:

* **Login**. In this case, the Education plugin displays a login page
  where the user can enter their credentials, which are specified in
  the configuration file. Internally, after a successful login, user
  information is stored as a `JWT
  <https://en.wikipedia.org/wiki/JSON_Web_Token>`__ session cookie
  named ``orthanc-education-user``.

* **HTTP headers**. In this case, the user identity is determined by
  the presence of a specific HTTP header, specified in the
  ``AuthenticationHttpHeader`` configuration option. This approach can
  be used in the standalone mode of operation, when `single sign-on
  (SSO) <https://en.wikipedia.org/wiki/Single_sign-on>`__ is
  implemented within an institution. At UCLouvain, this authentication
  mode has been validated with `Shibboleth
  <https://en.wikipedia.org/wiki/Shibboleth_(software)>`__ in
  combination with the ``libapache2-mod-shib`` module, with Apache
  acting as a :ref:`reverse proxy <apache>`. Two options are available
  for header-based authentication:

  * **Restricted**:

  * **Unrestricted**:



Precedence of cookies

Labels

HTTPS
