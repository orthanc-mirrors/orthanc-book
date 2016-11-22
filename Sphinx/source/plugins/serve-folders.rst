.. _serve-folders:


Sample Serve Folders plugin
===========================

This **official** plugin enables Orthanc to serve additional folders
from the filesystem using its embedded Web server. This plugin is
extremely useful when creating new Web applications on the top of the
REST API of Orthanc, as it allows to fulfill the :ref:`same-origin
policy <same-origin>` without setting up a reverse proxy.
 
The source code of this sample plugin is `available in the source
distribution of Orthanc
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ServeFolders/>`__
(GPLv3+ license).


Basic usage
-----------

1. First, generate the :ref:`default configuration of Orthanc <configuration>`.
2. Then, modify the ``Plugins`` option to point to the folder containing
   the shared library of the plugin.
3. Finally, create a section ``ServeFolders`` in the configuration file to
   specify which folder you want to serve, and at which URI.

.. highlight:: json

For instance, the following excerpt would load the plugins from the
working directory, then would map the content of the folder
``/home/jodogne/WWW/fosdem`` as URI "http://localhost:8042/fosdem"::

  {
    [...]
    "Plugins" : [ 
      "."
    ],
    "ServeFolders" : {
      "/fosdem" : "/home/jodogne/WWW/fosdem"
    }
  }

