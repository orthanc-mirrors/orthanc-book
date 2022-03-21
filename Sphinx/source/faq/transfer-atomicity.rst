.. _dcmtk-tricks:

How to guarantee study transfer atomicity ?
=========================================

.. contents::
   :depth: 3

Introduction
------------

There are multiple ways to transfer studies to an Orthanc instance.
Only a few of them provide a guarantee that the study has been
transferred completely.

**Notes**: 

* By ``transfer atomicity``, we mean the capability to transfer
  only full studies and make sure that if a transfer fails before
  it is complete, no partial data is saved in Orthanc.  The study is either
  fully stored or not stored at all.

* DICOM, in general, does not provide any way to detect that a study 
  is ``complete``.  Actually, a study is never ``complete`` since, e.g, 
  a viewing workstation or an AI algorithm can still add a new enhanced 
  series even years after the study has been acquired.
  However, it is still important, in many applications, to make sure
  that a study, in its current state, is fully transmitted to another
  destination.

* Both the **client/source** and the **server/destination** might be interrested
  in the transfer status.  Usually, the **client** will have a guarantee that the
  study was fully transmitted if it receives a successful answer from the server.
  On the **server** side, it is usually more complex to make sure that the
  full study has been received.


Summary
-------

+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+
| Transfer method                                  | What can the Client/source trust to make sure    | Can Server/destination trust ``StableStudy``  |                          
|                                                  | the full study has been stored in the server ?   | event to consider the study as complete ?     |
+==================================================+==================================================+===============================================+
| **C-Store**                                      | * If every C-Store receives a success status.    | No                                            |
|                                                  | * If ``/modalities/sample/store`` receives a     |                                               |
|                                                  |   200 or if job is successfull                   |                                               |
+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+
| **C-Store with storage commitment**              | * same as above                                  | No                                            |
|                                                  | * use storage commitment to check which          |                                               |
|                                                  |   instances are stored on destination            |                                               |
+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+
| **DicomWeb**                                     | * If client receives a 200                       | No                                            |
|                                                  | * If ``/dicom-web/servers/sample/stow`` returns  |                                               |
|                                                  |   a 200 or if job is successfull                 |                                               |
+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+
| **Orthanc Rest API**                             | * If every call to ``/instances`` receives a     | No                                            |
|                                                  |   200                                            |                                               |
|                                                  | * If ``/peers/sample/store`` receives a          |                                               |
|                                                  |   200 or if job is successfull                   |                                               |
+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+
| **Transfers accelerator plugin**                 | * If ``/transfers/send`` receives a              | Yes (provided that the client sends full      |
|                                                  |   200 or if job is successfull                   | study)                                        |
+--------------------------------------------------+--------------------------------------------------+-----------------------------------------------+


C-Store
-------

If you are sending a study to Orthanc via C-Store, the study will be
considered as ``stable`` after a given period of time (defined by
the configuration ``StableAge``).  This gives no guarantee at all that
the study has been fully transferred.  The sending modality may have 
paused transfer for a while and might resume in a few minutes.

Although inaccurate by design, the ``IsStable`` status in Orthanc is the 
best way to assume that a study has been fully transferred via DICOM.
The default value of ``60 seconds`` is appropriate for most setups.

**Note**:

* When Orthanc, acting as C-Store SCP, responds with a success status to a C-Store command,
  it means that the instance has already been saved in the DB and
  on the storage.



C-Store with storage commitment
-------------------------------

Since release 1.6.0, Orthanc supports :ref:`Storage Commitment <storage-commitment>`.
Storage commitment is not a guarantee of atomicity but simply provides a 
way to check that a set of instances have really been saved by Orthanc.

Given that Orthanc only responsds to C-Store with a success status once the
instance has really been saved in DB and on disk, storage commitment
actually do not provide any additional guarantee during transfer.


DicomWeb STOW-RS
----------------

:ref:`STOW-RS <dicomweb-stow-rs>` can be used to transfer studies to an Orthanc.
The STOW-RS request contains a list of DICOM instances to store in the destination
Orthanc (likely a complete study).

Files are stored as they are received which means that, if the transfer is interrupted, 
only a partial study may be stored on the destination.  Therefore, on the destination, 
a ``StableStudy`` event might be triggered even if the study was not fully received.


**Note**:

* In earlier Orthanc versions, ``ChunkedTransfers`` was disabled, and the whole study 
was transmitted in a single HTTP request and parsed only once the full HTTP request 
had been received.  Therefore, the whole study was stored at once on the destination.
However, note that ``ChunkedTransfers`` is enabled by default on every Orthanc server 
but it can be disabled in the client configuration.  Also note that studies bigger than 
2 GB can not be transferred with ``ChunkedTransfers`` disabled which means it is not 
recommended to perform transfers with disabled ``ChunkedTransfers``.



Orthanc Rest API
----------------

When transferring a study through the Orthanc Rest API, each instance is transferred individually.
Therefore, on server side, if the transfer is interrupted, the destination has no way to know that the study 
has been fully transmitted or not.

The server will respond with a 200 HTTP status only once the instance is stored in DB and on storage.



Transfers Accelerator plugin
----------------------------

:ref:`Transfers Accelerator plugin <transfers>` has been design to:

* speed up transfers over HTTP/HTTPS.
* guarantee the transfer atomicity

Provided that the client is sending a full study, the server receiving it
will store it completely.  Therefore, on server side, the ``StableStudy`` event will trigger only
on full studies.