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
are tasks to be done by Orthanc. Jobs are first added to a queue of
pending tasks, and Orthanc will simultaneously a fixed number of jobs
(check out :ref:`configuration option <configuration>`
``ConcurrentJobs``). Once the jobs have been processed, they are tagged
as successful or failed, and kept in a history (the size of this
history is controlled by the ``JobsHistorySize`` option).

Synchronous vs. asynchronous
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some calls to the REST API of Orthanc require time to be executed, and
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
  associated job. It is up to the caller to monitor the end of the
  execution by calling the jobs API.

The choice between synchronous and asynchronous modes is done by
setting the `Synchronous` field (or indifferently `Asynchronous`
field) in the POST body of the call to the REST API. Note that the
:ref:`transfers accelerator <transfers>` only run in the asynchronous
mode.

Even if it is more complex to handle, the asynchronous mode is highly
recommended for jobs whose execution time can last over a dozen of
seconds (typically, the creation of an archive or a network transfer).
Indeed, this prevents timeouts in the HTTP protocol.




.. _pdf:

PDF
---

TODO
