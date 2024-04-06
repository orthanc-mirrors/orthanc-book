.. _java-plugin:


Java plugin for Orthanc
=======================

.. contents::


Overview
--------

This plugin can be used to write :ref:`Orthanc plugins
<creating-plugins>` using the `Java programming language
<https://en.wikipedia.org/wiki/Java_(programming_language)>`__ instead
of the more complex C/C++ programming languages.

Java plugins have access to more features and a more consistent SDK
than :ref:`Lua scripts <lua>`. The largest part of the Java API is
automatically generated from the `Orthanc plugin SDK in C
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.3/OrthancServer/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.

As of release 1.0 of the plugin, the coverage of the C SDK is about
76% (122 functions are automatically wrapped in Java out of a total of
160 functions from the Orthanc SDK 1.10.0).

**For researchers**: `Please cite this paper
<https://doi.org/10.5220/0012384600003657>`__.


Source code
-----------

* Link to the `official releases of this plugin
  <https://orthanc.uclouvain.be/downloads/sources/orthanc-java/index.html>`__.

* Link to the `code repository
  <https://orthanc.uclouvain.be/hg/orthanc-java/>`__.


Licensing
---------

This plugin is licensed under the terms of the `GPLv3+ license
<https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License>`__,
which is the same as the core of Orthanc.

This has an important consequence: If you distribute Orthanc to
clients together with one Java plugin, you **must** disclose the
source code of your Java script to the Orthanc community under the
terms of the GPL or AGPL licenses.

We suggest you to put the source code of your Java scripts on the
dedicated `"OrthancContributed" repository on GitHub
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__,
and/or to send it to the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__.

Check out the :ref:`FAQ about licensing <licensing>` for more context.


Usage
-----


FHIR server
-----------

