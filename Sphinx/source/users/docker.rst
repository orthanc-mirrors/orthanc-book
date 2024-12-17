.. _docker:
.. highlight:: bash


jodogne/orthanc Docker images
=============================

.. toctree::
   :hidden:

   docker-orthancteam.rst
   

.. contents::
   :depth: 3


Introduction
------------

`Docker images <https://en.wikipedia.org/wiki/Docker_(software)>`__
for the Orthanc core and its official plugins are freely available on
the `DockerHub platform <https://hub.docker.com/u/jodogne/>`__. The
source code of the corresponding Docker images is available on `GitHub
<https://github.com/jodogne/OrthancDocker>`__.


.. _docker-jodogne-vs-orthanc-team:

``jodogne/orthanc`` vs. ``orthancteam/orthanc`` Docker images
-------------------------------------------------------------

Two different flavors of Docker images for Orthanc are available:

* The ``jodogne/orthanc`` and ``jodogne/orthanc-plugins`` Docker images that are
  described on this page are regularly kept in sync with the latest releases of
  the Orthanc project, with a basic configuration system that is inherited from
  the Debian packages (i.e., manual edition of the configuration files). 
  
  This is also where the new experimental features from `Sébastien Jodogne's
  research team at UCLouvain <https://orthanc.uclouvain.be/>`__ are initially
  released. The binaries used in these images correspond to the Linux Standard
  Base binaries. 
  
  The default user interface is the built-in **Orthanc Explorer**. 
  
  These images are most useful to **software developers and researchers**.

* Our commercial partner `Orthanc Team <https://orthanc.team/>`__ also
  `publishes separate Docker images
  <https://hub.docker.com/r/orthancteam/orthanc>`__.  
  
  These ``orthancteam/orthanc`` images are released 2 or 3 times a month every
  time a new version of a plugin or Orthanc is available or every time the base
  Debian image needs to be updated for security reasons.  
  
  Each image has a tag and the `list of each component version is documented
  <https://hub.docker.com/r/orthancteam/orthanc>`__.
  
  These images support both AMD64 and ARM64 architectures.
  
  These images can be configured using congirutation files or **environment
  variables** (which is very handy if using Docker Compose or Kubernetes). 
  
  The default user interface is the **Orthanc Explorer 2** :ref:`plugin
  <orthanc-explorer-2>`. 
  
  These images are targeted at **ops teams and end-users**.

  A :ref:`specific page <docker-orthancteam>` is available to describe how these
  images should be used. 

**Note for CentOS users:** The Docker environment might be difficult to
configure on your platform. Hints are available on the `Orthanc Users
discussion group
<https://groups.google.com/d/msg/orthanc-users/w-uPAknnRQc/-XhzBGSCAwAJ>`__.


Running the Orthanc core
------------------------

The following command will start the core of Orthanc, with all the
plugins disabled::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc

Once Orthanc is running, use Mozilla Firefox at URL
http://localhost:8042/ to interact with Orthanc. The default username
is ``orthanc`` and its password is ``orthanc``.

The command above starts the mainline version of Orthanc, whose
development is in continuous progress. Do not forget to regularly
update the Docker image to benefit from the latest features::

  $ docker pull jodogne/orthanc

If more stability is required, you can select the official release of
Orthanc to be run::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc:1.12.5

Passing additional command-line options (e.g. to make Orthanc verbose)
can be done as follows (note the ``/etc/orthanc`` option that is
required for Orthanc to find its configuration files)::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc:1.12.5 /etc/orthanc --verbose


Usage, with plugins enabled
---------------------------

The following command will run the mainline version of the Orthanc
core, together with its :ref:`Web viewer <webviewer>`, its
:ref:`PostgreSQL support <postgresql>`, its :ref:`DICOMweb
implementation <dicomweb>`, and its :ref:`whole-slide imaging viewer
<wsi>`::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-plugins

Or you can also start a specific version of Orthanc for more stability::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-plugins:1.12.5

If you have an interest in the :ref:`Python plugin <python-plugin>`,
you can use the ``orthanc-python`` image. The latter image is a
heavier version of the ``orthanc-plugins`` image, as it embeds the
Python 3.7 interpreter. Here is how to start this image::

  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-python
  $ docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-python:1.12.5
  

Fine-tuning the configuration
-----------------------------

For security reasons, you should at least protect your instance of
Orthanc by changing this default user, in the ``RegisteredUsers``
:ref:`configuration option <configuration>`. You will also probably
need to fine-tune other parameters, notably the list of the DICOM
modalities Orthanc knows about.

You can generate a custom configuration file for Orthanc as follows::

  $ docker run --rm --entrypoint=cat jodogne/orthanc:1.12.5 /etc/orthanc/orthanc.json > /tmp/orthanc.json

Then, edit the just-generated file ``/tmp/orthanc.json`` and restart
Orthanc with your updated configuration::

  $ docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro jodogne/orthanc:1.12.5

*Remark:* These Docker images automatically set the environment
variable ``MALLOC_ARENA_MAX`` to ``5`` in order to :ref:`control
memory usage <scalability-memory>`. This default setting can be
overriden by providing the option ``-e MALLOC_ARENA_MAX=1`` when
invoking ``docker run`` (the value ``0`` corresponds to the default
value).


.. _docker-compose:

Configuration management using Docker Compose
---------------------------------------------

Depending on the context, the `Docker Compose tool
<https://docs.docker.com/compose/>`__ might be easier to use than the
plain Docker tool, as it allows replacing long command lines as above,
by plain configuration files. The trick here is to provide the JSON
configuration files to Orthanc as `secrets
<https://docs.docker.com/compose/compose-file/#secrets>`__ (note that
the related option ``configs`` could in theory be better,
unfortunately it is only available to `Docker Swarm
<https://github.com/docker/compose/issues/5110>`__).

.. highlight:: yaml

First create the ``docker-compose.yml`` file as follows (this one uses
the `YAML file format <https://en.wikipedia.org/wiki/YAML>`__)::

  version: '3.1'  # Secrets are only available since this version of Docker Compose
  services:
    orthanc:
      image: jodogne/orthanc-plugins:1.12.5
      command: /run/secrets/  # Path to the configuration files (stored as secrets)
      ports:
        - 4242:4242
        - 8042:8042
      secrets:
        - orthanc.json
      environment:
        - ORTHANC_NAME=HelloWorld
  secrets:
    orthanc.json:
      file: orthanc.json

.. highlight:: json

Then, place the configuration file ``orthanc.json`` next to the
``docker-compose.yml`` file. Here is a minimalist ``orthanc.json``::

  {
    "Name" : "${ORTHANC_NAME} in Docker Compose",
    "RemoteAccessAllowed" : true
  }

.. highlight:: bash

This single configuration file should contain all the required
configuration options for Orthanc and all its plugins. The container
can then be started as follows::

  $ docker-compose up
               
Note how the `environment variable
<https://docs.docker.com/compose/environment-variables/>`__
``ORTHANC_NAME`` has been used in order to easily adapt the
configuration of Orthanc. This results from the fact that Orthanc
injects :ref:`environment variables <orthanc-environment-variables>`
once reading the content of its configuration files (since Orthanc
1.5.0).

  
Making the Orthanc database persistent
--------------------------------------

The filesystem of Docker containers is volatile (its content is
deleted once the container stops). You can make the Orthanc database
persistent by mapping the ``/var/lib/orthanc/db`` folder of the
container to some path in the filesystem of your Linux host, e.g.::

  $ mkdir /tmp/orthanc-db
  $ docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc-db/:/var/lib/orthanc/db/ jodogne/orthanc:1.12.5


Whole-slide imaging support
---------------------------

The ``orthanc-plugins`` image includes support for :ref:`microscopic
whole-slide imaging (WSI) <wsi>`. For instance, the following command
will start the WSI viewer plugin transparently together with Orthanc::

  $ docker run -p 4242:4242 -p 8042:8042 --rm --name orthanc-wsi jodogne/orthanc-plugins:1.12.5

Note that we gave the name ``orthanc-wsi`` to this new Docker
container. Then, the Dicomizer command-line tool can be invoked as
follows::

  $ docker run -t -i --rm --link=orthanc-wsi:orthanc --entrypoint=OrthancWSIDicomizer -v /tmp/Source.tif:/tmp/Source.tif:ro jodogne/orthanc-plugins:1.12.5 --username=orthanc --password=orthanc --orthanc=http://orthanc:8042/ /tmp/Source.tif

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
instruct the Dicomizer to use `OpenSlide <https://openslide.org/>`__
to decode it by adding the ``--openslide`` option::

  $ docker run -t -i --rm --link=orthanc-wsi:orthanc --entrypoint=OrthancWSIDicomizer -v /tmp/Source.svs:/tmp/Source.svs:ro jodogne/orthanc-plugins:1.12.5 --username=orthanc --password=orthanc --orthanc=http://orthanc:8042/ --openslide=libopenslide.so /tmp/Source.svs


PostgreSQL and Orthanc inside Docker
------------------------------------

It is possible to run both Orthanc and PostgreSQL inside Docker. First, start the official PostgreSQL container::

  $ docker run --name some-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pgpassword --rm postgres

Open another shell, and create a database to host the Orthanc database::

  $ docker run -it --link some-postgres:postgres --rm postgres sh -c 'echo "CREATE DATABASE orthanc;" | exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres'

You will have to type the password (cf. the environment variable
``POSTGRES_PASSWORD`` above that it set to ``pgpassword``). Then,
retrieve the IP and the port of the PostgreSQL container, together
with the default Orthanc configuration file::

  $ docker inspect --format '{{ .NetworkSettings.IPAddress }}' some-postgres
  $ docker inspect --format '{{ .NetworkSettings.Ports }}' some-postgres
  $ docker run --rm --entrypoint=cat jodogne/orthanc-plugins:1.12.5 /etc/orthanc/orthanc.json > /tmp/orthanc.json

.. highlight:: text

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

  $ docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro jodogne/orthanc-plugins:1.12.5


Debugging
---------

.. highlight:: text

For debugging purpose, you can start an interactive bash session as
follows::

  $ docker run -i -t --rm --entrypoint=bash jodogne/orthanc:1.12.5
  $ docker run -i -t --rm --entrypoint=bash jodogne/orthanc-plugins:1.12.5
