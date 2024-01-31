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
are high-level tasks to be processed by Orthanc. Jobs can be started
synchronously or asynchronously (see the section below).  All Jobs,
no matter how they were started, are first added
to a queue of pending tasks, and Orthanc will simultaneously execute a
fixed number of jobs (check out :ref:`configuration option
<configuration>` ``ConcurrentJobs``). Once the jobs have been
processed, they are tagged as successful or failed, and kept in a
history (the size of this history is controlled by the
``JobsHistorySize`` option).

By default, Orthanc saves the jobs into its database (check out the
``SaveJobs`` option).  Jobs are saved within 100ms after their creation,
and then, the whole jobs list, with their updated status, is saved every 10 seconds and when
Orthanc stops. If Orthanc is stopped then relaunched, the jobs whose 
processing was not finished are automatically put into the queue of 
pending tasks or resumed if they were being processed when Orthanc stopped, 
regardless of whether they were started synchronously or asynchronously 
(see the section below). The command-line option ``--no-jobs`` can also be used to 
prevent the loading of jobs from the database upon the launch of 
Orthanc.

Note that the queue of pending jobs has no size limit.

.. _jobs-synchronicity:

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
seconds (typically, the creation of an archive if
``SynchronousZipStream`` :ref:`configuration option <configuration>`
is set to ``false``, or a network transfer).  Indeed, synchronous
calls can be affected by timeouts in the HTTP protocol if they last
too long.

When generating archives asynchronously, you should take care of 
the ``MediaArchiveSize`` configuration that defines the maximum
number of ZIP/media archives that are maintained by Orthanc, as a 
response to the asynchronous creation of archive. As of Orthanc
1.12.3, this value is ``1`` by default.

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
  re-submission after a delay. As of Orthanc 1.12.3, this feature is not
  used by any type of job.

In order to wait for the end of an asynchronous call, the caller will
typically have to poll the ``/jobs/...`` URI (i.e. make periodic
calls), waiting for the ``State`` field to become ``Success`` or
``Failure``.

Note that the `integration tests of Orthanc
<https://orthanc.uclouvain.be/hg/orthanc-tests/file/Orthanc-1.12.3/Tests/Toolbox.py>`__
give an example about how to monitor a job in Python using the REST
API (cf. function ``MonitorJob()``).


.. _jobs-priority:

Jobs priority
^^^^^^^^^^^^^

When executing jobs, Orthanc will pick the jobs with the highest ``Priority`` 
from the pending job list. An integer value is a valid ``Priority``.  You may 
also use negative number to lower the priority below the default one (``0``).

Pending jobs are not ordered in the API response but they are picked up in the right order.


.. _jobs-controlling:

Interacting with jobs
^^^^^^^^^^^^^^^^^^^^^

Given the ID of some job, one can:

* Cancel the job by POST-ing to ``/jobs/.../cancel``.
* Pause the job by POST-ing to ``/jobs/.../pause``.
* Resume a job in ``Paused`` state by POST-ing to ``/jobs/.../resume``.
* Retry a job in ``Failed`` state by POST-ing to ``/jobs/.../resubmit``.

The related state machine is depicted in the `implementation notes
<https://orthanc.uclouvain.be/hg/orthanc/raw-file/default/OrthancServer/Resources/ImplementationNotes/JobsEngineStates.pdf>`__.


Example: Asynchronous generation of an archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Sucessful jobs are associated with a set of so-called "outputs" that
can be attached to the job.
               
Here is a sample bash session to ask Orthanc to generate a ZIP
archive, then to download it locally::

  $ curl http://localhost:8042/studies/27f7126f-4f66fb14-03f4081b-f9341db2-53925988/archive -d '{"Asynchronous":true}'
  {
    "ID" : "82cc02d1-03fe-41f9-be46-a308d16ea94a",
    "Path" : "/jobs/82cc02d1-03fe-41f9-be46-a308d16ea94a"
  }
  $ curl http://localhost:8042/jobs/82cc02d1-03fe-41f9-be46-a308d16ea94a
  {
    "CompletionTime" : "20200817T144700.401777",
    "Content" : {
      "Description" : "REST API",
      "InstancesCount" : 232,
      "UncompressedSizeMB" : 64
    },
    "CreationTime" : "20200817T144658.011824",
    "EffectiveRuntime" : 2.3879999999999999,
    "ErrorCode" : 0,
    "ErrorDescription" : "Success",
    "ID" : "82cc02d1-03fe-41f9-be46-a308d16ea94a",
    "Priority" : 0,
    "Progress" : 100,
    "State" : "Success",
    "Timestamp" : "20200817T144705.770825",
    "Type" : "Archive"
  }
  $ curl http://localhost:8042/jobs/82cc02d1-03fe-41f9-be46-a308d16ea94a/archive > a.zip

Note how we retrieve the content of the archive by accessing the
``archive`` output of the job (check out the virtual method
``IJob::GetOutput()`` from the `source code
<https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.3/OrthancServer/Sources/ServerJobs/ArchiveJob.cpp>`__
of Orthanc).

Here is the corresponding sequence of commands to generate a DICOMDIR
media::

  $ curl http://localhost:8042/studies/27f7126f-4f66fb14-03f4081b-f9341db2-53925988/media -d '{"Asynchronous":true}'
  $ curl http://localhost:8042/jobs/6332be8a-0052-44fb-8cc2-ac959aeccad9/archive > a.zip

As of Orthanc 1.12.3, only the creation of a ZIP or a DICOMDIR archive
produces such "outputs".

  
.. _pdf:

Attaching PDF file as DICOM series
----------------------------------

Among many different types of data, DICOM files can be used to store
PDF files. The ``/tools/create-dicom`` URI can be used to upload a PDF
file to Orthanc. The following scripts perform such a *DICOM-ization*;
They convert the ``HelloWorld2.pdf`` file to base64, then perform a
``POST`` request with JSON data containing the converted payload.

Importantly, the ``Parent`` field of the ``POST`` body can be set to
the :ref:`Orthanc identifier of some study <orthanc-ids>` in order to
attach the newly-created PDF series to the given parent study.

Using bash:

.. code-block:: bash

    # create the json data, with the BASE64 data embedded in it
    (echo -n '{"Parent": "b6e8436b-c5835b7b-cecc9576-0483e165-ab5c710b", "Tags" : {"Modality" : "CT"}, "Content" : "data:application/pdf;base64,'; base64 HelloWorld2.pdf; echo '"}') > /tmp/foo

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

And here's another sample  `using python
<https://github.com/orthanc-server/orthanc-setup-samples/tree/master/python-samples/attach-pdf-to-study.py>`__.

Please note that the ``/tools/create-dicom`` API call will return the
Orthanc instance ID of the newly created DICOM resource.

You can use the ``/instances/.../pdf`` URI to retrieve an embedded PDF
file.


.. _private-tags:

Creating DICOM instance with private tags
-----------------------------------------

.. highlight:: json

The ``/tools/create-dicom`` URI can be used to create DICOM instances
containing private tags. Those private tags must first be defined in
the ``Dictionary`` configuration option of Orthanc. Importantly, the
``xxxx,0010`` tag must be defined to register the private creator,
where ``xxxx`` is the private group of interest. Here is a sample::

  {
    "Dictionary" : {
      "0405,0010" : [ "LO", "PrivateCreatorForMyCompany", 1, 1, "My Company" ],   // reserve 0405,10xx for "My Company"
      "0405,1001" : [ "ST", "MyPrivateXMLTag", 1, 1, "My Company" ]               // all tags from "My Company" must start with 0405,10xx 
    }
  }

Once Orthanc is started using this configuration file, it is possible
to create a DICOM instance using the following POST body on
``/tools/create-dicom``::

  {
    "PrivateCreator" : "My Company",                             // private creator here
    "Tags" :
    {
      "PatientName" : "Love^Sarah",
      "PatientID" : "7",
      "PrivateCreatorForMyCompany" : "My Company",               // and here !
      "MyPrivateXMLTag" : "<xml><test>Testing</test></xml>"
    }
  }

Which then gives this in Orthanc UI:

.. image:: ../images/PrivateTagsInCreateDicom.png
           :align: center
           :width: 400px

Rob Oakes provides more a `detailed explanation about how to use
private tags with Orthanc
<https://oak-tree.tech/blog/soandor-orthanc-private-headers>`__ on
Oak-Tree's homepage.

  
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
  orthanc_count_instances 21741 1680083638028
  orthanc_count_patients 86 1680083638028
  orthanc_count_series 239 1680083638028
  orthanc_count_studies 93 1680083638028
  orthanc_dicom_cache_count 2 1680083630571
  orthanc_dicom_cache_size 0.00191688538 1680083630571
  orthanc_disk_size_mb 16855.9629 1680083638028
  orthanc_jobs_completed 10 1680083638028
  orthanc_jobs_failed 0 1680083638028
  orthanc_jobs_pending 0 1680083638028
  orthanc_jobs_running 0 1680083638028
  orthanc_jobs_success 10 1680083638028
  orthanc_last_change 81062 1680083638028
  orthanc_rest_api_active_requests 1 1680083638027
  orthanc_rest_api_duration_ms 77 1680083630549
  orthanc_storage_create_duration_ms 2 1680083630565
  orthanc_storage_read_duration_ms 2 1680083630557
  orthanc_store_dicom_duration_ms 7 1680083630570
  orthanc_uncompressed_size_mb 16855.9629 1680083638028
  orthanc_up_time_s 64 1680083638028

The metrics only appear in the response once they have been recorded at least once.  Furthermore, some plugins
may add their own metrics dynamically.

+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| Metrics                                                | Meaning                                                                     | Origin                                                         |
+========================================================+=============================================================================+================================================================+
| ``orthanc_up_time_s``                                  | The time [s] spent since Orthanc started                                    | Orthanc                                                        |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_last_change``                                | The current id of the last `change` event                                   | Orthanc                                                        |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_memory_trimming_duration_ms``                | The max duration [ms] over the last 10 seconds of the last memory           | Orthanc                                                        |
|                                                        | trimming duration                                                           |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_store_dicom_duration_ms``                    | The max duration [ms] over the last 10 seconds needed to store a            | Orthanc                                                        |
|                                                        | DICOM file (received from HTTP, DICOM protocol or from a plugin)            |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_count_instances``                            | The number of instances stored in DB                                        | Orthanc DB                                                     |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_count_series``                               | The number of series stored in DB                                           | Orthanc DB                                                     |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_count_studies``                              | The number of studies stored in DB                                          | Orthanc DB                                                     |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_count_patients``                             | The number of patients stored in DB                                         | Orthanc DB                                                     |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_dicom_cache_count``                          | The number of DICOM files currently stored in the DICOM cache               | Orthanc DICOM cache                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_dicom_cache_size_mb``                        | The size [MB] of all DICOM files currently stored in the DICOM cache        | Orthanc DICOM cache                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_find_scp_duration_ms``                       | The max duration [ms] over the last 10 seconds of a C-Find SCP execution    | Orthanc DICOM protocol server                                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_get_scp_duration_ms``                        | The max duration [ms] over the last 10 seconds of a C-Get SCP execution     | Orthanc DICOM protocol server                                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_move_scp_duration_ms``                       | The max duration [ms] over the last 10 seconds of a C-Move SCP execution    | Orthanc DICOM protocol server                                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_rest_api_active_requests``                   | The maximum number of concurrent HTTP requests being handled by the         | Orthanc HTTP server                                            |
|                                                        | HTTP server over the last 10 seconds.                                       |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_rest_api_duration_ms``                       | The max duration [ms] over the last 10 seconds required to handle           | Orthanc HTTP server                                            |
|                                                        | an HTTP request                                                             |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_jobs_pending``                               | The current number of jobs whose execution is currently pending             | Orthanc Jobs engine                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_jobs_running``                               | The current number of jobs currently being executed                         | Orthanc Jobs engine                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_jobs_completed``                             | The current number of jobs completed (failed or success)                    | Orthanc Jobs engine                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_jobs_success``                               | The current number of jobs that have succeeded                              | Orthanc Jobs engine                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_jobs_failed``                                | The current number of jobs that have failed                                 | Orthanc Jobs engine                                            |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_disk_size_mb``                               | The size [MB] of all DICOM files currently stored in Orthanc                | Orthanc Storage                                                |
|                                                        | (possibly compressed size)                                                  |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_uncompressed_size_mb``                       | The size [MB] of all DICOM files currently stored in Orthanc                | Orthanc Storage                                                |
|                                                        | (uncompressed size)                                                         |                                                                |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_cache_count``                        | The number of files currently stored in the Storage cache                   | Orthanc Storage cache                                          |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_cache_size_mb``                      | The size [MB] of all files currently stored in the Storage cache            | Orthanc Storage cache                                          |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_create_duration_ms``                 | The max duration [ms] over the last 10 seconds to save a file to disk       | Orthanc Storage (default file system storage)                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_read_duration_ms``                   | The max duration [ms] over the last 10 seconds to read a file from disk     | Orthanc Storage (default file system storage)                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_remove_duration_ms``                 | The max duration [ms] over the last 10 seconds to delete a file from disk   | Orthanc Storage (default file system storage)                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_read_bytes``                         | The total number of bytes read from disk since Orthanc started              | Orthanc Storage (default file system storage)                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+
| ``orthanc_storage_written_bytes``                      | The total number of bytes written to disk since Orthanc started             | Orthanc Storage (default file system storage)                  |
+--------------------------------------------------------+-----------------------------------------------------------------------------+----------------------------------------------------------------+



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
