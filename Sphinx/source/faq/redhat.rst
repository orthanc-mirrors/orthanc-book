.. highlight:: bash
.. _redhat:

Accessing an Orthanc instance running inside Fedora/RHEL/CentOS
===============================================================

For remote access to Orthanc, you will have to open the 4242 and the
8042 ports on iptables, that are closed by default::

    $ sudo iptables -I INPUT -p tcp --dport 8042 -j ACCEPT
    $ sudo iptables -I INPUT -p tcp --dport 4242 -j ACCEPT
    $ sudo iptables-save 
