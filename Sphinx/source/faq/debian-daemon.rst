.. highlight:: bash

Installing Orthanc as a Debian/Ubuntu daemon
============================================

To install Orthanc as a GNU/Linux daemon on a Debian/Ubuntu system,
you can:

1. Download this `service script
   <http://anonscm.debian.org/cgit/debian-med/orthanc.git/tree/debian/orthanc.init>`_
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
