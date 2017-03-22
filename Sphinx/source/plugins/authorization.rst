.. _authorization:


Advanced authorization plugin
=============================

.. contents::

This **official plugin by Osimis** extends Orthanc with advanced
authorization mechanism.

For each incoming REST request to some URI, the plugin will query a
Web service to know whether the access is granted to the
user. Authorization credentials can be retrieved either from a GET
argument, or from a HTTP header.

Compilation
-----------

.. highlight:: bash

The procedure to compile these plugins is similar of that for the
:ref:`core of Orthanc <binaries>`. The following commands should work
for every UNIX-like distribution (including GNU/Linux)::

  $ mkdir Build
  $ cd Build
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce a shared library ``OrthancAuthorization``
that contains the authorization plugin.

Usage
-----

.. highlight:: json

You of course first have to :ref:`install Orthanc <compiling>`. Once
Orthanc is installed, you must change the :ref:`configuration file
<configuration>` to tell Orthanc where it can find the plugin: This is
done by properly modifying the ``Plugins`` option. You could for
instance use the following configuration file::

  {
    "Name" : "MyOrthanc",
    [...]
    "Plugins" : [
      "/home/user/OrthancAuthorization/Build/libOrthancAuthorization.so"
    ]
  }

.. highlight:: text

Orthanc must of course be restarted after the modification of its
configuration file.

Configuration
-------------

WIP

