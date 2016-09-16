.. highlight:: bash
.. _compiling-old:

Old build instructions for GNU/Linux
====================================

This page summarizes the GNU/Linux build instructions that were used
**up to Orthanc 0.7.0 (inclusive)**.  Instructions for Orthanc above
0.7.0 can be found directly `inside the source package
<https://bitbucket.org/sjodogne/orthanc/src/default/LinuxCompilation.txt>`_.

Static linking
--------------

In general, the static linking should work on any GNU/Linux
distribution (in particular, this works on Debian Squeeze)::

    $ cmake -DSTATIC_BUILD:BOOL=ON -DCMAKE_BUILD_TYPE=Debug

Peter Somlo provides `detailed instructions
<https://groups.google.com/d/msg/orthanc-users/hQYulBBvJvs/S1Pm125o59gJ>`_
to statically build Orthanc on a minimal Ubuntu installation.

Dynamic linking against system-wide libraries
---------------------------------------------

If you want to dynamically link against the system libraries, the
following CMake configurations have been reported to work.

Dynamic Linking on Ubuntu 11.10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ cmake "-DDCMTK_LIBRARIES=wrap;oflog" -DSTATIC_BUILD=OFF -DCMAKE_BUILD_TYPE=Debug

*Explanation:* You have to manually link against the ``wrap`` and
``oflog`` shared libraries because of a packaging error in
``libdcmtk``.

Dynamic Linking on Ubuntu 12.04 LTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ cmake "-DDCMTK_LIBRARIES=wrap;oflog" -DSTATIC_BUILD=OFF  -DUSE_DYNAMIC_GOOGLE_LOG:BOOL=OFF -DDEBIAN_USE_GTEST_SOURCE_PACKAGE:BOOL=ON -DCMAKE_BUILD_TYPE=Debug


Dynamic Linking on Ubuntu 12.10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ cmake "-DDCMTK_LIBRARIES=wrap;oflog" -DSTATIC_BUILD=OFF -DDEBIAN_USE_GTEST_SOURCE_PACKAGE:BOOL=ON -DCMAKE_BUILD_TYPE=Debug ..

Dynamic Linking on Debian Sid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ cmake -DSTATIC_BUILD:BOOL=OFF -DSTANDALONE_BUILD:BOOL=ON -DUSE_DYNAMIC_JSONCPP:BOOL=ON -DDEBIAN_USE_GTEST_SOURCE_PACKAGE:BOOL=ON -DCMAKE_BUILD_TYPE=Debug -DDCMTK_LIBRARIES="wrap;oflog"

This is the configuration from the `official Debian package
<http://anonscm.debian.org/cgit/debian-med/orthanc.git/tree/debian/orthanc.init>`_.

Dynamic Linking on Fedora 18 and 19
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ cmake -DSTATIC_BUILD:BOOL=OFF -DSTANDALONE_BUILD:BOOL=ON -DUSE_DYNAMIC_GOOGLE_LOG:BOOL=ON -DUSE_DYNAMIC_JSONCPP:BOOL=ON -DCMAKE_BUILD_TYPE=Debug

This is the configuration from the `official Fedora package
<http://pkgs.fedoraproject.org/cgit/orthanc.git/tree/orthanc.spec?h=f18>`_.

Static Linking on CentOS 6.3 and 6.4
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have to build and install `CMake 2.8 from source
<https://cmake.org/download/>`_, or you can use
the cmake28 package from `EPEL
<https://admin.fedoraproject.org/pkgdb/package/rpms/cmake28/>`_. The
``STATIC_BUILD=ON`` option will then work::

    $ /usr/local/bin/cmake -DSTATIC_BUILD:BOOL=ON -DCMAKE_BUILD_TYPE=Debug

*Thanks to Will Ryder.*
