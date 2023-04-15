.. _debugging:

Debugging Orthanc
=================

If you experience an error within Orthanc (or one of its plugins), that
the troubleshooting sections (cf. :ref:`here <troubleshooting>` and
:ref:`here <dicom>`) do not help, and that you can't provide a robust
way to reproduce your issue by third-party developers, you'll have to
analyze the backtrace of Orthanc.

If you observe a **fatal crash** of Orthanc, where Orthanc stops
abruptly (e.g. by creating a so-called "core dumped" or reporting an
invalid memory access), which rarely occurs, please check the
:ref:`dedicated section <crash>`). The present FAQ entry is rather
about C++ exceptions that are thrown by Orthanc, typically as a
consequence of invalid inputs, and that result in an error message
reported by Orthanc (not in a crash), and for which the :ref:`log
files in verbose mode <log>` do not provide meaningful information.

**Important reminder:** Most issues with Orthanc can be solved by
carefully looking at the :ref:`Orthanc logs <log>` after starting
Orthanc with the ``--verbose --trace-dicom`` command-line options!


Any system
----------

First :ref:`compile Orthanc by yourself <compiling>`, in debug mode by
setting ``-DCMAKE_BUILD_TYPE=Debug`` when invoking CMake.

Then, learn how to use the debugger that is best suited to your
platform (e.g. Microsoft Visual Studio, gdb or Xcode).


GNU/Linux system using gdb
--------------------------

.. highlight:: bash

The Orthanc project provides precompiled debug binaries that can be
run on almost any recent GNU/Linux system (generated thanks to the
`LSB - Linux Standard Base SDK
<https://en.wikipedia.org/wiki/Linux_Standard_Base>`__). This allows
to debug Orthanc without compiling from sources. Here is a sample
debug session::

  $ wget https://lsb.orthanc-server.com/orthanc/debug/1.12.0/Orthanc
  $ chmod +x ./Orthanc
  $ gdb ./Orthanc Configuration.json
  (gdb) catch throw
  Catchpoint 1 (throw)
  (gdb) run
  W0513 15:24:42.374349 main.cpp:1436] Orthanc version: 1.12.0
  ---> Reproduce your error case <---
  Thread 15 "Orthanc" hit Catchpoint 1 (exception thrown), 0x00007ffff6de68bd in __cxa_throw () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  (gdb) backtrace
  #0  0x00007ffff6de68bd in __cxa_throw ()
     from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  ...

If you are unable to analyze such a backtrace by yourself, feel free
to post your backtrace on the `Orthanc forum
<https://groups.google.com/forum/#!forum/orthanc-users>`__.

**Plugins:** Besides the Orthanc core, debug binaries of the official
plugins precompiled using the LSB are also available at the following
locations:

* `Orthanc core <https://lsb.orthanc-server.com/orthanc/debug/>`__
* `DICOMweb plugin <https://lsb.orthanc-server.com/plugin-dicom-web/debug/>`__
* `MySQL plugin <https://lsb.orthanc-server.com/plugin-mysql/debug/>`__
* `Orthanc Web viewer <https://lsb.orthanc-server.com/plugin-webviewer/debug/>`__
* `PostgreSQL plugin <https://lsb.orthanc-server.com/plugin-postgresql/debug/>`__
* `Transfers accelerator plugin <https://lsb.orthanc-server.com/plugin-transfers/debug/>`__
* `Whole-slide imaging <https://lsb.orthanc-server.com/whole-slide-imaging/debug/>`__
  

Docker
------

To be written.
