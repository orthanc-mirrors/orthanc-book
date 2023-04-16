.. _multitenant-dicom:


Sample multitenant DICOM server
===============================

.. contents::

This **official** plugin by the `ICTEAM institute of UCLouvain
<https://uclouvain.be/en/research-institutes/icteam>`__ can be used to
turn Orthanc into a **multitenant DICOM** server using :ref:`labels
<labels>`. More precisely, the same Orthanc database can be accessed
from different DICOM servers, that each provides a different view
depending on the presence of labels. This plugin available is part of
the `official source distribution
<https://hg.orthanc-server.com/orthanc/file/default/OrthancServer/Plugins/Samples/MultitenantDicom>`__
of Orthanc, starting with Orthanc 1.12.0.

This plugin starts additional DICOM servers, in complement to the main
DICOM server of Orthanc that provides full access to the Orthanc
database. These additional DICOM servers support the C-Find, C-Move,
and C-Store commands, and share most of their configuration with the
main DICOM server of Orthanc. They are however distinguished from the
latter by using a **different AET** and a **different TCP
port**. Furthermore, each of those additional DICOM servers are
associated with a **set of labels** that restricts which DICOM
resources stored in Orthanc are accessible through this additional
DICOM server.

.. highlight:: json

Here is a sample :ref:`configuration file <configuration>` to use this
plugin::
  
  {
    "Plugins" : [ "." ],
    "DicomModalities" : {
      "sample" : [ "STORESCP", "127.0.0.1", 2000 ]
    },
    "MultitenantDicom" : {
      "Servers" : [
        {
          "AET" : "HELLO",
          "Port" : 4343,
          "Labels" : [ "hello" ],
          "LabelsConstraint" : "All",
          "LabelsStoreLevels" : [ "Patient", "Study", "Series", "Instance" ]
        }
      ]
    }
  }

This configuration will start an additional DICOM server with AET
``HELLO`` listening on the 4343 port. This DICOM server will work as
follows:

* DICOM C-Find and C-Move requests are restricted to the DICOM
  resources that are assigned with the ``hello`` label.

  * Note that the labels are checked by query/retrieve level: For
    instance, if ``QueryRetrieveLevel (0008, 0052)`` equals ``STUDY``,
    the plugin will only report the studies that are associated with
    the ``hello`` label.

  * The ``LabelsConstraint`` specifies the type of constraint on the
    labels. Its value can be ``All`` (default), ``Any``, or ``None``,
    which corresponds to the values accepted by the ``/tools/find``
    :ref:`route in the REST API <labels>` of Orthanc. Note that in the
    sample configuration above, because there is only one label in the
    ``Labels`` field, both ``Any`` and ``All`` have the same behavior.
  
* Any DICOM resource that is received through DICOM C-Store requests
  issued to this additional DICOM server, is automatically associated
  with all the labels provided in the ``Labels`` field. The
  configuration option ``LabelsStoreLevels`` can be used to restrict
  the levels to which the labels are applied (it defaults to the three
  study, series, and instances levels).
