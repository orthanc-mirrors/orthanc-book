Starting Orthanc as a GNU/Linux daemon
======================================

.. contents::

.. highlight:: bash

"init" flavor
-------------

To install Orthanc as a GNU/Linux `init daemon
<https://en.wikipedia.org/wiki/Init>`__ on a Debian/Ubuntu system, you
can:

1. Download this `service script
   <https://salsa.debian.org/med-team/orthanc/raw/master/debian/orthanc.init>`_
   (this file is part of the `official Debian package
   <https://tracker.debian.org/pkg/orthanc>`_ of Orthanc),
2. Adapt some of its variables to reflect the configuration of your
   system,
3. Copy it in ``/etc/init.d`` as root (the filename cannot contain
   dot, otherwise it is not executed), make it belong to root, and tag
   it as executable::

    $ sudo mv orthanc.init /etc/init.d/orthanc
    $ sudo chown root:root /etc/init.d/orthanc
    $ sudo chmod 755 /etc/init.d/orthanc

4. If you wish the daemon to be automatically launched at boot time and stopped at shutdown::

    $ sudo update-rc.d orthanc defaults

5. If you wish to remove the automatic launching at boot time later on::

    $ sudo update-rc.d -f orthanc remove

*Note*: You can use ``rcconf`` to easily monitor the services that are
run at startup::

    $ sudo apt-get install rcconf


"systemd" flavor
----------------

A sample `systemd daemon <https://en.wikipedia.org/wiki/Systemd>`__
for Orthanc can be found in the official `Debian package
<https://tracker.debian.org/pkg/orthanc>`_ and in the official `Fedora
package <https://src.fedoraproject.org/rpms/orthanc/tree/f32>`__ (now
orphaned - please consider :ref:`contributing by adopting this package
<contributing>`):

1. Download the `systemd script
   <https://salsa.debian.org/med-team/orthanc/raw/master/debian/orthanc.service>`__,
2. Adapt some of its variables to reflect the configuration of your
   system,
3. Copy it as ``/etc/systemd/system/orthanc.service``,
4. Start the daemon as follows::

     $ sudo systemctl daemon-reload
     $ sudo systemctl start orthanc.service

5. To make this change permanent after a reboot, you can create a
   symbolic link as follows::

     $ sudo ln -s /etc/systemd/system/orthanc.service /etc/systemd/system/default.target.wants/
    

Other GNU/Linux distributions
-----------------------------

The instructions above have been tested on Debian/Ubuntu/Fedora
systems, but should work similarly on other GNU/Linux distributions.
