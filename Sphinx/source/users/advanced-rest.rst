.. _rest-advanced:

Advanced features of the REST API
=================================

.. contents::
   :depth: 3

This section of the Orthanc Book is a complement to the description of
the :ref:`REST API of Orthanc <rest>`. It explains some advanced uses
of the API.


.. _jobs:

Jobs
----

Since Orthanc 1.4.0, a jobs engine is embedded within Orthanc. Jobs
are high-level tasks to be processed by Orthanc. Jobs are first added
to a queue of pending tasks, and Orthanc will simultaneously execute a
fixed number of jobs (check out :ref:`configuration option
<configuration>` ``ConcurrentJobs``). Once the jobs have been
processed, they are tagged as successful or failed, and kept in a
history (the size of this history is controlled by the
``JobsHistorySize`` option).

By default, Orthanc saves the jobs into its database (check out the
``SaveJobs`` option). If Orthanc is stopped then relaunched, the jobs
whose processing was not finished are automatically put into the queue
of pending tasks. The command-line option ``--no-jobs`` can also be
used to prevent the loading of jobs from the database upon the launch
of Orthanc.

Note that the queue of pending jobs has a maximum size (check out the
``LimitJobs`` option). When this limit is reached, the addition of new
jobs is blocked until some job finishes.



Synchronous vs. asynchronous calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some calls to the REST API of Orthanc need time to be executed, and
thus result in adding a job to the processing queue. This notably
includes the following URIs:

* :ref:`Modifying and anonymizing <anonymization>` DICOM instances.
* Creating ZIP or media archives.
* C-Move SCU (``/queries/.../retrieve``).
* C-Store SCU (``/modalities/.../store``).
* Sending to an Orthanc peer (``/peers/.../store``).
* :ref:`Split/merge <split-merge>`.
* Sending images using the :ref:`transfers accelerator <transfers>` plugin.

Such REST API calls can be configured to be executed in a synchronous
or an asynchronous mode:

* **Synchronous calls** wait for the end of the execution of their
  associated job. This is in general the default behavior.
* **Asynchronous calls** end immediately and return a handle to their
  associated job. It is up to the caller to monitor the execution by
  calling the jobs API (e.g. to know whether the job has finished its
  execution).

The choice between synchronous and asynchronous modes is done by
setting the ``Synchronous`` field (or indifferently the
``Asynchronous`` field) in the POST body of the call to the REST
API. Note that the :ref:`transfers accelerator <transfers>` only runs
in asynchronous mode.

An integer number (possibly negative) can be specified in the
``Priority`` field of the POST body. Jobs with higher priority will be
executed first. By default, the priority is set to zero.

Despite being more complex to handle, the asynchronous mode is highly
recommended for jobs whose execution time can last over a dozen of
seconds (typically, the creation of an archive or a network transfer).
Indeed, synchronous calls can be affected by timeouts in the HTTP
protocol if they last too long.


.. _jobs-monitoring:

Monitoring jobs
^^^^^^^^^^^^^^^

.. highlight:: bash

The list of all jobs can be retrieved as follows::

  $ curl http://localhost:8042/jobs
  [ "e0d12aac-47eb-454f-bb7f-9857931e2904" ]

Full details about each job can be retrieved::

  $ curl http://localhost:8042/jobs/e0d12aac-47eb-454f-bb7f-9857931e2904
  {
    "CompletionTime" : "20190306T095223.753851",
    "Content" : {
      "Description" : "REST API",
      "InstancesCount" : 1,
      "UncompressedSizeMB" : 0
    },
    "CreationTime" : "20190306T095223.750666",
    "EffectiveRuntime" : 0.001,
    "ErrorCode" : 0,
    "ErrorDescription" : "Success",
    "ID" : "e0d12aac-47eb-454f-bb7f-9857931e2904",
    "Priority" : 0,
    "Progress" : 100,
    "State" : "Success",
    "Timestamp" : "20190306T095408.556082",
    "Type" : "Archive"
  }

Note that the ``/jobs?expand`` URI will retrieve this information in
one single REST query. The ``Content`` field contains the parameters
of the job, and is very specific to the ``Type`` of job.

The ``State`` field can be:

* ``Pending``: The job is waiting to be executed.
* ``Running``: The job is being executed. The ``Progress`` field will
  be continuously updated to reflect the progression of the execution.
* ``Success``: The job has finished with success.
* ``Failure``: The job has finished with failure. Check out the
  ``ErrorCode`` and ``ErrorDescription`` fields for more information.
* ``Paused``: The job has been paused.
* ``Retry``: The job has failed internally, and has been scheduled for
  re-submission after a delay. As of Orthanc 1.6.0, this feature is not
  used by any type of job.

In order to wait for the end of an asynchronous call, the caller will
typically have to poll the ``/jobs/...` URI (i.e. make periodic
calls), waiting for the ``State`` field to become ``Success`` or
``Failure``.


.. _jobs-controlling:

Interacting with jobs
^^^^^^^^^^^^^^^^^^^^^

Given the ID of some job, one can:

* Cancel the job by POST-ing to ``/jobs/.../cancel``.
* Pause the job by POST-ing to ``/jobs/.../pause``.
* Resume a job in ``Paused`` state by POST-ing to ``/jobs/.../resume``.
* Retry a job in ``Failed`` state by POST-ing to ``/jobs/.../resubmit``.

The related state machine is depicted in the `implementation notes
<https://hg.orthanc-server.com/orthanc/raw-file/tip/Resources/ImplementationNotes/JobsEngineStates.pdf>`__.
  



.. _pdf:

Attaching PDF file as DICOM series
----------------------------------

Among many different types of data, DICOM files can be used to store
PDF files. The ``/tools/create-dicom`` URI can be used to upload a PDF
file to Orthanc. The following scripts perform such a *DICOM-ization*;
They convert the ``HelloWorld2.pdf`` file to base64, then perform a
``POST`` request with JSON data containing the converted payload.

Using bash:

.. code-block:: bash

    # create the json data, with the BASE64 data embedded in it
    (echo -n '{"Tags" : {"PatientName" : "Benjamino", "Modality" : "CT"},"Content" : "data:application/pdf;base64,'; base64 HelloWorld2.pdf; echo '"}') > /tmp/foo

    # upload it to Orthanc
    cat /tmp/foo | curl -H "Content-Type: application/json" -d @- http://localhost:8042/tools/create-dicom


Using powershell:

.. code-block:: perl

    # create the BASE64 string data
    $fileInBase64 = $([Convert]::ToBase64String((gc -Path "HelloWorld2.pdf" -Encoding Byte)))

    # create the json data
    $params = @{Tags = @{PatientName = "Benjamino";Modality = "CT"};Content= "data:application/pdf;base64,$fileInBase64"}

    # disabling the progress bar makes the Invoke-RestMethod call MUCH faster
    $ProgressPreference = 'SilentlyContinue'

    # upload it to Orthanc
    $reply = Invoke-RestMethod http://localhost:8042/tools/create-dicom -Method POST -Body ($params|ConvertTo-Json) -ContentType 'application/json'

    # display the result
    Write-Host "The instance can be retrieved in PDF at http://localhost:8042$($reply.Path)/pdf"

Please note that the ``/tools/create-dicom`` API call will return the
Orthanc instance ID of the newly created DICOM resource.

You can use the ``/instances/.../pdf`` URI to retrieve an embedded PDF
file.



.. _prometheus:

Instrumentation with Prometheus
-------------------------------

.. highlight:: text

Orthanc publishes its metrics according to the `text-based format of
Prometheus
<https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format>`__
(check also the `OpenMetrics project <https://openmetrics.io/>`__), onto
the ``/tools/metrics-prometheus`` URI of the REST API. For instance::

  $ curl http://localhost:8042/tools/metrics-prometheus
  orthanc_count_instances 1 1551868380543
  orthanc_count_patients 1 1551868380543
  orthanc_count_series 1 1551868380543
  orthanc_count_studies 1 1551868380543
  orthanc_disk_size_mb 0.0135002136 1551868380543
  orthanc_jobs_completed 1 1551868380543
  orthanc_jobs_failed 0 1551868380543
  orthanc_jobs_pending 0 1551868380543
  orthanc_jobs_running 0 1551868380543
  orthanc_jobs_success 1 1551868380543
  orthanc_rest_api_active_requests 1 1551868380543
  orthanc_rest_api_duration_ms 0 1551868094265
  orthanc_storage_create_duration_ms 0 1551865919315
  orthanc_storage_read_duration_ms 0 1551865943752
  orthanc_store_dicom_duration_ms 5 1551865919319
  orthanc_uncompressed_size_mb 0.0135002136 1551868380543


.. highlight:: bash

Note that the collection of metrics can be statically disabled by
setting the :ref:`global configuration option <configuration>`
``MetricsEnabled`` to ``false``, or dynamically disabled by PUT-ing
``0`` on ``/tools/metrics``::

  $ curl http://localhost:8042/tools/metrics
  1
  $ curl http://localhost:8042/tools/metrics -X PUT -d '0'
  $ curl http://localhost:8042/tools/metrics
  0


.. highlight:: yaml

Here is a sample configuration for Prometheus (in the `YAML format
<https://en.wikipedia.org/wiki/YAML>`__)::

  scrape_configs:
    - job_name: 'orthanc'
      scrape_interval: 10s
      metrics_path: /tools/metrics-prometheus
      basic_auth:
        username: orthanc
        password: orthanc
      static_configs:
        - targets: ['192.168.0.2:8042']

.. highlight:: bash

Obviously, make sure to adapt this sample with your actual IP
address. Thanks to Docker, you can easily start a Prometheus server by
writing this configuration to, say, ``/tmp/prometheus.yml``, then
type::
          
  $ sudo run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml --rm prom/prometheus:v2.7.0
