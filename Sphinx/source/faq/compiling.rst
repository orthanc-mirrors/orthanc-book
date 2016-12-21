.. _compiling:

Compiling Orthanc
=================

Under GNU/Linux
---------------

* Orthanc >= 0.7.1: See the `build instructions
  <https://bitbucket.org/sjodogne/orthanc/src/default/LinuxCompilation.txt>`_
  inside the source package.
* Orthanc <= 0.7.0: See the :ref:`compiling-old`.

Under Microsoft Windows
-----------------------

See the `build instructions for Windows
<https://bitbucket.org/sjodogne/orthanc/src/default/INSTALL>`_ inside
the source package.

Under OS X
----------

The mainline of Orthanc can compile under Apple OS X, with the XCode
compiler, since June 24th, 2014. See the `build instructions for
Darwin
<https://bitbucket.org/sjodogne/orthanc/src/default/DarwinCompilation.txt>`_
inside the source package.

Performance warning
-------------------

If performance is important to you, make sure to add the option
``-DCMAKE_BUILD_TYPE=Release`` when invoking ``cmake``. Indeed, by
default, `run-time debug assertions
<https://en.wikipedia.org/wiki/Assertion_(software_development)#Assertions_for_run-time_checking>`_
are enabled, which can seriously impact performance, especially if
your Orthanc server stores a lot of DICOM instances.



Please explain the build infrastructure
---------------------------------------

The build infrastructure of Orthanc is based upon `CMake
<https://cmake.org/>`_. The build scripts are designed to embed all
the third-party dependencies directly inside the Orthanc
executable. This is the meaning of the ``-DSTATIC_BUILD=ON`` option,
as described in the `INSTALL
<https://bitbucket.org/sjodogne/orthanc/src/default/INSTALL>`_ file of Orthanc.

Such a static linking is very desirable under Windows, since the
Orthanc binaries do not depend on any external DLL, which results in a
straightforward installation procedure (just download the Windows
binaries and execute them), which eases the setup of the development
machines (no external library is to be manually installed, everything
is downloaded during the build configuration), and which avoids the
`DLL hell <https://en.wikipedia.org/wiki/Dll_hell>`_. As a downside,
this makes our build infrastructure rather complex.

Static linking is not as desirable under GNU/Linux than under
Windows. GNU/Linux prefers software that dynamically links against the
system-wide libraries: This is explained by the fact that whenever a
third-party dependency benefits from a bugfix, any software that is
linked against it also immediately benefits from this fix. This also
reduces the size of the binaries as well as the build time. Under
GNU/Linux, it is thus recommended to use the ``-DSTATIC_BUILD=OFF``
option whenever possible.

When the dynamic build is used, some third-party dependencies may be
unavailable or incompatible with Orthanc, depending on your GNU/Linux
distribution. Some CMake options have thus been introduced to force
the static linking against some individual third-party
dependencies. Here are the most useful:

* ``-DUSE_SYSTEM_DCMTK=OFF`` to statically link against DCMTK.
* ``-DUSE_SYSTEM_JSONCPP=OFF`` to statically link against JsonCpp.

You will also have to set the ``-DALLOW_DOWNLOADS=ON`` to explicitely
allow the CMake script to download the source code of any required
dependency. The source code of all these dependencies is self-hosted
on the Web server running our official homepage.

Please also note that the option ``-DSTANDALONE_BUILD=ON`` must be
used whenever your plan to move the binaries or to install them on
another computer. This option will embed all the external resource
files (notably Orthanc Explorer) into the resulting executable. If
this option is set to ``OFF``, the resources will be read from the
source directories.


Missing ``uuid-dev`` package
----------------------------

Orthanc might fail to compile, complaining about missing ``uuid-dev`` package. 

This problem seems to occur when fist building Orthanc without the
``uuid-dev`` package installed, then installing ``uuid-dev``, then
rebuilding Orthanc. It seems that the build scripts do not update the
cached variable about the presence of ``uuid-dev``.

To solve this problem, `as reported
<https://groups.google.com/d/msg/orthanc-users/hQYulBBvJvs/S1Pm125o59gJ>`_
by Peter Somlo, it is necessary to entirely remove the build directory
(e.g. with ``rm -rf Build``) and start again the build from a fresh
directory.
