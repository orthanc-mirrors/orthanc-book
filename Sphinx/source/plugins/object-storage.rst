.. _object-storage:


Cloud Object Storage plugins
============================

.. contents::

Release notes
-------------

Release notes are available `here
<https://hg.orthanc-server.com/orthanc-object-storage/file/default/NEWS>`__ 
   
Introduction
------------

Osimis freely provides the `source code
<https://hg.orthanc-server.com/orthanc-object-storage/file/default/>`__ of 3 plugins
to store the Orthanc files in `Object Storage <https://en.wikipedia.org/wiki/Object_storage>`__
at the 3 main providers: `AWS <https://aws.amazon.com/s3/>`__, 
`Azure <https://azure.microsoft.com/en-us/services/storage/blobs/>`__ & 
`Google Cloud <https://cloud.google.com/storage>`__

Storing Orthanc files in object storage and your index SQL in a 
managed database allows you to have a stateless Orthanc that does
not store any data in its local file system which is highly recommended
when deploying an application in the cloud.


Pre-compiled binaries
---------------------

These plugins are used to interface Orthanc with commercial and
proprietary cloud services that you accept to pay. As a consequence,
the Orthanc project doesn't freely provide pre-compiled binaries for
Docker, Windows, Linux or OS X. These pre-compiled binaries do exist,
but are reserved to the companies who have subscribed to a
`professional support contract
<https://www.osimis.io/en/services.html#cloud-plugins>`__ by
Osimis. Although you are obviously free to compile these plugins by
yourself (instructions are given below), purchasing such support
contracts makes the Orthanc project sustainable in the long term, to
the benefit of the worldwide community of medical imaging.


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

Azure Blob Storage plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisites: Install `vcpkg <https://github.com/Microsoft/vcpkg>`__ dependencies::

  $ ./vcpkg install cpprestsdk


Compile::

  $ mkdir -p build/azure
  $ cd build/azure
  $ cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]\scripts\buildsystems\vcpkg.cmake ../../orthanc-object-storage/Azure

Google Storage plugin
^^^^^^^^^^^^^^^^^^^^^

Prerequisites: Install `vcpkg <https://github.com/Microsoft/vcpkg>`__ dependencies::

  $ ./vcpkg install google-cloud-cpp
  $ ./vcpkg install cryptopp

Compile::

  $ mkdir -p build/google
  $ cd build/google
  $ cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]\scripts\buildsystems\vcpkg.cmake ../../orthanc-object-storage/google


Configuration
-------------

.. highlight:: json

AWS S3 plugin
^^^^^^^^^^^^^

Sample configuration::

  "AwsS3Storage" : {
  	"BucketName": "test-orthanc-s3-plugin",
    "Region" : "eu-central-1",
    "AccessKey" : "AKXXX",
    "SecretKey" : "RhYYYY",
    "Endpoint": "",                           // custom endpoint
    "ConnectionTimeout": 30,                  // connection timeout in seconds
    "RequestTimeout": 1200,                   // request timeout in seconds (max time to upload/download a file)
    "RootPath": "",                           // see below
    "MigrationFromFileSystemEnabled": false,  // see below
    "StorageStructure": "flat"                // see below
  }

The **EndPoint** configuration is used when accessing an S3 compatible cloud provider.  I.e. here is a configuration to store data on Scaleway::

 "AwsS3Storage" : {
    "BucketName": "test-orthanc",
    "Region": "fr-par",
    "AccessKey": "XXX",
    "SecretKey": "YYY",
    "Endpoint": "s3.fr-par.scw.cloud"
  },

Azure Blob Storage plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Sample configuration::

  "AzureBlobStorage" : {
    "ConnectionString": "DefaultEndpointsProtocol=https;AccountName=xxxxxxxxx;AccountKey=yyyyyyyy===;EndpointSuffix=core.windows.net",
    "ContainerName" : "test-orthanc-storage-plugin",
    "RootPath": "",                           // see below
    "MigrationFromFileSystemEnabled": false,  // see below
    "StorageStructure": "flat"                // see below
  }


Google Storage plugin
^^^^^^^^^^^^^^^^^^^^^

Sample configuration::

  "GoogleCloudStorage" : {
    "ServiceAccountFile": "/path/to/googleServiceAccountFile.json",
    "BucketName": "test-orthanc-storage-plugin",
    "RootPath": "",                           // see below
    "MigrationFromFileSystemEnabled": false,  // see below
    "StorageStructure": "flat"                // see below
  }


Migration & Storage structure
-----------------------------

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
object storage.

Note that you can not change these configurations once you've uploaded the first files in Orthanc.

The **MigrationFromFileSystemEnabled** configuration has been for Orthanc to continue working
while you're migrating your data from the file system to the object storage.  While this option is enabled,
Orthanc will store all new files into the object storage but will try to read/delete files
from both the file system and the object storage.

This option can be disabled as soon as all files have been copied from the file system to the 
object storage.  Note that Orthanc is not copying the files from one storage to the other; you'll
have to use a standard ``sync`` command from the object-storage provider.


Sample setups
-------------

You'll find sample deployments and more info in the `Orthanc Setup Samples repository <https://bitbucket.org/osimis/orthanc-setup-samples/src/master/#markdown-header-for-osimisorthanc-pro-image-users>`__ .


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

Another advantage is that these packets of bytes might eventually not be considered as PHI anymore and eventually 
help you meet your local regulations (Please check your local regulations).

However, note that, if you're running entirely in a cloud environment, your decryption keys will still 
be stored on the cloud infrastructure (VM disks - process RAM) and an attacker could still eventually gain access to this keys.  

If Orthanc is running in your infrastructure with the Index DB on your infrastructure, and files are store in the cloud, 
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
