General information
===================

Orthanc is a lightweight, RESTful Vendor Neutral Archive for
DICOM. General information about Orthanc can be found on its
[official Website](http://www.orthanc-server.com/).

This repository contains the source code of the
[Orthanc Book](https://orthanc.uclouvain.be/book/), that documents how
Orthanc can be used. It also contains the source code of the
documentation of the
[REST API of Orthanc](https://orthanc.uclouvain.be/api/). The continuous
integration server (CIS) of Orthanc watches this repository, and
automatically publishes modifications online.


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
   publish the new version [online](https://orthanc.uclouvain.be/book/).



REST API of Orthanc
===================

The REST API of Orthanc is now fully documented in the [source code of
the Orthanc
server](https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Sources/OrthancRestApi).
The `--openapi=` and the `--cheatsheet=` command-line options of
Orthanc automatically generate respectively the [OpenAPI in JSON
format](https://swagger.io/specification/) and its [quick reference
(cheatsheet)](https://orthanc.uclouvain.be/book/users/rest-cheatsheet.html)
in CSV format that is designed to be included right into the [Orthanc
Book](https://orthanc.uclouvain.be/hg/orthanc-book/file/default/Sphinx/source/users/rest-cheatsheet.csv).

In order to contribute to the documentation of the REST API, you can
[propose a simple
patch](https://orthanc.uclouvain.be/book/developers/repositories.html#simple-patch-import-export)
to the core of Orthanc to be reviewed by the core maintainers.
