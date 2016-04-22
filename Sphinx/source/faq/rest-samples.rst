.. highlight:: bash
.. _rest-samples:

Finding samples for the REST API
================================

* This "Orthanc Book" proposes a :ref:`number of samples showing how
  to use the REST API <rest>` of Orthanc.
* Many working examples written in Python are `available in the source
  distribution
  <https://bitbucket.org/sjodogne/orthanc/src/default/Resources/Samples/Python/>`__.
* If you cannot find an example for some feature in this manual or in
  the Python examples, please check the `publicly available
  integration tests
  <https://bitbucket.org/sjodogne/orthanc-tests/src/default/Tests/Tests.py>`__
  that span most of the REST API.
* Samples for the deprecated APIs are available below.



Deprecated APIs
---------------

You will find below code snippets for APIs that have been deprecated
over the releases of Orthanc. They are reproduced here for backward
compatibility and should not be used in new developments.


.. _deprecated-find-scu:

C-Find SCU (Deprecated)
^^^^^^^^^^^^^^^^^^^^^^^

1. Retrieve the PatientID::

     $ curl http://localhost:8042/modalities/pacs/find-patient -X POST -d '{"PatientName":"JOD*","PatientSex":"M"}'

2. Retrieve the studies of this patient (using the "PatientID" returned from Step 1)::

     $ curl http://localhost:8042/modalities/pacs/find-study -X POST -d '{"PatientID":"0555643F"}'

3. Retrieve the series of one study (using the "PatientID" from Step 1, and the "StudyInstanceUID" from Step 2)::

     $ curl http://localhost:8042/modalities/pacs/find-series -X POST -d '{"PatientID":"0555643F","StudyInstanceUID":"1.2.840.113704.1.111.276

You will have to define the modality "pacs" in the :ref:`configuration file
<configuration>` of Orthanc (under the section ``DicomModalities``).

*Note:* This API has been superseded by the ``/modalities/.../query``
URI. Please check the ``test_rest_query_retrieve`` `integration test
<https://bitbucket.org/sjodogne/orthanc-tests/src/default/Tests/Tests.py>`__.


Using Orthanc to Ease WADO Querying (Deprecated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of Orthanc 0.6.1, it will be possible to use Orthanc to easily
gather the three identifiers that are required to run a `WADO query
<ftp://medical.nema.org/medical/dicom/2006/06_18pu.pdf>`__ against a
remote modality (without storing the files inside Orthanc). These
identifiers are:

* StudyInstanceUID (0020,000d),
* SeriesInstanceUID (0020,000e),
* ObjectUID, that exactly corresponds to the SOPInstanceUID tag
  (0008,0018) (cf. the `WADO specification
  <ftp://medical.nema.org/medical/dicom/2006/06_18pu.pdf>`__, Section
  8.1.4).

The trick consists in using the experimental C-Find SCU API, going down to the instance level::

    $ curl http://localhost:8042/modalities/pacs/find-patient -X POST -d '{"PatientName":"JOD*","PatientSex":"M"}'
    $ curl http://localhost:8042/modalities/pacs/find-study -X POST -d '{"PatientID":"0555643F"}'
    $ curl http://localhost:8042/modalities/pacs/find-series -X POST -d '{"PatientID":"0555643F","StudyInstanceUID":"1.2.840.113704.1.111.2768.1239195678.57"}' 
    $ curl http://localhost:8042/modalities/pacs/find-instance -X POST -d '{"PatientID":"0555643F","StudyInstanceUID":"1.2.840.113704.1.111.2768.1239195678.57","SeriesInstanceUID":"1.3.46.670589.28.2.7.2200939417.2.13493.0.1239199523"}'

The first three steps are described in this :ref:`other FAQ entry
<deprecated-find-scu>`. The fourth step retrieves the list of the
instances of the series. The latter query was not possible until
Orthanc 0.6.1. As a result of this sequence of four commands, the
StudyInstanceUID, SeriesInstanceUID and SOPInstanceUID are readily
available for each instance of the series.

*Note:* This API has been superseded by the ``/modalities/.../query``
URI. Please check the ``test_rest_query_retrieve`` `integration test
<https://bitbucket.org/sjodogne/orthanc-tests/src/default/Tests/Tests.py>`__.
