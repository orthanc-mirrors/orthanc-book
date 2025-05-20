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

Java applications for Orthanc have access to more features and a more
consistent SDK than :ref:`Lua scripts <lua>`. The largest part of the
Java API is automatically generated from the `Orthanc plugin SDK in C
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.7/OrthancServer/Plugins/Include/orthanc/OrthancCPlugin.h>`__
using the `Clang <https://en.wikipedia.org/wiki/Clang>`__ compiler
front-end.

As of release 1.0 of the plugin, **the coverage of the C SDK is about
74%** (122 functions are automatically wrapped in Java out of a total
of 165 functions from the Orthanc SDK 1.10.0).

**For researchers**: `Please cite this paper
<https://doi.org/10.5220/0012384600003657>`__.


How to get it ?
---------------

Binaries are included in:

- The `orthancteam/orthanc Docker image <https://hub.docker.com/r/orthancteam/orthanc>`__
- The `Windows Installer <https://www.orthanc-server.com/download-windows.php>`__

Release notes are available `here <https://orthanc.uclouvain.be/hg/orthanc-java/file/default/NEWS>`__.

Compilation instructions are available below.


Source code
-----------

* Link to the `official releases of this plugin
  <https://orthanc.uclouvain.be/downloads/sources/orthanc-java/index.html>`__.

* Link to the `code repository
  <https://orthanc.uclouvain.be/hg/orthanc-java/>`__.


Compilation
-----------

The Java plugin for Orthanc implies the compilation of two modules:

- The **plugin shared library**, which is needed for all users to run
  Java applications from within Orthanc, and

- The **Orthanc Java SDK**, which is needed for developers of Java
  applications for Orthanc.


.. _java_shared_library:

Shared library
^^^^^^^^^^^^^^

.. highlight:: text

If targeting **GNU/Linux distributions**, compiling the shared library
of the Java plugin (which is written in C++) works as follows::

  $ mkdir BuildPlugin
  $ cd BuildPlugin
  $ cmake ../Plugin -DCMAKE_BUILD_TYPE=Release
  $ make

This requires the `JNI (Java Native Interface)
<https://en.wikipedia.org/wiki/Java_Native_Interface>`__ to be
installed on your system (on Ubuntu setups, you can simply install the
``default-jdk`` package). This produces the ``libOrthancJava.so``
shared library. This shared library depends on the very specific
configuration of your system, so precompiled binaries are not
available.

If targeting **Microsoft Windows**, the supported way of compiling the
plugin consists in using the MinGW toolchains to cross-compile the
shared library on a GNU/Linux host::

  $ mkdir BuildWindows64
  $ cd BuildWindows64
  $ cmake ../Plugin -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_TOOLCHAIN_FILE=../Resources/Orthanc/Toolchains/MinGW-W64-Toolchain64.cmake
  $ make

This produces the ``libOrthancJava.dll`` shared library. Contrarily to
GNU/Linux distributions, precompiled binaries are available:

* For `Microsoft Windows 32 <https://orthanc.uclouvain.be/downloads/windows-32/orthanc-java/index.html>`__, and
* For `Microsoft Windows 64 <https://orthanc.uclouvain.be/downloads/windows-64/orthanc-java/index.html>`__.


.. _java_sdk:

Java SDK
^^^^^^^^

In addition to the shared library that is needed by all the users, the
developers of Java applications for Orthanc need a set of Java classes
that provide access to the native functions of the Orthanc plugin SDK.

The Orthanc Java SDK is available in the folder ``JavaSDK`` of the
source distribution. A ``.jar`` file containing the Orthanc Java SDK
can be compiled as follows::

  $ mkdir BuildJavaSDK
  $ cd BuildJavaSDK
  $ cmake ../JavaSDK
  $ make

This requires a JDK to be installed on your computer. This generates
the file ``OrthancJavaSDK.jar``. Alternatively, this cross-platform
``.jar`` library is available in a precompiled form at:

* The `following location
  <https://orthanc.uclouvain.be/downloads/cross-platform/orthanc-java/index.html>`__
  (evidently, make sure to download the version that matches your
  version of the ``libOrthancJava.so|.dll`` shared library).


Usage
-----

Here is a minimal example of a Java application for Orthanc:

.. literalinclude:: java/HelloWorld.java
                    :language: java

If both the :ref:`shared library <java_shared_library>` and the
:ref:`Java SDK <java_sdk>` are located in the current directory, here
is a :ref:`configuration file <configuration>` to run this sample Java
application on a GNU/Linux distribution:

.. literalinclude:: java/HelloWorld.json
                    :language: json

Orthanc can then be started as follows (the path to ``libjvm.so`` must
be adapted depending on your configuration)::

  $ javac HelloWorld.java -classpath ./OrthancJavaSDK.jar
  $ LD_PRELOAD=/usr/lib/jvm/java-11-openjdk-amd64/lib/server/libjvm.so ./Orthanc ./HelloWorld.json

On Microsoft Windows, one would use the following configuration file
(beware of the ``:`` that is replaced by ``;`` in the ``Classpath``
option):

.. literalinclude:: java/HelloWorldWindows.json
                    :language: json

This example simply outputs a line in the logs of Orthanc. Indeed, the
``static`` section of the class that is specified in the
``InitializationClass`` option is executed during the initialization
of the plugin.

You can find the full **Javadoc documentation of the Orthanc Java
SDK** `at the following location
<https://orthanc.uclouvain.be/javadoc/>`__.


Troubleshooting
---------------

Microsoft Windows
.................

Pre-compiled binaries for Microsoft Windows are now part of the 
`Windows installers <https://www.orthanc-server.com/download-windows.php>`__
but not installed by default.  They are also `available here
<https://orthanc.uclouvain.be/downloads/windows-64/orthanc-java/index.html>`__.

Pay also attention to pick the right 32/64 bits version.  If you are
running Orthanc 64bits, install Java in 64bits and select the 64bits
Java plugin too.

When you install Java on your Windows machine, make sure to add the path to 
``jvm.dll`` to your ``Path`` environment variable for at ``System`` level, not user level.
E.g: ``C:\Program Files\Java\jre-1.8\bin\server\``.

If you get the following error::
  
  LoadLibrary(C:\Program Files\Orthanc Server\Plugins\OrthancJava.dll) failed: Error 126

This very likely means that OrthancJava.dll can not find the ``jvm.dll``.  Check your system ``Path``.


If you get the following errors::
  
  LoadLibrary(C:\Program Files\Orthanc Server\Plugins\OrthancJava.dll) failed: Error 193
  Error while using a shared library (plugin): You are most probably trying to load a 32bit plugin into a 64bit version of Orthanc

This very likely means that Java 32bits has been installed on a 64bits version of Windows.

`Process Monitor <https://learn.microsoft.com/en-us/sysinternals/downloads/procmon>`__ 
should allow you to debug this type of errors.


Examples
--------

Adding a route in the REST API of Orthanc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New routes can be added to the REST API of Orthanc as follows:

.. literalinclude:: java/ExtendingRest.java
                    :language: java

Reacting to events
^^^^^^^^^^^^^^^^^^

Java applications can react to Orthanc events as follows:

.. literalinclude:: java/Changes.java
                    :language: java


Additional samples
^^^^^^^^^^^^^^^^^^

More advanced samples using Maven can be found `in the source
distribution of the Java plugin
<https://orthanc.uclouvain.be/hg/orthanc-java/file/default/Samples>`__.


FHIR server for Orthanc
-----------------------

Instructions for using the sample FHIR server for Orthanc that is
described in the `reference paper
<https://doi.org/10.5220/0012384600003657>`__ can be found in the
`source distribution
<https://orthanc.uclouvain.be/hg/orthanc-java/file/default/Samples/FHIR/>`__.

A precompiled version of the FHIR server is also available at the
`following location
<https://orthanc.uclouvain.be/downloads/cross-platform/orthanc-java/index.html>`__.



Licensing
---------

This plugin is licensed under the terms of the `GPLv3+ license
<https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License>`__,
which is the same as the core of Orthanc.

This has an important consequence: If you distribute Orthanc to
clients together with one Java plugin, you **must** disclose the
source code of your Java plugins to the Orthanc community under the
terms of the GPL or AGPL licenses.

We suggest you to put the source code of your Java plugins on the
dedicated `"OrthancContributed" repository on GitHub
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__,
and/or to send it to the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__.

Check out the :ref:`FAQ about licensing <licensing>` for more context.
