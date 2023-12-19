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
the resulting anonymized DICOM file (without storing the anonymized
DICOM instance into Orthanc). Anonymization consists in erasing all
the tags that are specified in `Table E.1-1 from PS 3.15
<http://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_E.html#table_E.1-1>`__
of the DICOM standard 2008, 2017c, 2021b, 2023b (default). Example::

    $ curl http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/anonymize -X POST -d '{}' > Anonymized.dcm

It is possible to control how anonymization is achieved by specifying
a JSON body::

    $ curl http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/anonymize -X POST \
      --data '{
                "Replace": {
                  "PatientName": "Hello",
                  "0010-1001": "World"
                },
                "Keep": [
                  "StudyDescription", 
                  "SeriesDescription"
                ],
                "KeepPrivateTags": true, 
                "DicomVersion" : "2017c"
              }' > Anonymized.dcm

**Explanations:**

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
* ``DicomVersion`` specifies which version of the DICOM standard shall
  be used for anonymization. Allowed values are ``2008``, ``2017c``, 
  ``2021b`` (new in Orthanc 1.9.4) or ``2023b`` (new in Orthanc 1.12.1). 
  This parameter has been introduced in Orthanc 1.3.0. In earlier version, 
  the ``2008`` standard was used. If the parameter is absent, the highest 
  version that is supported by Orthanc is used.
* ``Remove`` can also be used to provide a list of tags to be manually
  deleted.

**Important:** Starting with Orthanc 1.9.4, the ``Replace``, ``Keep``
and ``Remove`` fields can also specify sequences, using the same
syntax as the ``dcmodify`` command-line tool (wildcards are supported
as well). Earlier versions were limited to top-level tags in the DICOM
dataset. Check out the integration test ``test_modify_subsequences``
for `examples
<https://orthanc.uclouvain.be/hg/orthanc-tests/file/default/Tests/Tests.py>`__.

**Implementation:** Internally, the setup of the anonymization
profiles can be found in the methods ``SetupAnonymizationXXX()`` of
the class ``Orthanc::DicomModification`` (cf. `source code
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.2/OrthancFramework/Sources/DicomParsing/DicomModification.cpp>`__).


Modification of a Single Instance
---------------------------------

Orthanc allows to modify a set of specified tags in a single DICOM
instance and to download the resulting modified DICOM file (without
storing the modified DICOM instance into Orthanc). Example::

    $ curl -X POST http://localhost:8042/instances/6e67da51-d119d6ae-c5667437-87b9a8a5-0f07c49f/modify \
      --data '{
                "Replace": {
                  "PatientName":"hello",
                  "PatientID":"world"
                },
                "Remove":[
                  "InstitutionName"
                ],
                "RemovePrivateTags": true, 
                "Force": true,
                "Transcode": "1.2.840.10008.1.2.4.70"
              }' > Modified.dcm

**Remarks:**

* The ``Remove`` array specifies the list of the tags to remove.
* The ``Replace`` associative array specifies the substitions to be applied (cf. anonymization).
* If ``RemovePrivateTags`` is set to ``true``, the private tags
  (i.e. manufacturer-specific tags) are removed.
* The ``Transcode`` option allows you to define the TransferSyntax
  of the modified file.
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

* To add a Private DICOM tag, you should use this syntax (provided that you have defined an entry ``"7001,0001" : [ "CS", "MyPrivateTag", 1, 1, "MyPrivateCreator"]`` in the ``Dictionary`` configuration)::

    {
      "Replace" : {
        "MyPrivateTag" : "Hello"
      },
      "PrivateCreator" : "MyPrivateCreator"
    }


**Important:** Similarly to anonymization, starting with Orthanc
1.9.4, the ``Replace``, ``Keep`` and ``Remove`` fields can also
specify sequences, using the same syntax as the ``dcmodify``
command-line tool (wildcards are supported as well). Earlier versions
were limited to top-level tags in the DICOM dataset. Check out the
integration test ``test_modify_subsequences`` for `examples
<https://orthanc.uclouvain.be/hg/orthanc-tests/file/default/Tests/Tests.py>`__.


.. _study-modification:

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

Up to version 1.11.2, Orthanc implemented safety checks to
preserve the :ref:`DICOM model of the real world <model-world>`. These
checks prevented the modification of some tags that are known to belong
to a level in the patient/study/series/instance hierarchy that is
higher than the level that corresponds to the REST API call. For
instance, the tag ``PatientID`` could not be modified if using the
``/studies/{id}/modify`` route (in the latter case, the
``/patients/{id}/modify`` route had to be used, cf. next section).
These sanity checks have been loosened in more recent versions (starting from 1.11.3)
and users must be very careful to preserve the DICOM model when updating these tags (e.g.
if you modify the ``PatientID`` at study level, also make sure to modify all other Patient related
tags (``PatientName``, ``PatientBirthDate``, ...)).

Also note that you have to set the ``Force`` argument to ``true`` if modifying one
of the :ref:`DICOM identifiers tags <orthanc-ids>`
(i.e. ``PatientID``, ``StudyInstanceUID``, ``SeriesInstanceUID`` and
``SOPInstanceUID``).


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


.. _bulk-modification:

Bulk modification or anonymization
----------------------------------

Starting with Orthanc 1.9.4, it is possible to use the new routes
``/tools/bulk-modify`` and ``/tools/bulk-anonymize`` to respectively
modify or anonymize a set of multiple DICOM resources that are not
related (i.e. that don't share any parent DICOM resource). A typical
use case is to modify/anonymize a list of DICOM instances that don't
belong to the same parent patient/study/series.

.. highlight:: bash

These two routes accept the same arguments as described above, but
must also be provided with an additional argument ``Resources`` that
lists the :ref:`Orthanc identifiers <orthanc-ids>` of the resources of
interest (that may indifferently correspond to patients, studies,
series or instances). Here are two sample calls::

  $ curl http://localhost:8042/tools/bulk-modify -d '{"Replace":{"SeriesDescription":"HELLO"},"Resources":["b6da0b16-a25ae9e7-1a80fc33-20df01a9-a6f7a1b0","d6634d97-24379e4a-1e68d3af-e6d0451f-e7bcd3d1"]}'
  $ curl http://localhost:8042/tools/bulk-anonymize -d '{"Resources":["b6da0b16-a25ae9e7-1a80fc33-20df01a9-a6f7a1b0","d6634d97-24379e4a-1e68d3af-e6d0451f-e7bcd3d1"]}'

.. highlight:: json

The output of the modification/anonymization lists all the resources
that have been altered by the call (including their parents). Here is
the output of the second sample above::

  {
    "Description" : "REST API",
    "FailedInstancesCount" : 0,
    "InstancesCount" : 2,
    "IsAnonymization" : true,
    "Resources" : [
      {
         "ID" : "04c04806-27b01a5a-08ea66cb-cb36c8b9-ebe62fe3",
         "Path" : "/instances/04c04806-27b01a5a-08ea66cb-cb36c8b9-ebe62fe3",
         "Type" : "Instance"
      },
      {
         "ID" : "4e37fce9-6b33b8ba-7bb378e1-abc7e2c4-fca4ade3",
         "Path" : "/instances/4e37fce9-6b33b8ba-7bb378e1-abc7e2c4-fca4ade3",
         "Type" : "Instance"
      },
      {
         "ID" : "6438ee62-b58a4788-517931b3-e10321eb-d1ab2613",
         "Path" : "/series/6438ee62-b58a4788-517931b3-e10321eb-d1ab2613",
         "Type" : "Series"
      },
      {
         "ID" : "660494fd-1ddd661b-4358d996-ba600e5a-066d94cc",
         "Path" : "/studies/660494fd-1ddd661b-4358d996-ba600e5a-066d94cc",
         "Type" : "Study"
      },
      {
         "ID" : "5faa0bf8-8a45520b-3a07e536-fc24f241-f59ae3e1",
         "Path" : "/patients/5faa0bf8-8a45520b-3a07e536-fc24f241-f59ae3e1",
         "Type" : "Patient"
      }
    ]
  }

  

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


.. _altering-dicom:

Altering the content of a single instance
-----------------------------------------

People often want to add/remove specific DICOM tags in an existing
DICOM instance, i.e. to ask ``/instances/{id}/modify`` to keep the
existing ``SOPInstanceUID (0008,0018)``. This operation is **strongly
discouraged**, as it **breaks medical traceability** by dropping the
history of the modifications that were applied to a DICOM
instance. Furthermore, the altered DICOM instance may be ignored by
further DICOM software. Indeed, the DICOM standard expects two DICOM
instances with the same SOP Instance UID to contain exactly the same
set of DICOM tags. Consequently, a DICOM software could perfectly
decide to only consider the original version of the DICOM instance.

Consequently, **Orthanc implements safeguards** in its REST API to
avoid such dangerous situations to occur. That being said, **if you
understand the risks**, it is possible to bypass those safeguards. The
trick is to pass both the ``Keep`` and ``Force`` arguments to the
``/instances/{id}/modify`` call. Here is a sample Python script that
implements this trick:

.. literalinclude:: anonymization_bypass.py
                    :language: python

This sample script downloads an altered version of a DICOM instance
from Orthanc (with the same ``SOPInstanceUID``), then uploads it again
to Orthanc. By default, Orthanc will ignore the upload of the altered
DICOM instance and will answer with the ``AlreadyStored`` message,
because ``SOPInstanceUID`` is already present in the Orthanc database.
To force the upload of the altered DICOM instance, one can either
(1) DELETE the instance before POST-ing it again, or (2) set the
``OverwriteInstances`` :ref:`configuration option <configuration>` of
Orthanc to ``true``. Both strategies are implemented in the sample
script.
