.. _transfers:


Transfers accelerator plugin
============================

.. contents::

Osimis provides a `transfers accelerator plugin
<https://orthanc.uclouvain.be/hg/orthanc-transfers/file/default>`__ whose
purpose is to speed up the transfers of DICOM instances over networks
(with respect to the native DICOM protocol or to the built-in
:ref:`Orthanc peers <peers>` mechanism).


Description
-----------

This plugin can be used to **send** local images to remote Orthanc
peers, or to locally **retrieve** images stored on remote Orthanc
peers.

The plugin also implements **storage commitment**, i.e. the peer that
initiates the transfer is informed whether *all* the DICOM instances
have been properly received by the other peer. The DICOM instances are
individually validated using their MD5 checksum. In other words, this
plugin provides atomicity in the transfers (i.e. a study/series is
considered as a whole, and partial transfers are prevented).

Note that the protocol is **entirely built over HTTP/HTTPS** (and not
directly over TCP), making it friendly with network firewalls and Web
caches. Also, the plugin takes advantage of the **jobs engine** of
Orthanc, so that transfers can be easily paused/canceled/resubmitted.

Technically, this plugin extends the REST API of Orthanc with
endpoints that optimize the use of the network bandwidth over the HTTP
and HTTPS protocols, through the combination of the following
mechanisms:

* Small DICOM instances are grouped together to form so-called
  "buckets" of some megabytes in order to reduce the number of HTTP
  handshakes.

* Large DICOM instances are split as a set of smaller buckets in
  order to bypass nasty effects of TCP congestion control on
  low-quality network links.

* Buckets are downloaded/uploaded concurrently by several threads.

* Buckets can be individually compressed using the gzip algorithm,
  hereby reducing the network usage. On a typical medical image, this
  can divide the volume of the transmission by a factor 2 to 3, at
  the price of a larger CPU usage.

* Sending images to remote Orthanc peers can either be done with HTTP
  ``PUT`` requests (so-called "push mode"), or with HTTP ``GET``
  requests if the local Orthanc server has a public IP address
  (so-called "pull mode").



Compilation
-----------

Static linking
^^^^^^^^^^^^^^

.. highlight:: text

The procedure to compile the plugin is similar to that for the
:ref:`core of Orthanc <compiling>`. The following commands should work
for most UNIX-like distribution (including GNU/Linux)::

  $ mkdir BuildTransfers
  $ cd BuildTransfers
  $ cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
  $ make

The compilation will produce the shared library ``OrthancTransfers``
that can be loaded as a plugin by Orthanc.

  
Microsoft Windows
^^^^^^^^^^^^^^^^^

Pre-compiled binaries for Microsoft Windows `are available
<https://orthanc.uclouvain.be/downloads/windows-32/orthanc-transfers/index.html>`__.


Dynamic linking on Ubuntu 16.04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

If static linking is not desired, here are build instructions for
Ubuntu 16.04 (provided build dependencies for the :ref:`core of
Orthanc <compiling>` have already been installed)::

  $ mkdir BuildTransfers
  $ cd BuildTransfers
  $ cmake .. -DCMAKE_BUILD_TYPE=Release \
             -DALLOW_DOWNLOADS=ON \
             -DUSE_SYSTEM_GOOGLE_TEST=OFF \
             -DUSE_SYSTEM_ORTHANC_SDK=OFF
  $ make

  
Basic usage: Sending images
---------------------------

.. highlight:: json

You of course first have to :ref:`install Orthanc <binaries>`, with a
version above 1.4.2. Secondly, you have to load the plugin and to
**declare the remote Orthanc peers** in the :ref:`configuration file
<configuration>`. Here is a minimal example (obviously, adapt the
parameters)::

  {
    "Name" : "MyOrthanc",
    "Plugins" : [
      "/home/user/orthanc-transfers/BuildTransfers/libOrthancTransfers.so"
    ],
    "OrthancPeers" : {
      "remote" : [ "http://1.2.3.4:8042/" ]
    }
  }

Once Orthanc is running, when you open a patient, a study, or a series
in :ref:`Orthanc Explorer <orthanc-explorer>`, you will see a new
yellow button entitled ``Transfers accelerator``. By clicking on this
button, you will be able to send the local patient/study/series to one
of the remote Orthanc peers (provided they are also equipped with the
transfers accelerator plugin).


REST API
--------

.. highlight:: bash

Here is a sample command line to **receive** a patient from the remote
peer called ``remote``::

  $ curl -v -X POST http://localhost:8042/transfers/pull \
     --data '{
                "Resources" : [{"Level":"Patient","ID":"16738bc3-e47ed42a-43ce044c-a3414a45-cb069bd0"}],
                "Compression" : "gzip",
                "Peer" : "remote"
              }'



Note that several resources from different levels (patient, study,
series or instances) can be retrieved at once.

Conversely, here is a sample command line to **send** the same patient
to the remote peer ``remote``::

  $ curl -v -X POST http://localhost:8042/transfers/send \ 
     --data '{
              "Resources" : [{"Level":"Patient","ID":"16738bc3-e47ed42a-43ce044c-a3414a45-cb069bd0"}],
              "Compression" : "gzip",
              "Peer" : "remote"
            }'

The command above is the one that is issued by Orthanc Explorer under
the hood (see section above).



Sending in pull vs. push mode
-----------------------------

In the case DICOM instances are being **sent** to a remote peer, the
plugin can work in two different modes:

* In **"pull" mode**, the plugin will transfer images by using as many
  HTTP ``GET`` requests as possible.

* In **"push" mode**, it will use a sequence of HTTP ``PUT`` requests.

Push mode is easier to setup, but pull mode should be favored, as it
might lead to improved performance in the presence of Web caches.  For
pull mode to work, the remote peer must be able to make calls to the
REST API of the local peer. This often means that the local peer has a
public IP address.

In order to enable pull mode to send image from Orthanc peer "A" to
another Orthanc peer "B", 2 actions must be taken:

1. "B" must have "A" defined as one of its peers, by adding "A" to its
   ``OrthancPeers`` configuration section.

2. "A" must also have "B" defined as one of its peers, and the
   ``RemoteSelf`` property must be provided for peer "B". This option
   specifies the symbolic name under which "B" is known to "A".

.. highlight:: json

Here is a sample configuration for "A"::

  {
    "Name" : "A",
    "Plugins" : [
      "/home/user/orthanc-transfers/BuildTransfers/libOrthancTransfers.so"
    ],
    "OrthancPeers" : {
      "B" : {
        "Url" : "http://b.myinstitution.com:8042/",
        "RemoteSelf" : "A"
      }
    }
  }

And here is a sample configuration for "B"::

  {
    "Name" : "B",
    "Plugins" : [
      "/home/user/orthanc-transfers/BuildTransfers/libOrthancTransfers.so"
    ],
    "OrthancPeers" : {
      "A" : {
        "Url" : "http://a.myinstitution.com:8042/"
      }
    }
  }



NB: **Receiving** images is always done in pull mode.



Advanced options
----------------

Besides the ``OrthancPeers`` configuration option, several advanced
options are available to fine-tune the configuration of the
plugin. They are listed below::

  {
    ...
    "HttpTimeout" : 120,         // Can be increased on slow networks
    "Transfers" : {
      "Threads" : 6,             // Number of worker threads for one transfer
      "BucketSize" : 4096,       // Optimal size for a bucket (in KB)
      "CacheSize" : 128,         // Size of the memory cache to process DICOM files (in MB)
      "MaxPushTransactions" : 4, // Maximum number of simultaneous receptions in push mode
      "MaxHttpRetries" : 0,      // Maximum number of HTTP retries for one bucket
      "PeerConnectivityTimeout": 2 // HTTP Timeout (in seconds) used when checking if a remote peer has the transfer plugin enabled in /transfers/peers GET route
    }
  }


Working with load-balancers
---------------------------

.. highlight:: bash
  
If the receiving Orthanc instance is implemented by a cluster of Orthanc instances
behind a load-balancer, it is very important that all requests relating to a single
**"push"** transfer target the same Orthanc instance.

In order to achieve this, in your load-balancer, you may use the ``sender-transfer-id`` 
HTTP header to route the requests.  This header is populated in every outgoing HTTP request.  
By default, its value is a random uuid.  If required, you may force the value of this
HTTP header by adding a ``SenderTransferID`` field in the payload when creating
the transfer::

  $ curl -v -X POST http://localhost:8042/transfers/send \ 
     --data '{
              "Resources" : [{"Level":"Patient","ID":"16738bc3-e47ed42a-43ce044c-a3414a45-cb069bd0"}],
              "Compression" : "gzip",
              "Peer" : "remote",
              "SenderTransferID" : "my-transfer-id"
            }'
