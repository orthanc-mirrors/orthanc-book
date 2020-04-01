.. _worklist:

Does Orthanc support worklists?
===============================

Orthanc supports DICOM Modality Worklists (MWL) through its `plugin
SDK
<https://github.com/jodogne/OrthancContributed/tree/master/Plugins>`__.
In other words, Orthanc can act as a worklist server (C-Find SCP), but
an user-defined plugin must be provided to answer a list of worklists
given a MWL query.

The rationale for using plugins instead of providing a built-in MWL
mechanism, is that the way worklists are generated is very specific to
the clinical flows and to the manufacturer of your `RIS system
<https://en.wikipedia.org/wiki/Radiology_information_system>`__.
Indeed, depending on the situation, worklists can be generated either
from HL7 messages, from calls to a Web service (e.g. through FHIR), or
from a direct access to some RIS database. It is thus up to the
Orthanc user to provide the worklist generator that is best suited for
her use.

A :ref:`sample plugin <worklists-plugin>` is available in the source
distribution of Orthanc to serve the worklists stored in some folder
on the filesystem. This sample plugin mimics the behavior of the
``wlmscpfs`` command-line tool from the `DCMTK software
<https://support.dcmtk.org/docs/wlmscpfs.html>`__.

For more complex or integrated workflows where you must implement a
custom MWL plugin, please check the `documentation of the part of the
Orthanc plugin SDK
<https://sdk.orthanc-server.com/group__DicomCallbacks.html#ga23080c4e871b8428ede61d9841c10d76>`__
that is related to the management of worklists.
