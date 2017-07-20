.. _apache:

How can I run Orthanc behind Apache?
====================================

It is possible to make Orthanc run behind Apache using the `reverse
proxy mechanism <https://en.wikipedia.org/wiki/Reverse_proxy>`_. To
map the REST API of an Orthanc server listening on the port 8000 on
the URI ``/Orthanc``, paste the following code in your
``/etc/apache2/httpd.conf``::

    LoadModule proxy_module /usr/lib/apache2/modules/mod_proxy.so
    LoadModule proxy_http_module /usr/lib/apache2/modules/mod_proxy_http.so
    ProxyRequests On
    ProxyPass /Orthanc/ http://localhost:8000/ retry=0

*Note*: These instructions are for Ubuntu 11.10. You most probably
have to adapt the absolute paths above to your distribution.

You might also wish to adapt the ``LimitRequestBody`` `configuration
option of Apache
<https://www.cyberciti.biz/faq/apache-limiting-upload-size/>`__ to
allow the uploading of large DICOM files if using the :ref:`REST API
<sending-dicom-images>` of Orthanc.

