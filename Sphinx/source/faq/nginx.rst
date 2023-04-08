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


.. _nginx-demo:

Setting up a demo server using nginx
------------------------------------

It is often needed to setup a demo server through which users can
access DICOM images, but cannot modify the content of the Orthanc
database. The easiest solution to this scenario is to place an Orthanc
server behind a nginx proxy, with a :ref:`Lua script
<lua-filter-rest>` that only grants read-only access to external
users.

.. highlight:: json
               
To this end, first define two users ``admin`` and ``public`` in the
:ref:`configuration file <configuration>` of Orthanc::

  {
    "RemoteAccessAllowed" : true,
    "AuthenticationEnabled" : true,
    "RegisteredUsers" : {
      "admin" : "orthanc",
      "public" : "hello"
    },
    "LuaScripts" : [ "ReadOnly.lua" ]
  }


.. highlight:: lua
               
Next, disallow POST/PUT/DELETE requests to the ``public`` using the
``ReadOnly.lua`` script::

  function IncomingHttpRequestFilter(method, uri, ip, username, httpHeaders)
    if method == 'GET' then
      return true
    elseif username == 'admin' then
      return true
    else
      return false
    end
  end


.. highlight:: text
               
Finally, setup the nginx reverse proxy so that it automatically adds
the `HTTP basic authentication header
<https://en.wikipedia.org/wiki/Basic_access_authentication>`__ that is
expected by Orthanc for the ``public`` user::

    server {
       listen  80  default_server;
       ...
       location  /orthanc/  {
          proxy_pass http://127.0.0.1:8042;
          proxy_set_header HOST $host;
          proxy_set_header X-Real-IP $remote_addr;
          rewrite /orthanc(.*) $1 break;

          // Use the "public" user with the "hello" password
          proxy_set_header Authorization "Basic cHVibGljOmhlbGxv";
       }
       ...
    }
  
The ``cHVibGljOmhlbGxv`` corresponds to the `Base64 encoding
<https://en.wikipedia.org/wiki/Base64>`__ of the string
``public:hello``, as can be seen using the following bash command
line::

  $ echo -n 'public:hello' |base64
  cHVibGljOmhlbGxv

Note that more fine-grained access control can be achieved using
:ref:`Python plugins <python_authorization>` or the :ref:`advanced
authorization plugin <authorization>`.
  

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

