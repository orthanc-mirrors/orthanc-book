.. _serve-folders:


Sample Serve Folders plugin
===========================

This **official** plugin enables Orthanc to serve additional folders
from the filesystem using its embedded Web server. This plugin is
extremely useful when creating new Web applications on the top of the
REST API of Orthanc, as it allows to fulfill the `same-origin policy
<https://en.wikipedia.org/wiki/Same-origin_policy>`__ without setting
up a reverse proxy.
 
The source code of this sample plugin is `available in the source
distribution of Orthanc
<https://bitbucket.org/sjodogne/orthanc/src/default/Plugins/Samples/ServeFolders/>`__
(GPLv3 license).
