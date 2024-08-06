How do you get "mainline" binaries ?
==================================

``Mainline`` binaries are non official releases of Orthanc containing
the latest version of the code.  They are built after each commit
or every night.

Always take care before using one of these versions since they might
contain untested features or temporary code.

Windows, OSX and Linux LSB binaries are built directly after each commit
and are available in the `Downloads page <https://orthanc.uclouvain.be/downloads/>`__
of each component in the ``mainline`` folder.

:ref:`orthancteam <docker-orthancteam>` Docker images are built every
night and are updated only if the full integration tests have been run successfully.
The "mainline" versions are named differently and are available under:

- ``orthancteam/orthanc-pre-release:master-unstable``
- ``orthancteam/orthanc-pre-release:master-full-unstable``
