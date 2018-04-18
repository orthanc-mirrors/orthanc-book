.. _log:

Collecting logs
---------------

Standard logs
=============

Everytime the Orthanc service starts, it will generate
a new log file in ``C:\Program Files\Orthanc Server\Logs`` on Windows 
and in ``/var/log/orthanc/`` on Linux.  

By default, on Windows, if the Orthanc service fails to start, it will 
retry to start 5 times and stop so it does not generate thousands of log files.

Log files are named as ``Orthanc.log.YYYYMMDD-hhmmss.ffff`` including
the date/time when Orthanc was started.  

Orthanc is not removing old logs so these log files might accumulate 
and consume lot's of space.  It's up to you to manage the logs folder
to make sure you don't fill your disk with logs.



Generating an exploitable debug log
===================================

By default, Orthanc logs only the `WARNING` and `ERROR` level
logs.  For your log to be exploitable by the Orthanc community, you must
generate them with the ``--verbose`` or ``--trace`` to get the `INFO` 
and `TRACE` information levels.  If you are using
Orthanc at the command-line, simply add these flags and redirect the
standard outputs to some log file. 

However, if you use packaged versions of Orthanc that runs the server
in background, you will have to manually start Orthanc. The sections
below explain how to achieve this goal with the officially supported
packages.


Under Windows
^^^^^^^^^^^^^

Under Windows, if you used the official installer:

1. Download the `precompiled command-line version
   <http://www.orthanc-server.com/download-windows.php>`__ of Orthanc.

2. Stop the Orthanc service. The actual process depends on your
   version of Windows.

3. Copy the just-downloaded ``Orthanc-1.3.2-Release.exe`` together
   with your configuration file (that is by default located in
   ``C:\Orthanc\Configuration.json``) into the same folder
   (e.g. ``C:\Temp``).

4. Type in a command-line shell, to generate the ``Orthanc.log`` file::

   $ cd C:\Temp
   $ Orthanc-1.3.2-Release.exe --verbose Configuration.json > Orthanc.log 2<&1

5. Restart the Orthanc service.


Under Debian GNU/Linux
^^^^^^^^^^^^^^^^^^^^^^

1. Stop the Orthanc service::

   $ sudo /etc/init.d/orthanc stop

2. Manually start Orthanc (using the same configuration as the
   service) and generate the log::

   $ sudo -u orthanc /usr/sbin/Orthanc --verbose /etc/orthanc/ > Orthanc.log 2>&1

3. Restart the Orthanc service::

   $ sudo /etc/init.d/orthanc start


Under Docker
^^^^^^^^^^^^

The command-line to be used is::

  $ sudo docker run -a stderr -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc --verbose /etc/orthanc > Orthanc.log 2>&1
