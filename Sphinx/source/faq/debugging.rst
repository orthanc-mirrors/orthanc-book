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
platform (e.g. Microsoft Visual Studio, gdb, cgdb, or Xcode).


GNU/Linux system using gdb
--------------------------

.. highlight:: bash

The Orthanc project provides precompiled binaries with debug symbols
for the mainline that can run on almost any recent GNU/Linux system
(generated thanks to the `LSB - Linux Standard Base SDK
<https://en.wikipedia.org/wiki/Linux_Standard_Base>`__). This allows
to debug Orthanc without compiling from sources. Here is a sample
debug session to analyze an error that comes from an invalid
:ref:`configuration file <configuration>`::

  $ wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/mainline-debug/Orthanc
  $ echo 'nope' > invalid.json
  $ chmod +x ./Orthanc
  $ gdb --args ./Orthanc invalid.json
  (gdb) catch throw
  Catchpoint 1 (throw)
  (gdb) run
  Starting program: /tmp/i/Orthanc invalid.json
  [Thread debugging using libthread_db enabled]
  Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
  W0103 18:25:01.540600             MAIN main.cpp:2041] Orthanc version: mainline (20240103T170440)
  W0103 18:25:01.540636             MAIN main.cpp:1775] Performance warning: Non-release build, runtime debug assertions are turned on
  W0103 18:25:01.540702             MAIN OrthancConfiguration.cpp:57] Reading the configuration from: "invalid.json"
  E0103 18:25:01.540823             MAIN OrthancException.cpp:61] Cannot parse a JSON document: The configuration file does not follow the JSON syntax: invalid.json

  Catchpoint 1 (exception thrown), 0x00007ffff7cae4a1 in __cxa_throw () from /lib/x86_64-linux-gnu/libstdc++.so.6
  (gdb) backtrace
  #0  0x00007ffff7cae4a1 in __cxa_throw () from /lib/x86_64-linux-gnu/libstdc++.so.6
  #1  0x0000000000473745 in Orthanc::AddFileToConfiguration (target=..., path=...)
      at /home/jodogne/BuildBotWorker/Orthanc_mainline_-_LSB_Debug/build/OrthancServer/Sources/OrthancConfiguration.cpp:72
  #2  0x0000000000473e98 in Orthanc::ReadConfiguration (target=..., configurationFile=0x7fffffffe302 "invalid.json")
      at /home/jodogne/BuildBotWorker/Orthanc_mainline_-_LSB_Debug/build/OrthancServer/Sources/OrthancConfiguration.cpp:149
  [...]

If you are unable to analyze such a backtrace by yourself, feel free
to post your backtrace on the `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__. Do not forget to indicate
the content of
`<https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/mainline-debug/revision.txt>`__
so that we can find the version of Orthanc that generated the core
file.

If you want to read the source code of the backtrace, it is highly
suggested to use ``cgdb`` with its ``set substitute-path`` command.
First read the content of the `revision.txt file
<https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc/mainline-debug/revision.txt>`__
to identify the revision of Orthanc. Then, you can type::

  $ hg clone -r 723251b2b71e https://orthanc.uclouvain.be/hg/orthanc/
  $ cgdb --args ./Orthanc invalid.json
  (gdb) set substitute-path /home/jodogne/BuildBotWorker/Orthanc_mainline_-_LSB_Debug/build/ ./orthanc/
  (gdb) catch throw
  (gdb) run
  (gdb) frame 2

  
Plugins
.......

Besides the Orthanc core, debug LSB binaries are also available for
most official plugins at the following location:
`<https://orthanc.uclouvain.be/downloads/linux-standard-base/index.html>`__

These binaries are identified as ``mainline-debug/``.
