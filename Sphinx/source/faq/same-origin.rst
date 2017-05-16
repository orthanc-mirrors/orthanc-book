.. _same-origin:

Same-origin policy in JavaScript
================================

Orthanc is designed as a lightweight service for medical imaging,
where the word *service* must be understood in the sense of
`service-oriented architectures
<https://en.wikipedia.org/wiki/Service-oriented_architecture>`__.
External software can interact with the Orthanc service through the
:ref:`rest`, so as to build higher-level applications that make use of
DICOM.

Such an external software can be JavaScript code executed by a Web
browser and making AJAX requests to Orthanc (possibly using the
widespread jQuery framework). However, such AJAX requests are subject
to the `same-origin policy
<https://en.wikipedia.org/wiki/Same-origin_policy>`__ that will
prevent the JavaScript code to get in touch with the REST API of
Orthanc, as the origin of the page serving the JavaScript code will
not be the Orthanc server itself. This problem does not arise with the
administrative interface :ref:`Orthanc Explorer <orthanc-explorer>`,
as its JavaScript code is directly served by Orthanc.

We have deliberately decided not to include any mechanism to bypass
the same-origin policy (`CORS
<https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`__) into
the core of Orthanc. By this choice, we hope to force clean Web
designs, which is especially important for medical applications.  To
circumvent the same-origin policy, you have three choices:

1. Branch the REST API of Orthanc as a **reverse proxy** into the Web
   server that serves the JavaScript code (cf. the instructions for
   :ref:`Apache <apache>`, :ref:`nginx <nginx>` and :ref:`iis <IIS>`). 
   This is the best solution for production.
2. Use the official :ref:`ServeFolders plugin <serve-folders>` that
   can be used to serve JavaScript code directly by the **embedded Web
   server of Orthanc** (i.e. next to its REST API). This is the best
   solution for development or debugging.
3. Enable **CORS on the top of Orthanc** with your Web server (cf. the
   instructions for :ref:`nginx <nginx-cors>`). This is the most hacky
   solution.
