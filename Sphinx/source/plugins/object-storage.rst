.. _object-storage:


Cloud Object Storage plugins
============================

.. contents::

Release notes
-------------

Release notes are available `here
<https://orthanc.uclouvain.be/hg/orthanc-object-storage/file/default/NEWS>`__ 
   
Introduction
------------

These 3 plugins enable storing the Orthanc files in `Object Storage <https://en.wikipedia.org/wiki/Object_storage>`__
at the 3 main Cloud providers: `AWS <https://aws.amazon.com/s3/>`__, 
`Azure <https://azure.microsoft.com/en-us/services/storage/blobs/>`__ & 
`Google Cloud <https://cloud.google.com/storage>`__

Storing Orthanc files in object storage and your index SQL in a 
managed database allows you to have a stateless Orthanc that does
not store any data in its local file system which is highly recommended
when deploying an application in the cloud.


Pre-compiled binaries
---------------------

These 3 plugins are provided as part of the ``osimis/orthanc`` :ref:`Docker images <docker-osimis>`.
The AWS plugin is available in the default Docker images while the Azure and Google plugins are available
in the ``-full`` images.

The Azure plugin is also available as part of the `Windows Installer
<https://orthanc.uclouvain.be/downloads/windows-64/installers/index.html>`__
(only for 64bits platform).

These plugins are used to interface Orthanc with commercial and
proprietary cloud services that you accept to pay. As a consequence,
the Orthanc project usually doesn't freely update them or fix them unless
the requester purchases a support contract e.g. at `Orthanc Team <https://orthanc.team>`__.

Although you are obviously free to compile these plugins by
yourself (instructions are given below), purchasing such support
contracts makes the Orthanc project sustainable in the long term, to
the benefit of the worldwide community of medical imaging.


Configuration
-------------

.. highlight:: json

AWS S3 plugin
^^^^^^^^^^^^^

Sample configuration::

  "AwsS3Storage" : {
    "BucketName": "test-orthanc-s3-plugin",
    "Region" : "eu-central-1",
    "AccessKey" : "AKXXX",                    // optional: if not specified, the plugin will use the default credentials manager (available from version 1.3.0)
    "SecretKey" : "RhYYYY",                   // optional: if not specified, the plugin will use the default credentials manager (available from version 1.3.0)
    "Endpoint": "",                           // optional: custom endpoint
    "ConnectionTimeout": 30,                  // optional: connection timeout in seconds
    "RequestTimeout": 1200,                   // optional: request timeout in seconds (max time to upload/download a file)
    "RootPath": "",                           // optional: see below
    "MigrationFromFileSystemEnabled": false,  // optional: see below
    "StorageStructure": "flat",               // optional: see below
    "EnableLegacyUnknownFiles": true,         // optional: see below
    "VirtualAddressing": true,                // optional: see the section related to MinIO
    "StorageEncryption" : {},                 // optional: see the section related to encryption
    "HybridMode": "Disabled",                 // optional: see the section related to Hybrid storage
    "UseTransferManager": false,              // optional: see below (available from version 2.3.0)
    "EnableAwsSdkLogs": false                 // optional: include AWS SDK logs in Orthanc logs
  }

The **EndPoint** configuration is used when accessing an S3 compatible cloud provider.  I.e. here is a configuration to store data on Scaleway::

 "AwsS3Storage" : {
    "BucketName": "test-orthanc",
    "Region": "fr-par",
    "AccessKey": "XXX",
    "SecretKey": "YYY",
    "Endpoint": "s3.fr-par.scw.cloud"
  }


The **UseTransferManager** configuration is used to select the `Transfer Manager <https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/examples-s3-transfermanager.html>`__ mode in the AWS SDK client.
This option was introduced in version 2.3.0.  If set to false (default value), the default "object" mode is used.


.. _minio:
  
Emulation of AWS S3 using MinIO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

The `MinIO project <https://min.io/>`__ can be used to emulate AWS S3
for local testing/prototyping. Here is a sample command to start a
MinIO server on your local computer using Docker (evidently, make sure
to set different credentials)::

  $ docker run -p 9000:9000 \
    -e "MINIO_REGION=eu-west-1" \
    -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" \
    -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MNG/bPxRfiCYEXAMPLEKEY" \
    minio/minio server /data

.. highlight:: json

Note that the ``MINIO_REGION`` must be set to an arbitrary region that
is supported by AWS S3.

You can then open the URL `http://localhost:9000/
<http://localhost:9000/>`__ with your Web browser to create a bucket,
say ``my-sample-bucket``.

Here is a corresponding full configuration for Orthanc::

  {
    "Plugins" : [ <...> ],
    "AwsS3Storage" : {
      "BucketName": "my-sample-bucket",
      "Region" : "eu-west-1",
      "Endpoint": "http://localhost:9000/",
      "AccessKey": "AKIAIOSFODNN7EXAMPLE",
      "SecretKey": "wJalrXUtnFEMI/K7MNG/bPxRfiCYEXAMPLEKEY",
      "VirtualAddressing" : false
    }
  }

Note that the ``VirtualAddressing`` option must be set to ``false``
for such a `local setup with MinIO to work
<https://github.com/aws/aws-sdk-cpp/issues/1425>`__. This option is
**not** available in releases <= 1.1.0 of the AWS S3 plugin.

**Important:** If you get the cryptic error message
``SignatureDoesNotMatch The request signature we calculated does not
match the signature you provided. Check your key and signing
method.``, this most probably indicates that your access key or your
secret key doesn't match the credentials that were used while starting
the MinIO server.
    

Azure Blob Storage plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Sample configuration::

  "AzureBlobStorage" : {
    "ConnectionString": "DefaultEndpointsProtocol=https;AccountName=xxxxxxxxx;AccountKey=yyyyyyyy===;EndpointSuffix=core.windows.net",
    "ContainerName" : "test-orthanc-storage-plugin",
    "CreateContainerIfNotExists": true,       // available from version 1.2.0
    "RootPath": "",                           // see below
    "MigrationFromFileSystemEnabled": false,  // see below
    "StorageStructure": "flat",               // see below
    "EnableLegacyUnknownFiles": true,         // optional: see below
    "StorageEncryption" : {}                  // optional: see the section related to encryption
    "HybridMode": "Disabled"                  // optional: see the section related to Hybrid storage
  }


Google Storage plugin
^^^^^^^^^^^^^^^^^^^^^

Sample configuration::

  "GoogleCloudStorage" : {
    "ServiceAccountFile": "/path/to/googleServiceAccountFile.json",
    "BucketName": "test-orthanc-storage-plugin",
    "RootPath": "",                           // see below
    "MigrationFromFileSystemEnabled": false,  // see below
    "StorageStructure": "flat",               // see below
    "EnableLegacyUnknownFiles": true,         // optional: see below
    "StorageEncryption" : {}                  // optional: see the section related to encryption
    "HybridMode": "Disabled"                  // optional: see the section related to Hybrid storage
  }


Migration & Hybrid mode Storage structure
-----------------------------------------

Since version **2.1.0** of the plugins, an HybridMode as been introduced.
This mode allows reading/writing files from both/to the file system and the object-storage.

By default, the ``HybridMode`` is ``Disabled``.  This means that the plugins will access
only the object-storage.

When the ``HybridMode`` is set to ``WriteToFileSystem``, it means that new files received
are stored on the file system.  When accessing a file, it is first read from the file system
and, if it is not found on the file system, it is read from the object-storage.

The ``WriteToFileSystem`` hybrid mode is useful for storing recent files on the file system for 
better performance and old files on the object-storage for lower cost and easier backups.

When the ``HybridMode`` is set to ``WriteToObjectStorage``, it means that new files received
are stored on the object storage.  When accessing a file, it is first read from the object storage
and, if it is not found on the object-storage, it is read from the file system.

The ``WriteToObjectStorage`` hybrid mode is useful mainly during a migration from file system to
object-storage, e.g, if you have deployed a VM in a cloud with local file system storage and want
to move your files to object-storage without interrupting your service.

Moving files between file-system and object-storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the ``HybridMode`` is set to ``WriteToFileSystem``, it is sometimes useful to move old files
to the object-storage for long term archive or to `pre-fetch` files from object-storage to file
system for improved performances e.g when before opening the study in a viewer.

When the ``HybridMode`` is set to ``WriteToObjectStorage``, it is useful to move file from the
file system to the object storage to perform a full data migration to object-storage.

To move files from one storage to the other, you should call the plugin Rest API::

    $ curl -X POST http://localhost:8042/move-storage \
      --data '{
                "Resources": ["27f7126f-4f66fb14-03f4081b-f9341db2-53925988"],
                "TargetStorage": "file-system",
                "Asynchronous": true,
                "Priority": 0
              }'

This call creates a ``MoveStorageJob`` that can then be monitor to the ``/jobs`` route.

The allowed values for ``TargetStorage`` are ``file-system`` or ``object-storage``.


Other configuration options
---------------------------

The **StorageStructure** configuration allows you to select the way objects are organized
within the storage (``flat`` or ``legacy``).  
Unlike the traditional file system in which Orthanc uses 2 levels
of folders, object storages usually have no limit on the number of files per folder and 
therefore all objects are stored at the root level of the object storage.  This is the
default ``flat`` behaviour.  Note that, in the ``flat`` mode, an extension `.dcm` or `.json`
is added to the filename which is not the case in the legacy mode.

The ``legacy`` behaviour mimics the Orthanc File System convention.  This is actually helpful
when migrating your data from a file system to an object storage since you can copy all the file
hierarchy as is.

The **RootPath** allows you to store the files in another folder as the root level of the
object storage.  Note: it shall not start with a ``/``.

Note that you can not change these configurations once you've uploaded the first files in Orthanc.

The **MigrationFromFileSystemEnabled** configuration has been superseded by the **HybridMode** in v 2.1.0.

The **EnableLegacyUnknownFiles** configuration has been introduced to allow recent version of the plugins (from 1.3.3)
continue working with data that was saved with Orthanc version around 1.9.3 and plugins version around 1.2.0 (e.g. osimis/orthanc:21.5.1 docker images).
With these specific versions, some ``.unk`` files were generated instead of ``.dcm.head`` files.  With this configuration option enabled,
when reading files, the plugin will try both file extensions.
If you have ``.unk`` files in your storage, you must enable this configuration.

Sample setups
-------------

You'll find sample deployments and more info in the `Orthanc Setup Samples repository <https://github.com/orthanc-server/orthanc-setup-samples/tree/master/#markdown-header-for-software-integrators>`__ .

Performances
------------

You'll find some performance comparison between VM SSDs and object-storage `here <https://github.com/orthanc-server/orthanc-setup-samples/tree/master/docker/performance-tests/>`__ .


.. _client-side-encryption:

Client-side encryption
----------------------

Although all cloud providers already provide encryption at rest, the plugins provide
an optional layer of client-side encryption .  It is very important that you understand 
the scope and benefits of this additional layer of encryption.

Rationale
^^^^^^^^^

Encryption at rest provided by cloud providers basically compares with a file-system disk encryption.  
If someone has access to the disk, he won't have access to your data without the encryption key.

With cloud encryption at rest only, if someone has access to the "api-key" of your storage or if one 
of your admin inadvertently make your storage public, `PHI <https://en.wikipedia.org/wiki/Protected_health_information>`__ will leak.

Once you use client-side encryption, you'll basically store packets of meaningless bytes on the cloud infrastructure.  
So, if an "api-key" leaks or if the storage is misconfigured, packets of bytes will leak but not PHI since
no one will be able to decrypt them.

Another advantage is that these packets of bytes might eventually not be considered as PHI anymore and potentially 
help you meet your local regulations (Please check your local regulations).

However, note that, if you're running entirely in a cloud environment, your decryption keys will still 
be stored on the cloud infrastructure (VM disks - process RAM) and an attacker could still eventually gain access to this keys.  

If Orthanc is running in your infrastructure with the Index DB on your infrastructure, and files are stored in the cloud, 
the master keys will remain on your infrastructure only and there's no way the data stored in the cloud could be decrypted outside your infrastructure.

Also note that, although the cloud providers also provide client-side encryption, we, as an open-source project, 
wanted to provide our own implementation on which you'll have full control and extension capabilities.  
This also allows us to implement the same logic on all cloud providers.

Our encryption is based on well-known standards (see below).  Since it is documented and the source code is open-source, 
feel-free to have your security expert review it before using it in a production environment.

Technical details
^^^^^^^^^^^^^^^^^

Orthanc saves 2 kind of files: DICOM files and JSON summaries of DICOM files.  Both files contain PHI.

When configuring the plugin, you'll have to provide a **Master Key** that we can also call the **Key Encryption Key (KEK)**.

For each file being saved, the plugin will generate a new **Data Encryption Key (DEK)**.  This DEK, encrypted with the KEK will be pre-pended to the file.

If, at any point, your KEK leaks or you want to rotate your KEKs, you'll be able to use a new one to encrypt new files that are being added 
and still use the old ones to decrypt data.  You could then eventually start a side script to remove usages of the leaked/obsolete KEKs.

To summarize:

- We use `Crypto++ <https://www.cryptopp.com/>`__ to perform all encryptions.  
- All keys (KEK and DEK) are AES-256 keys.
- DEKs and IVs are encrypted by KEK using CTR block cipher using a null IV.
- data is encrypted by DEK using GCM block cipher that will also perform integrity check on the whole file.

The format of data stored on disk is therefore the following:

- **VERSION HEADER**: 2 bytes: identify the structure of the following data currently `A1`
- **MASTER KEY ID**: 4 bytes: a numerical ID of the KEK that was used to encrypt the DEK
- **EIV**: 32 bytes: IV used by DEK for data encryption; encrypted by KEK
- **EDEK**: 32 bytes: the DEK encrypted by the KEK.
- **CIPHER TEXT**: variable length: the DICOM/JSON file encrypted by the DEK
- **TAG**: 16 bytes: integrity check performed on the whole encrypted file (including header, master key id, EIV and EDEK)

Configuration
^^^^^^^^^^^^^

.. highlight:: text

AES Keys shall be 32 bytes long (256 bits) and encoded in base64.  Here's a sample OpenSSL command to generate such a key::

  openssl rand -base64 -out /tmp/test.key 32

Each key must have a unique id that is a uint32 number.

.. highlight:: json

Here's a sample configuration file of the `StorageEncryption` section of the plugins::

  {
    "GoogleCloudStorage" : {
      "StorageEncryption" : {
        "Enable": true,
        "MasterKey": [3, "/path/to/master.key"], // key id - path to the base64 encoded key
        "PreviousMasterKeys" : [
            [1, "/path/to/previous1.key"],
            [2, "/path/to/previous2.key"]
        ],
        "MaxConcurrentInputSize" : 1024   // size in MB 
      }
    }
  }

**MaxConcurrentInputSize**: Since the memory used during encryption/decryption can grow up to a bit more 
than 2 times the input, we want to limit the number of threads doing concurrent processing according 
to the available memory instead of the number of concurrent threads.  Therefore, if you're currently
ingesting small files, you can have a lot of thread working together while, if you're ingesting large 
files, threads might have to wait before receiving a "slot" to access the encryption module.


Compilation
-----------

.. highlight:: text

The procedure to compile the plugins is quite similar of that for the
:ref:`core of Orthanc <compiling>` although they usually require 
some prerequisites.  The documented procedure has been tested only
on a Debian Buster machine.

The compilation of each plugin produces a shared library that contains 
the plugin.


AWS S3 plugin
^^^^^^^^^^^^^

Prerequisites: Compile the AWS C++ SDK::

  $ mkdir ~/aws
  $ cd ~/aws
  $ git clone https://github.com/aws/aws-sdk-cpp.git
  $ 
  $ mkdir -p ~/aws/builds/aws-sdk-cpp
  $ cd ~/aws/builds/aws-sdk-cpp
  $ cmake -DBUILD_ONLY="s3;transfer" ~/aws/aws-sdk-cpp 
  $ make -j 4 
  $ make install

Prerequisites: Install `vcpkg <https://github.com/Microsoft/vcpkg>`__ dependencies::

  $ ./vcpkg install cryptopp

Compile::

  $ mkdir -p build/aws
  $ cd build/aws
  $ cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]\scripts\buildsystems\vcpkg.cmake ../../orthanc-object-storage/Aws


**NB:** If you don't want to use vcpkg, you can use the following
command (this syntax is not compatible with Ninja yet)::

  $ cmake -DCMAKE_BUILD_TYPE=Debug -DUSE_VCPKG_PACKAGES=OFF -DUSE_SYSTEM_GOOGLE_TEST=OFF ../../orthanc-object-storage/Aws
  $ make

Crypto++ must be installed (on Ubuntu, run ``sudo apt install libcrypto++-dev``).


Azure Blob Storage plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisites: Install `vcpkg <https://github.com/Microsoft/vcpkg>`__ dependencies::

$ ./vcpkg install cryptopp
$ ./vcpkg install azure-storage-cpp


Compile::

  $ mkdir -p build/azure
  $ cd build/azure
  $ cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]\scripts\buildsystems\vcpkg.cmake ../../orthanc-object-storage/Azure

Google Storage plugin
^^^^^^^^^^^^^^^^^^^^^

Prerequisites: Install `vcpkg <https://github.com/Microsoft/vcpkg>`__ dependencies::

$ ./vcpkg install cryptopp
$ ./vcpkg install google-cloud-cpp

Compile::

  $ mkdir -p build/google
  $ cd build/google
  $ cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]\scripts\buildsystems\vcpkg.cmake ../../orthanc-object-storage/google
