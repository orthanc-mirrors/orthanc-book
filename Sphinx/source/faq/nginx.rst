.. _nginx:

How can I run Orthanc behind nginx?
===================================

Similarly to :ref:`Apache <apache>`, Orthanc can run behind `nginx
<https://en.wikipedia.org/wiki/Nginx>`__ through reverse
proxying. Here is the configuration snippet for nginx::

    server {
       listen  80  default_server;
       ...
       location  /orthanc/  {
          proxy_pass http://127.0.0.1:8042;
          proxy_set_header HOST $host;
          proxy_set_header X-Real-IP $remote_addr;
          rewrite /orthanc(.*) $1 break;
       }
       ...
    }

*Note:* Thanks to Qaler for `submitting this information
<https://groups.google.com/d/msg/orthanc-users/oTMCM6kElfw/uj0r062mptoJ>`__.

You might also wish to adapt the ``client_max_body_size``
`configuration option of nginx
<http://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size>`__
to allow the uploading of DICOM files larger than the default 1MB if
using the :ref:`REST API <sending-dicom-images>` of Orthanc.


.. _nginx-cors:

Enabling CORS
-------------

Orthanc does not feature built-in support for `cross-origin resource
sharing (CORS)
<https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_.  It
is however possible to enable it with a nginx reverse proxy. Here is a
sample configuration for nginx::

    server {
       listen  80  default_server;
       ...
       location  /orthanc/  {
          proxy_pass http://127.0.0.1:8042;
          proxy_set_header HOST $host;
          proxy_set_header X-Real-IP $remote_addr;
          rewrite /orthanc(.*) $1 break;
          add_header 'Access-Control-Allow-Credentials' 'true';
          add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
          add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
          add_header 'Access-Control-Allow-Origin' '*';
       }
       ...
    }

*Note:* Thanks to Fernando for `submitting this information
<https://groups.google.com/d/msg/orthanc-users/LH-ej_fB-dw/CmWP4jM3BgAJ>`__.

