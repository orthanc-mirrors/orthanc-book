.. _docker:
.. highlight:: bash


Orthanc for Docker
==================

.. contents::
   :depth: 3


Introduction
------------

`Docker images <https://en.wikipedia.org/wiki/Docker_(software)>`__
for the Orthanc core and its official plugins are freely available on
the `DockerHub platform <https://hub.docker.com/u/jodogne/>`__. The
source code of the corresponding Docker images is available on `GitHub
<https://github.com/jodogne/OrthancDocker>`__.

*Note for CentOS users:* The Docker environment might be difficult to
configure on your platform. Hints are available on the `Orthanc Users
discussion group
<https://groups.google.com/d/msg/orthanc-users/w-uPAknnRQc/-XhzBGSCAwAJ>`__.


Running the Orthanc core
------------------------

The following command will start the core of Orthanc, with all the
plugins disabled::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc

Once Orthanc is running, use Mozilla Firefox at URL
http://localhost:8042/ to interact with Orthanc. The default username
is ``orthanc`` and its password is ``orthanc``.

The command above starts the mainline version of Orthanc, whose
development is in continuous progress. Do not forget to regularly
update the Docker image to benefit from the latest features::

  $ sudo docker pull jodogne/orthanc

If more stability is required, you can select the official release of
Orthanc to be run::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc:1.3.2

Passing additional command-line options (e.g. to make Orthanc verbose)
can be done as follows (note the ``/etc/orthanc`` option that is
required for Orthanc to find its configuration files)::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc /etc/orthanc --verbose


Usage, with plugins enabled
---------------------------

The following command will run the mainline version of the Orthanc
core, together with its :ref:`Web viewer <webviewer>`, its
:ref:`PostgreSQL support <postgresql>`, its :ref:`DICOMweb
implementation <dicomweb>`, and its :ref:`whole-slide imaging viewer
<wsi>`::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-plugins


Fine-tuning the configuration
-----------------------------

For security reasons, you should at least protect your instance of
Orthanc by changing this default user, in the ``RegisteredUsers``
:ref:`configuration option <configuration>`. You will also probably
need to fine-tune other parameters, notably the list of the DICOM
modalities Orthanc knows about.

You can generate a custom configuration file for Orthanc as follows::

  $ sudo docker run --rm --entrypoint=cat jodogne/orthanc /etc/orthanc/orthanc.json > /tmp/orthanc.json

Then, edit the just-generated file ``/tmp/orthanc.json`` and restart
Orthanc with your updated configuration::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro jodogne/orthanc


Making the Orthanc database persistent
--------------------------------------

The filesystem of Docker containers is volatile (its content is
deleted once the container stops). You can make the Orthanc database
persistent by mapping the ``/var/lib/orthanc/db`` folder of the
container to some path in the filesystem of your Linux host, e.g.::

  $ mkdir /tmp/orthanc-db
  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc-db/:/var/lib/orthanc/db/ jodogne/orthanc:1.3.2 


Whole-slide imaging support
---------------------------

The ``orthanc-plugins`` image includes support for :ref:`microscopic
whole-slide imaging (WSI) <wsi>`. For instance, the following command
will start the WSI viewer plugin transparently together with Orthanc::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm --name orthanc-wsi jodogne/orthanc-plugins

Note that we gave the name ``orthanc-wsi`` to this new Docker
container. Then, the Dicomizer command-line tool can be invoked as
follows::

  $ sudo docker run -t -i --rm --link=orthanc-wsi:orthanc --entrypoint=OrthancWSIDicomizer -v /tmp/Source.tif:/tmp/Source.tif:ro jodogne/orthanc-plugins --username=orthanc --password=orthanc --orthanc=http://orthanc:8042/ /tmp/Source.tif

This command needs a few explanations:

* ``--link=orthanc-wsi:orthanc`` links the container running the
  Dicomizer, to the Docker container running Orthanc that we started
  just before.
* ``--entrypoint=OrthancWSIDicomizer`` specifies that the Dicomizer
  must be run instead of the Orthanc server.
* ``-v /tmp/Source.tif:/tmp/Source.tif:ro`` maps the source image
  ``/tmp/Source.tif`` on the host computer into the Orthanc container
  as read-only file ``/tmp/Source.tif``.
* ``--orthanc=http://orthanc:8042/`` instructs the Dicomizer to push
  images through the ``--link`` created above.
* ``--username=orthanc --password=orthanc`` correspond to the default
  credentials of the ``orthanc-plugins`` image.

Obviously, you are free to add all the options you wish (check out the
``--help`` flag to list these options). In particular, the
``--dataset`` option allows to specify DICOM tags, in the JSON file
format, so as to include them in the resulting DICOM series (the
option ``--sample-dataset`` prints a sample JSON file that has the
expected format).

If you have a source image that is not a hierarchical TIFF, you must
instruct the Dicomizer to use `OpenSlide <http://openslide.org/>`__ to
decode it by adding the ``--openslide`` option::

  $ sudo docker run -t -i --rm --link=orthanc-wsi:orthanc --entrypoint=OrthancWSIDicomizer -v /tmp/Source.svs:/tmp/Source.svs:ro jodogne/orthanc-plugins --username=orthanc --password=orthanc --orthanc=http://orthanc:8042/ --openslide=libopenslide.so /tmp/Source.svs


PostgreSQL and Orthanc inside Docker
------------------------------------

It is possible to run both Orthanc and PostgreSQL inside Docker. First, start the official PostgreSQL container::

  $ sudo docker run --name some-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pgpassword --rm postgres

Open another shell, and create a database to host the Orthanc database::

  $ sudo docker run -it --link some-postgres:postgres --rm postgres sh -c 'echo "CREATE DATABASE orthanc;" | exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres'

You will have to type the password (cf. the environment variable
``POSTGRES_PASSWORD`` above that it set to ``pgpassword``). Then,
retrieve the IP and the port of the PostgreSQL container, together
with the default Orthanc configuration file::

  $ sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' some-postgres
  $ sudo docker inspect --format '{{ .NetworkSettings.Ports }}' some-postgres
  $ sudo docker run --rm --entrypoint=cat jodogne/orthanc-plugins /etc/orthanc/orthanc.json > /tmp/orthanc.json

.. highlight:: json

Add the following section to ``/tmp/orthanc.json`` (adapting the
values Host and Port to what docker inspect said above)::

  "PostgreSQL" : {
    "EnableIndex" : true,
    "EnableStorage" : true,
    "Host" : "172.17.0.38",
    "Port" : 5432,
    "Database" : "orthanc",
    "Username" : "postgres",
    "Password" : "pgpassword"
  }

.. highlight:: bash

Finally, you can start Orthanc::

  $ sudo docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro jodogne/orthanc-plugins


Debugging
---------

For debugging purpose, you can start an interactive bash session as
follows::

  $ sudo docker run -i -t --rm --entrypoint=bash jodogne/orthanc
  $ sudo docker run -i -t --rm --entrypoint=bash jodogne/orthanc-plugins
