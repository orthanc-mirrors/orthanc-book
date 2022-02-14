.. _videos:

Does Orthanc support videos?
============================

The answer to this question really depends on what you mean by
"support" and "video":

* In the world of DICOM, a "video" can either refer to a 2D+t (aka. a
  "cine" sequence of individual frames) or a real video (compressed
  using H.264 or MPEG2). For instance, ultrasound devices would
  generate cine sequences, whereas recent endoscopes would generate
  real videos.
* Depending on the context, "support" can mean "*Is Orthanc able to
  query/receive/transfer DICOM files?*", or "*Is Orthanc able to
  render/play DICOM files?*".

If you "just" want to **query/receive/transfer** DICOM videos, Orthanc
will work fine either with 2D+t or real videos (because Orthanc is a
`Vendor Neutral Archive
<https://en.wikipedia.org/wiki/Vendor_Neutral_Archive>`__). This
distinction is also discussed in :ref:`another FAQ entry
<supported-images>`.

It is easy to **extract and download** the raw video embedded in the
DICOM instance using the :ref:`REST API of Orthanc
<download-pdf-videos>`.

If you also want to **play** the videos, the :ref:`Osimis Web Viewer
plugin <osimis_webviewer>` is able to play H.264 (MPEG4) videos and
2D+t (cine) sequences but not MPEG2 videos that currently can not be
played by Web browsers.

If your video is a 2D+t (cine) sequence, Orthanc can also display it inside 
a Web browser by at least 2 different means:

1. The built-in, administrative interface called :ref:`Orthanc
   Explorer <orthanc-explorer>` is able to display the individual
   frames and manually navigate between them through keyboard.
2. The official `Web viewer plugin
   <https://www.orthanc-server.com/static.php?page=web-viewer>`__ will
   allow you to use the mouse scroll wheel to display the successive
   frames of the video.

To summarize, if your video is not encoded with MPEG2, OR if
you do not need to play the video within a Web browser, Orthanc
actually supports video if the Osimis Web viewer plugin is installed.
