General information
===================

Orthanc is a lightweight, RESTful Vendor Neutral Archive for
DICOM. General information about Orthanc can be found on its
[official Website](http://www.orthanc-server.com/).

This repository contains the source code of the
[Orthanc Book](http://book.orthanc-server.com/), that documents how
Orthanc can be used. It also contains the source code of the
documentation of the
[REST API of Orthanc](http://api.orthanc-server.com/). The continuous
integration server (CIS) of Orthanc watches this repository, and
automatically publishes modifications online.

Improvements that should be done in the documentation can be reported
onto the
[dedicated issue tracker](https://bitbucket.org/sjodogne/orthanc-book/issues?status=new&status=open).


Orthanc Book
============

Setup
-----

To build the Orthanc Book from sources, you need to install
[Sphinx](http://www.sphinx-doc.org/), the Python Documentation
Generator.


### Installing Sphinx under Ubuntu 14.04 LTS ###

    # sudo pip install sphinx sphinx_bootstrap_theme


Generating the Book
-------------------

### Under Linux ###

    # cd ./Sphinx
    # make html

The HTML documentation will be available in the folder
`./build/html`. You can for instance open it using Mozilla Firefox as
follows:

    # firefox ./build/html/index.html


Contributing to the Book
------------------------

 * Make sure to understand the
   [reStructuredText file format](https://en.wikipedia.org/wiki/ReStructuredText).
 * Fork this repository onto your BitBucket account.
 * Edit the content of the
   [`./Sphinx/source/` folder](./Sphinx/source/).
 * Generate locally the Orthanc Book (cf. above), and make sure it
   displays properly on your computer.
 * Submit a
   [pull request](https://confluence.atlassian.com/bitbucket/create-a-pull-request-945541466.html)
   for review by the Orthanc project.
 * Once the pull request is reviewed and accepted, the continuous
   integration server of the Orthanc project will automatically
   publish the new version [online](http://book.orthanc-server.com/).



REST API of Orthanc
===================

Setup
-----

The REST API of Orthanc is documented according to the
[OpenAPI specification and in the YAML format](https://en.wikipedia.org/wiki/OpenAPI_Specification).

The source code of the OpenAPI documentation can be found in the file
[./OpenAPI/orthanc-openapi.yaml](./OpenAPI/orthanc-openapi.yaml)
within this repository.

Contributing to the OpenAPI
---------------------------

 * Make sure to understand the
   [OpenAPI YAML format](https://swagger.io/specification/).
 * Fork this repository onto your BitBucket account.
 * Edit the content of the
   [`./OpenAPI/orthanc-openapi.yaml` file](./OpenAPI/orthanc-openapi.yaml).
 * Submit a
   [pull request](https://confluence.atlassian.com/bitbucket/create-a-pull-request-945541466.html)
   for review by the Orthanc project.
 * Once the pull request is reviewed and accepted, the continuous
   integration server of the Orthanc project will automatically
   publish the new version [online](http://api.orthanc-server.com/).
