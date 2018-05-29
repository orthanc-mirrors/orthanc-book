General information
===================

Orthanc is a lightweight, RESTful Vendor Neutral Archive for DICOM.

General information about Orthanc can be found on its [official Website](http://www.orthanc-server.com/).

This repository contains the source code of the [Orthanc Book](http://book.orthanc-server.com/), that documents how Orthanc can be used.


Setup
-----

To build the Orthanc Book from sources, you need to install [Sphinx](http://www.sphinx-doc.org/), the Python Documentation Generator.


### Installing Sphinx under Ubuntu 14.04 LTS ###

    # sudo pip install sphinx sphinx_bootstrap_theme


Generating the documentation
----------------------------

### Under Linux ###

    # cd ./Sphinx
    # make html

The HTML documentation will be available in the folder
`./build/html`. You can for instance open it using Mozilla Firefox as
follows:

    # firefox ./build/html/index.html


How to contribute
-----------------

 * Make sure to understand the [reStructuredText file format](https://en.wikipedia.org/wiki/ReStructuredText).
 * Fork this repository onto your BitBucket account.
 * Edit the content of the [`./Sphinx/source/` folder](./Sphinx/source/).
 * Submit a [pull request](https://confluence.atlassian.com/bitbucket/create-a-pull-request-945541466.html) for review by the Orthanc project.
 * Once the pull request is reviewed, the continuous integration server of the Orthanc project will automatically publish the new version [online](http://book.orthanc-server.com/).
