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


Advanced usage
--------------

Starting with Orthanc 1.2.0, the Serve Folders plugin features some
more advanced configuration options, besides simply the list of
folders to be served:

* The **MIME types** associated with the file extensions can be
  configured through the ``Extensions`` option. By default, the most
  common file extensions for Web applications such as ``.html``,
  ``.js`` and ``.css`` are defined.
* The HTTP client can be asked to enable/disable its **caching
  mechanism** with the ``AllowCache`` option. By default, this option
  is set ``false`` (request no caching), as the most common use for
  this plugin consists in supporting the development of Web
  applications (with which caching would interfere). Note that this
  option is only informative: The client might choose to ignore it.
* The plugin will automatically generate an `HTTP entity tag
  <https://en.wikipedia.org/wiki/HTTP_ETag>`__ (**ETag**) for each
  served resource, if the ``GenerateETag`` option is set to ``true``
  (the default). The ETag is computed as the MD5 of the resource and
  acts as a fingerprint.

If one of these advanced options is used, the list of served folders
must be moved to a ``Folders`` sub-option. Here is an example of such
an advanced configuration::

  {
    [...]
    "Plugins" : [ 
      "."
    ],
    "ServeFolders" : {
      "AllowCache" : false,
      "GenerateETag" : true,
      "Extensions" : {
        ".mp4" : "video/mp4"
      },
      "Folders" : {
        "/fosdem" : "/home/jodogne/WWW"
      }
    }
  }
