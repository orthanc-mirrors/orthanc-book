.. highlight:: bash
.. _anonymization:

Anonymization and modification
==============================

.. contents::
   :depth: 2

Orthanc 0.5.0 introduces the anonymization of DICOM resources
(i.e. patients, studies, series or instances). This page summarizes
how to use this feature.


Anonymization of a Single Instance
----------------------------------

Orthanc allows to anonymize a single DICOM instance and to download
the resulting anonymized DICOM file. Anonymization consists in erasing
all the tags that are specified in Table E.1-1 from PS 3.15 of the
DICOM standard 2008 or 2017c (default). Example::

    $ curl http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/anonymize -X POST -d '{}' > Anonymized.dcm

It is possible to control how anonymization is achieved by specifying
a JSON body::

    $ curl http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/anonymize -X POST -d '{"Replace":{"PatientName":"Hello","0010-1001":"World"},"Keep":["StudyDescription", "SeriesDescription"],"KeepPrivateTags": true, "DicomVersion" : "2017c"}' > Anonymized.dcm

Explanations:

* New UUIDs are automatically generated for the study, the series and
  the instance.
* The DICOM tags can be specified either by their name
  (``PatientName``) or by their hexadecimal identifier (in the example
  above, ``0010-1001`` corresponds to ``Other Patient Names``).
* ``Replace`` is an associative array that associates a DICOM tag with its
  new string value. The value is dynamically cast to the proper DICOM
  data type (an HTTP error will occur if the cast fails). Replacements
  are applied after all the tags to anonymize have been removed.  
  You may also use the ``Replace`` field to add new tags to the file.
* ``Keep`` specifies a list of tags that should be preserved from full
  anonymization.
* If ``KeepPrivateTags`` is set to ``true`` in the JSON request,
  private tags (i.e. manufacturer-specific tags) are not removed by
  the anonymization process. The default behavior consists in removing
  the private tags, as such tags can contain patient-specific
  information.
* ``DicomVersion`` specifies which version of the DICOM standard shall be used
  for anonymization.  Allowed values are ``2008`` and ``2017c`` (default value 
  if the parameter is absent).  This parameter has been introduced in Orthanc 
  1.3.0.  In earlier version, the ``2008`` standard was used.


Modification of a Single Instance
---------------------------------

Orthanc allows to modify a set of specified tags in a single DICOM
instance and to download the resulting anonymized DICOM
file. Example::

    $ curl http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/modify -X POST -d '{"Replace":{"PatientName":"hello","PatientID":"world"},"Remove":["InstitutionName"],"RemovePrivateTags": true, "Force": true}' > Modified.dcm

Remarks:

* The ``Remove`` array specifies the list of the tags to remove.
* The ``Replace`` associative array specifies the substitions to be applied (cf. anonymization).
* If ``RemovePrivateTags`` is set to ``true``, the private tags
  (i.e. manufacturer-specific tags) are removed.
* The ``Force`` option must be set to ``true``, in order to allow the
  modification of the ``PatientID``, as such a modification of the
  :ref:`DICOM identifiers <dicom-identifiers>` might lead to breaking
  the DICOM model of the real-world. In general, any explicit
  modification to one of the ``PatientID``, ``StudyInstanceUID``,
  ``SeriesInstanceUID``, and ``SOPInstanceUID`` requires ``Force`` to
  be set to ``true``, in order to prevent any unwanted side effect.     

.. highlight:: json

* To replace a sequence of tags, you may use this syntax:: 


    {
      "Replace" : {
        "ProcedureCodeSequence" : [	
          {
            "CodeValue" : "2",	
            "CodingSchemeDesignator" : "1",	
            "CodeMeaning": "1" 
          }
        ]
      }
    }

* To replace a binary tag, you should encode it in base64 and use::

    {
      "Replace" : {
        "EncryptedAttributesSequence" : [
          {
            "EncryptedContentTransferSyntaxUID" : "1.2.840.10008.1.2",
            "EncryptedContent" : "data:application/octet-stream;base64,SSB3YXMgaGVyZSBpbiAyMDE5LiAgTWFydHkgTWNGbHku"
          }
        ]
      }
    }

Modification of Studies or Series
---------------------------------

.. highlight:: bash

It is possible to modify all the instances from a study or from a
series in a single request. In this case, the modified instances are
stored back into the Orthanc store. Here is how to modify a series::

    $ curl http://localhost:8042/series/95a6e2bf-9296e2cc-bf614e2f-22b391ee-16e010e0/modify -X POST -d '{"Replace":{"InstitutionName":"My own clinic"}}'


.. highlight:: json

The parameters are identical to those used to modify a single
instance. Orthanc will answer a JSON message that tells where the
modified series has been stored::

    {
      "ID" : "3bd3d343-82879d86-da77321c-1d23fd6b-faa07bce",
      "Path" : "/series/3bd3d343-82879d86-da77321c-1d23fd6b-faa07bce"
    }


.. highlight:: bash

Similarly, here is an interaction to modify a study::

    $ curl http://localhost:8042/studies/ef2ce55f-9342856a-aee23907-2667e859-9f3b734d/modify -X POST -d '{"Replace":{"InstitutionName":"My own clinic"}}'

.. highlight:: json

::

    {
      "ID" : "1c3f7bf4-85b4aa20-236e6315-5d450dcc-3c1bcf28",
      "Path" : "/studies/1c3f7bf4-85b4aa20-236e6315-5d450dcc-3c1bcf28"
    }


Modification of Patients
------------------------

.. highlight:: bash

Starting with Orthanc 0.7.5, Orthanc can also modify all the instances
of a patient with a single REST call. Here is a sample::

    $ curl http://localhost:8042/patients/6fb47ef5-072f4557-3215aa29-f99515c1-6fa22bf0/modify -X POST -d '{"Replace":{"PatientID":"Hello","PatientName":"Sample patient name"},"Force":true}'

.. highlight:: json

::

    {
      "ID" : "f7ff9e8b-7bb2e09b-70935a5d-785e0cc5-d9d0abf0",
      "Path" : "/patients/f7ff9e8b-7bb2e09b-70935a5d-785e0cc5-d9d0abf0",
      "PatientID" : "f7ff9e8b-7bb2e09b-70935a5d-785e0cc5-d9d0abf0",
      "Type" : "Patient"
    }

Please note that, in this case, you have to set the value of the
``PatientID (0010,0020)`` tag for Orthanc to accept this modification:
This is a security to prevent the merging of patient data before and
after anonymization, if the user does not explicitly tell Orthanc to
do so.


Anonymization of Patients, Studies or Series
--------------------------------------------

.. highlight:: bash

Study and series can be anonymized the same way as they are modified::

    $ curl http://localhost:8042/patients/6fb47ef5-072f4557-3215aa29-f99515c1-6fa22bf0/anonymize -X POST -d '{}'
    $ curl http://localhost:8042/studies/ef2ce55f-9342856a-aee23907-2667e859-9f3b734d/anonymize -X POST -d '{}'
    $ curl http://localhost:8042/series/95a6e2bf-9296e2cc-bf614e2f-22b391ee-16e010e0/anonymize -X POST -d '{}'

As written above, the anonymization process can be fine-tuned by using
a JSON body.


.. _split-merge: 

Split/merge of DICOM studies
----------------------------

Starting with Orthanc 1.5.0, Orthanc supports splitting and merging
DICOM studies through its REST API.

.. _split:

Splitting
^^^^^^^^^

Here is the syntax to **split** a DICOM study::

  $ curl http://localhost:8042/studies/6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12/split -d \
         '{"Series":["6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228"],"Replace":{"PatientName":"HELLO"},"Remove":["AccessionNumber"]}'

By issuing this command, the series whose :ref:`Orthanc identifier
<dicom-identifiers>` is
``6ca4c9f3-5e895cb3-4d82c6da-09e060fe-9c59f228``, and that is part of
the source study with identifier
``6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12``, will be removed from
the source study, and will be moved to a brand new study.

This is done by generating a new value for all the following DICOM
tags in the DICOM instances of the series of interest:
``StudyInstanceUID (0x0020, 0x000d)``, ``SeriesInstanceUID (0x0020,
0x000e)``, and ``SOPInstanceUID (0x0008, 0x0018)``. Here are the
arguments of this ``/studies/{study}/split`` URI:

* ``Series`` gives the list of series to be separated from the parent
  study (mandatory option).  These series must all be children of the
  same source study, that is specified in the URI.
* ``Replace`` allows to overwrite the DICOM tags that are part of the
  "Patient Module Attributes" and the "General Study Module
  Attributes", as specified by the DICOM 2011 standard in Tables C.7-1
  and C.7-3.
* ``Remove`` allows to remove DICOM tags from the same modules as in
  the ``Replace`` options.
* ``KeepSource`` (Boolean value), if set to ``true``, instructs
  Orthanc to keep a copy of the original series in the source study.
  By default, the original series are deleted from Orthanc.

.. _merge:

Merging
^^^^^^^

Here is the syntax to **merge** DICOM series, into another DICOM study::

  $ curl http://localhost:8042/studies/6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12/merge -d \
         '{"Resources":["ef2ce55f-9342856a-aee23907-2667e859-9f3b734d"]}'

By issuing this command, the DICOM series whose :ref:`Orthanc
identifier <dicom-identifiers>` is
``ef2ce55f-9342856a-aee23907-2667e859-9f3b734d``, will be merged into
target study with identifier
``6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12``.

As in the case of splitting, this is done by updating the following
DICOM tags: ``StudyInstanceUID (0x0020, 0x000d)``, ``SeriesInstanceUID
(0x0020, 0x000e)``, and ``SOPInstanceUID (0x0008,
0x0018)``. Furthermore, all the DICOM tags that are part of the
"Patient Module Attributes" and the "General Study Module Attributes"
(as specified by the DICOM 2011 standard in Tables C.7-1 and C.7-3),
are modified to match the target study. Here are the
arguments of this ``/studies/{study}/merge`` URI:

* ``Resources`` gives the list of source studies or source series
  that are to be merged into the target study.
* ``KeepSource`` (Boolean value), if set to ``true``, instructs
  Orthanc to keep the source studies and series.  By default, the
  original resources are deleted from Orthanc.
