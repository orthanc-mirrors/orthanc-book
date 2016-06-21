.. _iis:

How can I run Orthanc behind Microsoft IIS?
===========================================

Similarly to :ref:`Apache <apache>` and :ref:`nginx <nginx>`, Orthanc
can run behind `Microsoft IIS (Internet Information Services)
<https://en.wikipedia.org/wiki/Internet_Information_Services>`__
servers through reverse proxying. The instructions below are provided
courtesy of `Mark Hodge
<https://groups.google.com/d/msg/orthanc-users/3-b3cLBAr8U/QIePcADMAAAJ>`__.
They also illustrate how to configure :ref:`HTTPS encryption <https>`.

- IIS is available as a feature you can enable via the Programs and Features in non Server versions of Windows.

- Add Application Request Routing 3.0.

- Add URL Rewrite module 2.

- In IIS Manager bind an SSL certificate to port 443 on the default web site being used for Orthanc.

- Add the following ``web.config`` at the root of the default website:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
      <system.webServer>
        <rewrite>
          <rules>
            <clear />
            <rule name="HTTP to HTTPS redirect" stopProcessing="true">
              <match url="(.*)" />
              <conditions logicalGrouping="MatchAll" trackAllCaptures="false">
                <add input="{HTTPS}" pattern="off" ignoreCase="true" />
              </conditions>
              <action type="Redirect" url="https://{HTTP_HOST}/{R:1}" redirectType="Found" />
            </rule>
            <rule name="ReverseProxyInboundRule1" stopProcessing="true">
              <match url="(.*)" />
              <conditions logicalGrouping="MatchAll" trackAllCaptures="false" />
              <action type="Rewrite" url="http://127.0.0.1:8042/{R:1}" />
            </rule>
          </rules>
        </rewrite>
      </system.webServer>
    </configuration>

- In IIS Manager Open Application Request Routing Cache click on
  Server Proxy Settings on the right side of the window, change the
  Time-out to a much higher value. eg., 3600 = 1 hour to ensure
  download of DICOMDIR or ZIP's doesn't time out.

- To allow user authentication against an Active Directory group add
  the following directly after ``<configuration>`` in the above
  ``web.config``, grant the appropriate Active Directory group read
  permission on the ``wwwroot`` folder:
 
.. code-block:: xml

    <system.web>
        <authentication mode="Windows" />
    </system.web>

- You also need to make sure registered users is empty in the Orthanc Configuration.json file:

.. code-block:: json

    [...]
    "RegisteredUsers" : {  },
    [...]
