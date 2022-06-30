.. _rest:

REST API of Orthanc
===================

.. contents::
   :depth: 3

One of the major strengths of Orthanc lies in its built-in `RESTful
API
<https://en.wikipedia.org/wiki/Representational_state_transfer>`__,
that can be used to drive Orthanc from external applications,
independently of the programming language that is used to develop
these applications. The REST API of Orthanc gives a full programmatic
access to all the core features of Orthanc.

Importantly, Orthanc Explorer (the embedded administrative interface
of Orthanc) entirely resorts to this REST API for all its features.
This implies that anything that can be done through Orthanc Explorer,
can also be done through REST queries.

*Note:* All the examples are illustrated with the `cURL command-line
tool <https://curl.haxx.se/>`__, but equivalent calls can be readily
transposed to any programming language that supports both HTTP and
JSON.


.. _curl-windows:

Warning about using cURL from the Windows prompt
------------------------------------------------

The examples on this page assume that the user is running a bash shell
on some GNU/Linux distribution. Such a shell has the major advantage
of having the possibility to use either single-quote or double-quotes
characters in order to group a set of characters (including spaces) as
a whole string.

.. highlight:: bash

Unfortunately, the default command-line prompt of Microsoft Windows
**doesn't support single-quote characters**. If you copy/paste a cURL
command-line from this page that mixes single-quote and double-quotes,
it won't work as such, and you'll have to replace single-quotes by
double-quotes, and prefix the double-quotes by a backslash
character. For instance, consider the following command line that
works fine on GNU/Linux::

  $ curl -v -X PUT http://localhost:8042/modalities/sample \
         -d '{"AET" : "ORTHANCC", "Host": "127.0.0.1", "Port": 2002}'

This call will **not** work on the Microsoft Windows prompt as it
contains single-quotes. You should adapt this command line as follows
to run it on Windows::

  $ curl -v -X PUT http://localhost:8042/modalities/sample \
         -d "{\"AET\" : \"ORTHANCC\", \"Host\": \"127.0.0.1\", \"Port\": 2002}"

As an alternative, consider using a different Windows shell, for
instance `Windows PowerShell
<https://fr.wikipedia.org/wiki/Windows_PowerShell>`__ (some examples
of PowerShell can be found below on this page).


.. _sending-dicom-images:

Sending DICOM images
--------------------

.. highlight:: bash

The upload of DICOM files is possible by querying the REST API using
the following syntax::

    $ curl -X POST http://localhost:8042/instances --data-binary @CT.X.1.2.276.0.7230010.dcm

.. highlight:: json

Orthanc will respond with a JSON file that contain information about
the location of the stored instance, such as::

    {
      "ID" : "e87da270-c52b-4f2a-b8c6-bae25928d0b0",
      "Path" : "/instances/e87da270-c52b-4f2a-b8c6-bae25928d0b0",
      "Status" : "Success"
    }

.. highlight:: bash

Note that in the case of curl, setting the ``Expect`` HTTP Header will
significantly `reduce the execution time of POST requests
<https://stackoverflow.com/questions/463144/php-http-post-fails-when-curl-data-1024/463277#463277>`__::

    $ curl -X POST -H "Expect:" http://localhost:8042/instances --data-binary @CT.X.1.2.276.0.7230010.dcm

The code distribution of Orthanc contains a `sample Python script
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.11.1/OrthancServer/Resources/Samples/ImportDicomFiles/ImportDicomFiles.py>`__
that recursively upload the content of some folder into Orthanc using
the REST API::

    $ python ImportDicomFiles.py localhost 8042 ~/DICOM/

Starting with Orthanc 1.8.1, the source distribution of Orthanc
includes another Python script named ``OrthancImport.py`` that
provides more features than ``ImportDicomFiles.py``. It can notably
import the content of ``.zip``, ``.tar.gz`` or ``.tar.bz2`` archives
without having to uncompress them first. It also provides more
comprehensive command-line options. `Check this script out
<https://hg.orthanc-server.com/orthanc/file/Orthanc-1.11.1/OrthancServer/Resources/Samples/ImportDicomFiles/OrthancImport.py>`__.
    

.. highlight:: perl

If you are using Powershell (>= 3.0), you can use the following to send a single
Dicom instance to Orthanc::

    # disabling the progress bar makes the Invoke-RestMethod call MUCH faster
    $ProgressPreference = 'SilentlyContinue'

    # upload it to Orthanc
    $reply = Invoke-RestMethod http://localhost:8042/instances -Method POST -InFile CT.X.1.2.276.0.7230010.dcm

    # display the result
    Write-Host "The instance can be retrieved at http://localhost:8042$($reply.Path)"

.. _rest-access:

Accessing the content of Orthanc
--------------------------------

Orthanc structures the stored DICOM resources using the "Patient,
Study, Series, Instance" model of the DICOM standard. Each DICOM
resource is associated with an :ref:`unique identifier <orthanc-ids>`.

List all the DICOM resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is how you would list all the DICOM resources that are stored in
your local Orthanc instance::

    $ curl http://localhost:8042/patients
    $ curl http://localhost:8042/studies
    $ curl http://localhost:8042/series
    $ curl http://localhost:8042/instances

Note that the result of this command is a `JSON file
<https://en.wikipedia.org/wiki/Json>`__ that contains an array of
resource identifiers. The JSON file format is lightweight and can be
parsed from almost any computer language.

Accessing a patient
^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

To access a single resource, add its identifier to the `URI
<https://en.wikipedia.org/wiki/Uniform_resource_identifier>`__. You
would for instance retrieve the main information about one patient as
follows::

    $ curl http://localhost:8042/patients/dc65762c-f476e8b9-898834f4-2f8a5014-2599bc94

.. highlight:: json

Here is a possible answer from Orthanc::

 {
   "ID" : "07a6ec1c-1be5920b-18ef5358-d24441f3-10e926ea",
   "MainDicomTags" : {
      "OtherPatientIDs" : "(null)",
      "PatientBirthDate" : "0",
      "PatientID" : "000000185",
      "PatientName" : "Anonymous^Unknown",
      "PatientSex" : "O"
   },
   "Studies" : [ "9ad2b0da-a406c43c-6e0df76d-1204b86f-78d12c15" ],
   "Type" : "Patient"
 }

This is once again a JSON file. Note how Orthanc gives you a summary
of the main DICOM tags that correspond to the patient level.


.. _browsing-hierarchy:

Browsing from the patient down to the instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

The field ``Studies`` list all the DICOM studies that are associated
with the patient. So, considering the patient above, we would go down
in her DICOM hierarchy as follows::

    $ curl http://localhost:8042/studies/9ad2b0da-a406c43c-6e0df76d-1204b86f-78d12c15

.. highlight:: json

And Orthanc could answer::

 {
   "ID" : "9ad2b0da-a406c43c-6e0df76d-1204b86f-78d12c15",
   "MainDicomTags" : {
      "AccessionNumber" : "(null)",
      "StudyDate" : "20120716",
      "StudyDescription" : "TestSUVce-TF",
      "StudyID" : "23848",
      "StudyInstanceUID" : "1.2.840.113704.1.111.7016.1342451220.40",
      "StudyTime" : "170728"
   },
   "ParentPatient" : "07a6ec1c-1be5920b-18ef5358-d24441f3-10e926ea",
   "Series" : [
      "6821d761-31fb55a9-031ebecb-ba7f9aae-ffe4ddc0",
      "2cc6336f-2d4ae733-537b3ca3-e98184b1-ba494b35",
      "7384c47e-6398f2a8-901846ef-da1e2e0b-6c50d598"
   ],
   "Type" : "Study"
 }

.. highlight:: bash

The main DICOM tags are now those that are related to the study
level. It is possible to retrieve the identifier of the patient in the
``ParentPatient`` field, which can be used to go upward the DICOM
hierarchy. But let us rather go down to the series level by using the
``Series`` array. The next command would return information about one
of the three series that have just been reported::

    $ curl http://localhost:8042/series/2cc6336f-2d4ae733-537b3ca3-e98184b1-ba494b35

.. highlight:: json

Here is a possible answer::

 {
   "ExpectedNumberOfInstances" : 45,
   "ID" : "2cc6336f-2d4ae733-537b3ca3-e98184b1-ba494b35",
   "Instances" : [
      "41bc3f74-360f9d10-6ae9ffa4-01ea2045-cbd457dd",
      "1d3de868-6c4f0494-709fd140-7ccc4c94-a6daa3a8",
      <...>
      "1010f80b-161b71c0-897ec01b-c85cd206-e669a3ea",
      "e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4"
   ],
   "MainDicomTags" : {
      "Manufacturer" : "Philips Medical Systems",
      "Modality" : "PT",
      "NumberOfSlices" : "45",
      "ProtocolName" : "CHU/Body_PET/CT___50",
      "SeriesDate" : "20120716",
      "SeriesDescription" : "[WB_CTAC] Body",
      "SeriesInstanceUID" : "1.3.46.670589.28.2.12.30.26407.37145.2.2516.0.1342458737",
      "SeriesNumber" : "587370",
      "SeriesTime" : "171121",
      "StationName" : "r054-svr"
   },
   "ParentStudy" : "9ad2b0da-a406c43c-6e0df76d-1204b86f-78d12c15",
   "Status" : "Complete",
   "Type" : "Series"
 }

It can be seen that this series comes from a PET modality. Orthanc has
computed that this series should contain 45 instances.

.. highlight:: bash

So far, we have navigated from the patient level, to the study level,
and finally to the series level. There only remains the instance
level. Let us dump the content of one of the instances::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4

.. highlight:: json

The instance contains the following information::

 {
   "FileSize" : 70356,
   "FileUuid" : "3fd265f0-c2b6-41a2-ace8-ae332db63e06",
   "ID" : "e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4",
   "IndexInSeries" : 6,
   "MainDicomTags" : {
      "ImageIndex" : "6",
      "InstanceCreationDate" : "20120716",
      "InstanceCreationTime" : "171344",
      "InstanceNumber" : "6",
      "SOPInstanceUID" : "1.3.46.670589.28.2.15.30.26407.37145.3.2116.39.1342458737"
   },
   "ParentSeries" : "2cc6336f-2d4ae733-537b3ca3-e98184b1-ba494b35",
   "Type" : "Instance"
 }

.. highlight:: bash

The instance has the index 6 in the parent series. The instance is
stored as a raw DICOM file of 70356 bytes. You would download this
DICOM file using the following command::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/file > Instance.dcm


Accessing the DICOM fields of an instance as a JSON file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

When one gets to the instance level, you can retrieve the hierarchy of
all the DICOM tags of this instance as a JSON file::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/simplified-tags

.. highlight:: json

Here is a excerpt of the Orthanc answer::

 {
   "ACR_NEMA_2C_VariablePixelDataGroupLength" : "57130",
   "AccessionNumber" : null,
   "AcquisitionDate" : "20120716",
   "AcquisitionDateTime" : "20120716171219",
   "AcquisitionTime" : "171219",
   "ActualFrameDuration" : "3597793",
   "AttenuationCorrectionMethod" : "CTAC-SG",
   <...>
   "PatientID" : "000000185",
   "PatientName" : "Anonymous^Unknown",
   "PatientOrientationCodeSequence" : [
      {
         "CodeMeaning" : "recumbent",
         "CodeValue" : "F-10450",
         "CodingSchemeDesignator" : "99SDM",
         "PatientOrientationModifierCodeSequence" : [
            {
               "CodeMeaning" : "supine",
               "CodeValue" : "F-10340",
               "CodingSchemeDesignator" : "99SDM"
            }
         ]
      }
   ],
   <...>
   "StudyDescription" : "TestSUVce-TF",
   "StudyID" : "23848",
   "StudyInstanceUID" : "1.2.840.113704.1.111.7016.1342451220.40",
   "StudyTime" : "171117",
   "TypeOfDetectorMotion" : "NONE",
   "Units" : "BQML",
   "Unknown" : null,
   "WindowCenter" : "1.496995e+04",
   "WindowWidth" : "2.993990e+04"
 }

.. highlight:: bash

If you need more detailed information about the type of the variables
or if you wish to use the hexadecimal indexes of DICOM tags, you are
free to use the following URL::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/tags

Accessing the raw DICOM fields of an instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

You also have the opportunity to access the raw value of the DICOM
tags of an instance, without going through a JSON file. Here is how
you would find the Patient Name of the instance::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/content/0010-0010
    Anonymous^Unknown

The list of all the available tags for this instance can also be retrieved easily::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/content

It is also possible to recursively explore the sequences of tags::

    $ curl http://localhost:8042/instances/e668dcbf-8829a100-c0bd203b-41e404d9-c533f3d4/content/0008-1250/0/0040-a170/0/0008-0104
    For Attenuation Correction

The command above has opened the "0008-1250" tag that is a DICOM
sequence, taken its first child, opened its "0040-a170" tag that is
also a sequence, taken the first child of this child, and returned the
"0008-0104" DICOM tag.

Downloading images
^^^^^^^^^^^^^^^^^^

.. highlight:: bash

As :ref:`explained above <browsing-hierarchy>`, the raw DICOM file
corresponding to a single instance can be retrieved as follows::

  $ curl http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/file > Instance.dcm

It is also possible to download a preview PNG image that corresponds
to some DICOM instance::

  $ curl http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/preview > Preview.png

The resulting image will be a standard graylevel PNG image (with 8
bits per pixel) that can be opened by any painting software. The
dynamic range of the pixel data is stretched to the [0..255] range.
An equivalent JPEG image can be downloaded by setting the `HTTP header
<https://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`__
``Accept`` to ``image/jpeg``::

  $ curl -H 'Accept: image/jpeg' http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/preview > Preview.jpg

If you don't want to stretch the dynamic range, and create a 8bpp or
16bpp PNG image, you can use the following URIs::

  $ curl http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/image-uint8 > full-8.png
  $ curl http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/image-uint16 > full-16.png

In these images, the values are cropped to the maximal value that can
be encoded by the target image format. The
``/instances/{...}/image-int16`` is available as well to download
signed DICOM pixel data.

Since Orthanc 1.4.2, it is also possible to download such images in
the generic `PAM format
<https://en.wikipedia.org/wiki/Netpbm#PAM_graphics_format>`__::

  $ curl -H 'Accept: image/x-portable-arbitrarymap' http://localhost:8042/instances/609665c0-c5198aa2-8632476b-a00e0de0-e9075d94/image-uint16 > full-16.pam

Users of Matlab or Octave can find related information :ref:`in the
dedicated section <matlab>`.


.. _download_numpy:

Downloading decoded images from Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: python

Starting with Orthanc 1.11.0, it is possible to immediately download
DICOM instances and DICOM series as numpy arrays (even if they use a
compressed transfer syntax). This is especially useful for the
integration within AI (artificial intelligence) pipelines. Here is a
sample call::

  import io
  import numpy
  import requests
  
  r = requests.get('https://demo.orthanc-server.com/instances/6582b1c0-292ad5ab-ba0f088f-f7a1766f-9a29a54f/numpy')
  r.raise_for_status()
  
  image = numpy.load(io.BytesIO(r.content))
  print(image.shape)  # (1, 358, 512, 1)

The downloaded numpy array for one single DICOM instance contains
floating-point values, and has a shape of ``(1, height, width, 1)`` if
the corresponding instance is grayscale, or ``(1, height, width, 3)``
if the instance has colors (e.g. in ultrasound images). If applicable,
the ``Rescale Slope (0028,1053)`` and ``Rescale Intercept
(0028,1052)`` DICOM tags are applied to the floating-point values.

Similarly, this feature is available at the series level::

  import io
  import numpy
  import requests
  
  r = requests.get('https://demo.orthanc-server.com/series/dc0216d2-a406a5ad-31ef7a78-113ae9d9-29939f9e/numpy')
  r.raise_for_status()
  
  image = numpy.load(io.BytesIO(r.content))
  print(image.shape)  # (100, 256, 256, 1)

As can be seen, in the case of a DICOM series, the first dimension of
the resulting numpy array corresponds to the depth of the series
(i.e. to its number of 2D slices).

Some options are available for these ``/instances/.../numpy`` and
``/series/.../numpy`` routes:

* ``?compress=1`` will return a ``.npz`` compressed numpy archive
  instead of a plain ``.npy`` numpy array. This can be used to reduce
  the network bandwidth. In such a case, the array of interest is
  named ``arr_0`` in the ``.npz`` archive, e.g.::

    print(image['arr_0'].shape)

* ``?rescale=0`` will skip the conversion to floating-point values,
  and will not apply the rescale slope/intercept. This can be useful
  to reduce the network bandwidth or to receive the original integer
  values of the voxels.


Downloading studies
^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

All instances of a study can be retrieved as a zip file as follows::

  $ curl http://localhost:8042/studies/6b9e19d9-62094390-5f9ddb01-4a191ae7-9766b715/archive > Study.zip

It is also possible to download a zipped DICOMDIR through::

  $ curl http://localhost:8042/studies/6b9e19d9-62094390-5f9ddb01-4a191ae7-9766b715/media > Study.zip


.. _download-pdf-videos:

Downloading PDF or videos
^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Given a DICOM instance that embeds a PDF file (typically, one instance
whose SOP Class UID is ``1.2.840.10008.5.1.4.1.1.104.1`` -
Encapsulated PDF Storage), the PDF content can be downloaded as
follows::

  $ curl http://localhost:8042/instances/1915e0cc-c2c1a0fc-12cdd7f5-3ba32114-a97c2c9b/content/0042,0011 > sample.pdf

This corresponds to downloading the raw DICOM tag "Encapsulated
Document" (0042,0011). Beware that the last byte of the downloaded
file might correspond to one padding byte, if the source PDF had an
odd number of bytes.

Similarly, if you know that a DICOM instance :ref:`embeds a video
<videos>` (which can be tested by checking the :ref:`value of the
metadata <metadata-core>` corresponding to its transfer syntax UID),
the raw video can be downloaded as follows::

  $ curl http://localhost:8042/instances/e465dd27-83c96343-96848735-7035a133-1facf1a0/frames/0/raw > sample.mp4


.. _peering:

Sending resources to remote Orthanc over HTTP/HTTPS (through Orthanc peering)
-----------------------------------------------------------------------------

Orthanc can send its DICOM instances to remote Orthanc servers over
HTTP/HTTPS. Such servers are referred to as :ref:`Orthanc peers
<peers>`. This process can be triggered by the REST API, which is
described in this section.

Configuration
^^^^^^^^^^^^^

.. highlight:: json

You first have to declare the Url of the remote orthanc inside the
:ref:`configuration file <configuration>`. For instance, here is how
to declare a remote orthanc peer::

    ...
    "OrthancPeers" : {
      "sample" : [ "http://localhost:8043" ], // short version
      "sample2" : {                           // long version
        "Url" : "http://localhost:8044",
        "Username" : "alice",                          // optional
        "Password" : "alicePassword",                  // optional
        "HttpHeaders" : { "Token" : "Hello world" },   // optional
        "CertificateFile" : "client.crt",              // optional (only if using client certificate authentication)
        "CertificateKeyFile" : "client.key",           // optional (only if using client certificate authentication)
        "CertificateKeyPassword" : "certpass"          // optional (only if using client certificate authentication)
    },
    ...

.. highlight:: bash

Such a configuration would enable Orthanc to connect to two other
Orthanc instances that listens on the localhost on the ports 8043
and 8044. The peers that are known to Orthanc can be queried::

    $ curl http://localhost:8042/peers?expand

Instead of using the configuration file, peers can be created or
updated through the REST API using the ``PUT`` method of HTTP::

    $ curl -v -X PUT http://localhost:8042/peers/sample -d '{"Url" : "http://127.0.0.1:8043"}'

One peer can also be removed using the ``DELETE`` method as follows::
    
    $ curl -v -X DELETE http://localhost:8042/peers/sample

Note that, by default, peers are read from the Orthanc configuration
files and are updated in Orthanc memory only. If you want your
modifications to be persistent, you should configure Orthanc to store
its peers in the database.  This is done through this configuration::

    ...
    "OrthancPeersInDatabase" : true,
    ...

Sending One Resource
^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Once you have identified the Orthanc identifier of the DICOM resource
that would like to send :ref:`as explained above <rest-access>`, you
would use the following command to send it::

    $ curl -X POST http://localhost:8042/peers/sample/store -d c4ec7f68-9b162055-2c8c5888-5bf5752f-155ab19f

The ``/sample/`` component of the URI corresponds to the identifier of
the remote modality, as specified above in the configuration file.

Note that you can send isolated DICOM instances with this command, but
also entire patients, studies or series. It is possible to send multiple instances with a single POST
request::

    $ curl -X POST http://localhost:8042/peers/sample/store -d '["d4b46c8e-74b16992-b0f5ca11-f04a60fa-8eb13a88","d5604121-7d613ce6-c315a5-a77b3cf3-9c253b23","cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e"]'
     
Note that the list of resources to be sent can include the
:ref:`Orthanc identifiers <orthanc-ids>` of entire patients,
studies or series as well.

**Important remark:** Neither the :ref:`metadata <metadata>`, nor the
:ref:`attachments <attachments>` are transferred between the Orthanc
peers. This is because metadata and attachments are considered as
local to one Orthanc server.


Testing connectivity with a remote peer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

In version 1.5.9+, we have introduced a route to retrieve the ``/system`` info from
a remote peer.  This route can also be used to test the connectivity with that peer
without actually sending a DICOM resource.::

    $ curl http://localhost:8042/peers/sample/system


Using HTTPS
^^^^^^^^^^^

If you're transfering medical data over internet, it is mandatory to
use HTTPS.

On the server side, we recommend to put Orthanc behind an :ref:`HTTPS
server that will take care of the TLS <https>`.

On the client side, in order for the client Orthanc to recognize the
server certificate, you'll have to provide a path to the CA
(certification authority) certificates.  This is done in the
configuration file through this configurationg::

    ...
    "HttpsCACertificates" : "/etc/ssl/certs/ca-certificates.crt,
    ...

If you want your server to accept incoming connections for known hosts only, you can either:

- configure a firewall to accept incoming connections from known IP addresses 
- configure your client Orthanc to use a client certificate to authenticate at the Server.  This is done through the ``CertificateFile``, ``CertificateKeyFile`` and ``CertificateKeyPassword`` entries in the configuration file.




Sending resources to remote modalities (through DICOM C-Store)
--------------------------------------------------------------

Orthanc can send its DICOM instances to remote DICOM modalities (C-Store SCU). This process
can be triggered by the REST API.

Configuration
^^^^^^^^^^^^^

.. highlight:: json

You first have to declare the AET, the IP address and the port number
of the remote modality inside the :ref:`configuration file
<configuration>`. For instance, here is how to declare a remote
modality::

    ...
    "DicomModalities" : {
      "sample" : [ "ORTHANCA", "127.0.0.1", 2000 ], // short version
      "sample2" : {                                 // long version
        "AET" : "ORTHANCB",
        "Port" : 2001,
        "Host" : "127.0.0.1",
        "Manufacturer" : "Generic",
        "AllowEcho" : true,
        "AllowFind" : true,
        "AllowMove" : true,
        "AllowStore" : true
      }
    },
    ...

.. highlight:: bash

Such a configuration would enable Orthanc to connect to two DICOM
stores (for instance, other Orthanc instances) that listens on the
localhost on the port 2000 & 2001. The modalities that are known to Orthanc
can be queried::

    $ curl http://localhost:8042/modalities?expand

Instead of using the configuration file, modalities can be created or
updated through the REST API using the ``PUT`` method of HTTP::

    $ curl -v -X PUT http://localhost:8042/modalities/sample -d '{"AET" : "ORTHANCC", "Host": "127.0.0.1", "Port": 2002}'

One modality can also be removed using the ``DELETE`` method as follows::
    
    $ curl -v -X DELETE http://localhost:8042/modalities/sample

Note that, by default, modalities are read from the Orthanc
configuration files and are updated in Orthanc memory only. If you
want your modifications to be persistent, you should configure Orthanc
to store the modalities in the database.  This is done through this
configuration::

    ...
    "DicomModalitiesInDatabase" : true,
    ...


.. _rest-store-scu:
    
Sending One Resource
^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

Once you have identified the Orthanc identifier of the DICOM resource
that would like to send :ref:`as explained above <rest-access>`, you
would use the following command to send it::

    $ curl -X POST http://localhost:8042/modalities/sample/store -d c4ec7f68-9b162055-2c8c5888-5bf5752f-155ab19f

The ``/sample/`` component of the URI corresponds to the identifier of
the remote modality, as specified above in the configuration file.

Note that you can send isolated DICOM instances with this command, but
also entire patients, studies or series.

Various optional fields are also available.  i.e, if you need to 
monitor the state of a transfer, you can start the transfer in :ref:`asynchronous mode
<jobs>`, which will provide you with the identifier of the Orthanc job::

    $ curl -X POST http://localhost:8042/modalities/sample/store \
      --data '{
                "Resources" : ["d4b46c8e-74b16992-b0f5ca11-f04a60fa-8eb13a88"],
                "Synchronous" : false,
                "LocalAet" : "ORTHANC",
                "MoveOriginatorAet": "ORTHANC",
                "MoveOriginatorID": 1234,
                "Timeout": 10,
                "StorageCommitment": false
              }'


Bulk Store SCU
^^^^^^^^^^^^^^

.. highlight:: bash

Each time a POST request is made to ``/modalities/.../store``, a new
DICOM association is possibly established. This may lead to a large
communication overhead if sending multiple isolated instances by
making one REST call for each of these instances.

To circumvent this problem, you have 2 possibilities:

1. Set the ``DicomAssociationCloseDelay`` option in the
   :ref:`configuration file <configuration>` to a non-zero value. This
   will keep the DICOM connection open for a certain amount of time,
   waiting for new instances to be routed. This is useful if 
   autorouting images :ref:`using Lua <lua-auto-routing>`.

2. It is possible to send multiple instances with a single POST
   request (so-called "Bulk Store SCU", available from Orthanc
   0.5.2)::

    $ curl -X POST http://localhost:8042/modalities/sample/store -d '["d4b46c8e-74b16992-b0f5ca11-f04a60fa-8eb13a88","d5604121-7d613ce6-c315a5-a77b3cf3-9c253b23","cb855110-5f4da420-ec9dc9cb-2af6a9bb-dcbd180e"]'

   The list of the resources to be sent are given as a JSON array. In
   this case, a single DICOM connection is used. `Sample code is
   available
   <https://hg.orthanc-server.com/orthanc/file/default/OrthancServer/Resources/Samples/Python/HighPerformanceAutoRouting.py>`__.

   Note that the list of resources to be sent can include the
   :ref:`Orthanc identifiers <orthanc-ids>` of entire patients,
   studies or series as well.


Performing C-Echo
-----------------

To validate the DICOM connectivity between Orthanc and a remote modality,
you can perform a C-ECHO::

    $ curl -X POST http://localhost:8042/modalities/sample/echo -d '{}'

From Orthanc 1.7.0, you can include an extra ``Timeout`` field::

    $ curl -X POST http://localhost:8042/modalities/sample/echo -d '{ "Timeout": 10 }'

If no ``Timeout`` parameter is specified, the value of the ``DicomScuTimeout``
configuration is used as a default.  If ``Timeout`` is set to zero, this means 
no timeout.

NB: A body containing a valid JSON object is needed by
``/modalities/{id}/echo`` since Orthanc 1.7.0.


Performing C-Move
-----------------

.. highlight:: bash

You can perform a DICOM C-Move to move a specific study from one modality 
to another (including Orthanc itself if you don't specify the ``TargetAet`` 
field).  

I.e. to move a study whose you know the ``StudyInstanceUID`` from
the modality ``sample`` to another Orthanc whose AET is ``ORTHANCB``::

  $ curl --request POST --url http://localhost:8042/modalities/samples/move \
    --data '{ 
              "Level" : "Study", 
              "Resources" : [ 
                { 
                  "StudyInstanceUID": "1.2.840.113543.6.6.4.7.64067529866380271256212683512383713111129" 
                } 
              ], 
              "TargetAet": "ORTHANCB",
              "Timeout": 60 
            }'


Performing Query/Retrieve (C-Find) and Find with REST
-----------------------------------------------------

*Section contributed by Bryan Dearlove*

Orthanc can be used to perform queries on the local Orthanc instance,
or on remote modalities through the REST API.

To perform a query of a remote modality you must define the modality
within the :ref:`configuration file <configuration>` (See
Configuration section under Sending resources to remote modalities).

.. _rest-find-scu:

Performing Queries on Modalities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

To initiate a query you perform a POST command against the Modality
with the identifiers you are looking for. The the example below we are
performing a study level query against the modality sample for any
study descriptions with the word chest within it. This search is case
insensitive unless configured otherwise within the Orthanc
configuration file::

     $ curl --request POST \
       --url http://localhost:8042/modalities/sample/query \
       --data '{
                 "Level" : "Study",
                 "Query" : {
                   "PatientID" : "",
                   "StudyDescription" : "*Chest*",
                   "PatientName" : ""
                 }
               }'

You might be interested in including the ``Normalize`` option to bypass
the normalization of the outgoing C-FIND queries. For instance, for
the ``InstitutionName`` to be included at the ``Study`` level, one would
run::

  $ curl -v http://localhost:8042/modalities/sample/query -X POST -d \
    '{"Level":"Study","Query":{"InstitutionName":"a"},"Normalize":false}'

.. highlight:: json

You will receive back an ID which can be used to retrieve more
information with GET commands or C-Move requests with a POST Command::

     {
     	"ID": "5af318ac-78fb-47ff-b0b0-0df18b0588e0",
     	"Path": "/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0"
     }


Additional Options
^^^^^^^^^^^^^^^^^^

.. highlight:: json

You can use patient identifiers by including the ``*`` within your
search. For example if you were searching for a name beginning with
``Jones`` you can do::

  "PatientName":"Jones*"

If you wanted to search for a name with the words ``Jo`` anywhere
within it you can do::

  "PatientName":"*Jo*"

To perform date searches you can specify within StudyDate a starting
date and/or a before date. For example ``"StudyDate":"20180323-"``
would search for all study dates after the specified date to
now. Doing ``"StudyDate":"20180323-20180325"`` would search for all
study dates between the specified date.


Reviewing Level
^^^^^^^^^^^^^^^

.. highlight:: bash

::

   $ curl --request GET --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/level

Will retrieve the level with which the query was performed, Study,
Series or Instance.


Reviewing Modality
^^^^^^^^^^^^^^^^^^

.. highlight:: bash

::

   $ curl --request GET --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/modality

Will provide the modality name which the original query was performed against.


Reviewing Query
^^^^^^^^^^^^^^^

.. highlight:: bash

To retrieve information on what identifiers the query was originally
performed using you can use the query filter::

  $ curl --request GET --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/query


Reviewing Query Answers
^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

You are able to individually review each answer returned by performing
a GET with the answers parameter::

  $ curl --request GET --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/answers

You will get a JSON back with numbered identifiers for each answer you
received back. For example because we performed a Study level query we
received back 5 studies answers back. We are able to query each answer
for content details::

  $ curl --request GET --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/answers/0/content

If there are content items missing, you may add them by adding that
identifier to the original query. For example if we wanted Modalities
listed in this JSON answer in the initial query we would add to the
POST body: ``"ModalitiesInStudy":""``


Performing Retrieve (C-Move)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: bash

You can perform a C-Move to retrieve all studies within the original
query using a post command and identifying the Modality (named in this 
example ``Orthanc``), to be one to in the POST contents::

  $ curl --request POST --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/retrieve --data Orthanc

You are also able to perform individual C-Moves for a content item by
specifying that individual content item::

  $ curl --request POST --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/answers/0/retrieve --data Orthanc

If C-Moves take too long (for example, performing a C-Move of a big
study), you may run the request in :ref:`asynchronous mode <jobs>`,
which will create a job in Orthanc::

  $ curl --request POST --url http://localhost:8042/queries/5af318ac-78fb-47ff-b0b0-0df18b0588e0/retrieve \
    --data '{"TargetAet":"Orthanc","Synchronous":false}'


.. highlight:: bash

The answer of this POST request is the job ID taking care of the
C-Move command, :ref:`whose status can be monitored <jobs-monitoring>`
in order to detect failure or completion::

  {
      "ID" : "11541b16-e368-41cf-a8e9-3acf4061d238",
      "Path" : "/jobs/11541b16-e368-41cf-a8e9-3acf4061d238"
  }



.. _rest-find:

Performing Finds within Orthanc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. highlight:: bash

Performing a find within the local database of Orthanc is very similar
to using Queries against DICOM modalities and the additional options
listed above work with find also.  When performing a find, you will
receive the Orthanc ID's of all the matched items within your
find. For example if you perform a study level find and 5 Studies
match you will receive 5 study level Orthanc ID's in JSON format as a
response::

  $ curl --request POST --url http://localhost:8042/tools/find \
    --data '{
              "Level" : "Instance",
              "Query" : {
                "Modality" : "CR",
                "StudyDate" : "20180323-",
                "PatientID" : "*"
              }
            }'

Setting the ``Expand`` field to ``true`` in the POST body of the
query will automatically report details about each study::

  $ curl https://demo.orthanc-server.com/tools/find -d '{"Level":"Study","Query":{"PatientName":"KNIX"}}'
  [
    "b9c08539-26f93bde-c81ab0d7-bffaf2cb-a4d0bdd0"
  ]
  $ curl https://demo.orthanc-server.com/tools/find -d '{"Level":"Study","Query":{"PatientName":"KNIX"},"Expand":true}'
  [
    {
      "ID" : "b9c08539-26f93bde-c81ab0d7-bffaf2cb-a4d0bdd0",
      "IsStable" : true,
      "LastUpdate" : "20180414T091528",
      "MainDicomTags" : {
         "InstitutionName" : "0ECJ52puWpVIjTuhnBA0um",
         "ReferringPhysicianName" : "1",
         "StudyDate" : "20070101",
         "StudyDescription" : "Knee (R)",
         "StudyID" : "1",
         "StudyInstanceUID" : "1.2.840.113619.2.176.2025.1499492.7391.1171285944.390",
         "StudyTime" : "120000.000000"
      },
      "ParentPatient" : "6816cb19-844d5aee-85245eba-28e841e6-2414fae2",
      "PatientMainDicomTags" : {
         "PatientID" : "ozp00SjY2xG",
         "PatientName" : "KNIX"
      },
      "Series" : [
         "20b9d0c2-97d85e07-f4dbf4d2-f09e7e6a-0c19062e",
         "edbfa0a9-fa2641d7-29514b1c-45881d0b-46c374bd",
         "f2635388-f01d497a-15f7c06b-ad7dba06-c4c599fe",
         "4d04593b-953ced51-87e93f11-ae4cf03c-25defdcd",
         "5e343c3e-3633c396-03aefde8-ba0e08c7-9c8208d3",
         "8ea120d7-5057d919-837dfbcc-ccd04e0f-7f3a94aa"
      ],
      "Type" : "Study"
    }
  ]

Here is a sample REST API call to find the Orthanc identifiers of all
the DICOM series generated by an imaging modality whose "Device Serial
Number (0018,1000)" DICOM tag is equal to "123"::

  $ curl -X POST http://localhost:8042/tools/find -d '{"Level":"Series","Query":{"DeviceSerialNumber":"123"},"Expand":true}'

If you are interested by a **list of several items** (in this case, in
a list of serial numbers), just separate them with backslashes as
would do with DICOM C-FIND::

  $ curl -X POST http://localhost:8042/tools/find -d '{"Level":"Series","Query":{"DeviceSerialNumber":"123\\abc"},"Expand":true}'

  
  
Additional Options
^^^^^^^^^^^^^^^^^^
.. highlight:: json

You also have the ability to limit the responses by specifying a limit within the body of the POST message. For example::

  "Limit":4

.. highlight:: bash

Since Orthanc 1.11.0, you may also request a specific list of tags in the response (like in a C-FIND) even if these
tags are not stored in the MainDicomTags or if the tags needs to be computed (like ``ModalitiesInStudy``).  This ``RequestedTags`` option is
available only if you specify ``"Expand": true``::

  $ curl -X POST http://localhost:8042/tools/find -d '
    {
      "Level": "Studies",
      "Expand": true,
      "Query": {
        "StudyDate": "20220502"
      },
      "RequestedTags": ["PatientName", "PatientID", "StudyDescription", "StudyDate", "StudyInstanceUID", "ModalitiesInStudy", "NumberOfStudyRelatedSeries"]
    }'

.. highlight:: json

This query will return a response like this one::

  [
    {
      "ID" : "8a8cf898-ca27c490-d0c7058c-929d0581-2bbf104d",
      "IsStable" : true,
      "LastUpdate" : "20220428T074549",
      "MainDicomTags" : {
        "...":"..."
      },
      "..." : "...",
      "RequestedTags" : {
         "PatientName" : "Patient",
         "PatientID" : "1",
         "StudyDescription" : "Description",
         "StudyDate" : "20220502",
         "StudyInstanceUID" : "1.2.3",
         "ModalitiesInStudy" : "CT\\SEG\\SR",
         "NumberOfStudyRelatedSeries" : "3"
      },
      "Series" : [ "93034833-163e42c3-bc9a428b-194620cf-2c5799e5" ],
      "Type" : "Study"
   }
  ]


.. _changes:

Tracking changes
----------------

.. highlight:: bash

Whenever Orthanc receives a new DICOM instance, this event is recorded
in the so-called "Changes Log". This enables remote scripts to react
to the arrival of new DICOM resources. A typical application is
**auto-routing**, where an external script waits for a new DICOM
instance to arrive into Orthanc, then forward this instance to another
modality.

The Changes Log can be accessed by the following command::

    $ curl http://localhost:8042/changes

.. highlight:: json

Here is a typical output::

 {
   "Changes" : [
      {
         "ChangeType" : "NewInstance",
         "Date" : "20130507T143902",
         "ID" : "8e289db9-0e1437e1-3ecf395f-d8aae463-f4bb49fe",
         "Path" : "/instances/8e289db9-0e1437e1-3ecf395f-d8aae463-f4bb49fe",
         "ResourceType" : "Instance",
         "Seq" : 921
      },
      {
         "ChangeType" : "NewSeries",
         "Date" : "20130507T143902",
         "ID" : "cceb768f-e0f8df71-511b0277-07e55743-9ef8890d",
         "Path" : "/series/cceb768f-e0f8df71-511b0277-07e55743-9ef8890d",
         "ResourceType" : "Series",
         "Seq" : 922
      },
      {
         "ChangeType" : "NewStudy",
         "Date" : "20130507T143902",
         "ID" : "c4ec7f68-9b162055-2c8c5888-5bf5752f-155ab19f",
         "Path" : "/studies/c4ec7f68-9b162055-2c8c5888-5bf5752f-155ab19f",
         "ResourceType" : "Study",
         "Seq" : 923
      },
      {
         "ChangeType" : "NewPatient",
         "Date" : "20130507T143902",
         "ID" : "dc65762c-f476e8b9-898834f4-2f8a5014-2599bc94",
         "Path" : "/patients/dc65762c-f476e8b9-898834f4-2f8a5014-2599bc94",
         "ResourceType" : "Patient",
         "Seq" : 924
      }
   ],
   "Done" : true,
   "Last" : 924
 }

This output corresponds to the receiving of one single DICOM instance
by Orthanc. It records that a new instance, a new series, a new study
and a new patient has been created inside Orthanc. Note that each
changes is labeled by a ``ChangeType``, a ``Date`` (in the `ISO format
<https://en.wikipedia.org/wiki/ISO_8601>`__), the location of the
resource inside Orthanc, and a sequence number (``Seq``).

Note that this call is non-blocking. It is up to the calling program
to wait for the occurrence of a new event (by implementing a polling
loop).

.. highlight:: bash

This call only returns a fixed number of events, that can be changed
by using the ``limit`` option::

    $ curl http://localhost:8042/changes?limit=100

The flag ``Last`` records the sequence number of the lastly returned
event. The flag ``Done`` is set to ``true`` if no further event has
occurred after this lastly returned event. If ``Done`` is set to
``false``, further events are available and can be retrieved. This is
done by setting the ``since`` option that specifies from which
sequence number the changes must be returned::

    $ curl 'http://localhost:8042/changes?limit=100&since=922'

A `sample code in the source distribution
<https://hg.orthanc-server.com/orthanc/file/default/OrthancServer/Resources/Samples/Python/ChangesLoop.py>`__
shows how to use this Changes API to implement a polling loop.


Deleting resources from Orthanc
-------------------------------

.. highlight:: bash

Deleting patients, studies, series or instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deleting DICOM resources (i.e. patients, studies, series or instances)
from Orthanc is as simple as using a HTTP DELETE on the URI of this
resource.

Concretely, you would first explore the resources that are stored in
Orthanc :ref:`as explained above <rest-access>`::

    $ curl http://localhost:8042/patients
    $ curl http://localhost:8042/studies
    $ curl http://localhost:8042/series
    $ curl http://localhost:8042/instances

Secondly, once you have spotted the resources to be removed, you would
use the following command-line syntax to delete them::

    $ curl -X DELETE http://localhost:8042/patients/dc65762c-f476e8b9-898834f4-2f8a5014-2599bc94
    $ curl -X DELETE http://localhost:8042/studies/c4ec7f68-9b162055-2c8c5888-5bf5752f-155ab19f
    $ curl -X DELETE http://localhost:8042/series/cceb768f-e0f8df71-511b0277-07e55743-9ef8890d
    $ curl -X DELETE http://localhost:8042/instances/8e289db9-0e1437e1-3ecf395f-d8aae463-f4bb49fe


Starting with Orthanc 1.9.4, it is also possible to ``POST`` on the
new route ``/tools/bulk-delete`` to delete at once a set of multiple
DICOM resources that are not related (i.e. that don't share any parent
DICOM resource). A typical use case is to delete a list of DICOM
instances that don't belong to the same parent patient/study/series.
The list of the :ref:`Orthanc identifiers <orthanc-ids>` of the
resources to be deleted (that may indifferently correspond to
patients, studies, series or instances) must be provided in an
argument ``Resources`` in the body of the request. Here is a sample
call::

  $ curl http://localhost:8042/tools/bulk-delete -d '{"Resources":["b6da0b16-a25ae9e7-1a80fc33-20df01a9-a6f7a1b0","d6634d97-24379e4a-1e68d3af-e6d0451f-e7bcd3d1"]}'

    
Clearing log of changes
^^^^^^^^^^^^^^^^^^^^^^^

:ref:`As described above <changes>`, Orthanc keeps track of all the
changes that occur in the DICOM store. This so-called "Changes Log"
is accessible at the following URI::

    $ curl http://localhost:8042/changes

To clear the content of the Changes Log, simply DELETE this URI::

    $ curl -X DELETE http://localhost:8042/changes


Log of exported resources
^^^^^^^^^^^^^^^^^^^^^^^^^

For medical traceability, Orthanc can be configured to store a log of
all the resources that have been exported to remote modalities::

    $ curl http://localhost:8042/exports

In auto-routing scenarios, it is important to prevent this log to grow
indefinitely as incoming instances are routed. You can either disable
this logging by setting the option ``LogExportedResources`` to ``false``
in the :ref:`configuration file <configuration>`, or periodically
clear this log by DELETE-ing this URI::

    $ curl -X DELETE http://localhost:8042/exports

NB: Starting with Orthanc 1.4.0, the ``LogExportedResources`` is set
to ``false`` by default. If the logging is desired, set this option to
``true``.
    

Anonymization and modification
------------------------------

The process of anonymizing and modifying DICOM resources is
:ref:`documented in a separate page <anonymization>`.


Further reading
---------------

The examples above have shown you the basic principles for driving an
instance of Orthanc through its REST API. All the possibilities of the
API have not been described:

* Advanced features of the REST API can be found on :ref:`another page
  <rest-advanced>`.
* A :ref:`FAQ entry <rest-samples>` lists where you can find more
  advanced samples of the REST API of Orthanc.
* A :ref:`short reference of the REST API of Orthanc <cheatsheet>` is
  part of the Orthanc Book.
* The full documentation of the REST API in the OpenAPI/Swagger format
  is `available online <https://api.orthanc-server.com/>`__. This
  reference is automatically generated from the source code of
  Orthanc.
