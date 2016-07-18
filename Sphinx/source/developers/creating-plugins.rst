Creating new plugins
====================

The recommended way of :ref:`contributing to the Orthanc code <contributing>`
is by extending it by :ref:`creating new plugins <plugins>`.

Overview
--------

Orthanc plugins must use the `plugin SDK
<https://orthanc.chu.ulg.ac.be/sdk/index.html>`__ and must be written
in C or C++. They must also fullfil the terms of the `GPLv3 license
<http://www.gnu.org/licenses/quick-guide-gplv3.en.html>`__ that is
used by the core of Orthanc. Sample code for plugins can be found `in
the official Orthanc repository
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/>`__
(in the ``Plugins/Samples`` folder of the ``plugins`` branch). A
tutorial showing how to implement a basic WADO server is `available on
CodeProject
<http://codeproject.com/Articles/797118/Implementing-a-WADO-Server-using-Orthanc>`__.

A plugin takes the form of a shared library (``.DLL`` under Windows,
``.so`` under Linux, ``.dylib`` under Apple OS X...) that must declare 4
public functions/symbols:

* ``int32_t OrthancPluginInitialize(OrthancPluginContext* context)``. This
  callback function is responsible for initializing the plugin. The
  ``context`` argument gives access to the API of Orthanc.
* ``void OrthancPluginFinalize()``. This function is responsible
  for finalizing the plugin, releasing all the allocated resources.
* ``const char* OrthancPluginGetName()``. This function must give a
  name to the plugin.
* ``const char* OrthancPluginGetVersion()``. This function must
  provide the version of the plugin.

We suggest developers to adopt the :ref:`coding style of the Orthanc
core <coding-style>`, although this is of course not required.

Do not hesitate to `contact us
<http://www.orthanc-server.com/static.php?page=contact>`__ if you wish
your plugin to be **indexed** in :ref:`this part of the Orthanc Book
<plugins-contributed>`!

