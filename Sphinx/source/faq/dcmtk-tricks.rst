.. _dcmtk-tricks:

Some tricks with DCMTK
======================

.. contents::
   :depth: 3

Sending uncommon or recent SOP class UIDs
-----------------------------------------

On many systems, the ``storescu`` command from the `DCMTK project
<https://support.dcmtk.org/docs/storescu.html>`__ is not configured
out-of-the-box to send uncommon/recent SOP class UIDs or transfer
syntaxes. You might have to fine-tune the default configuration file
of ``storescu`` in order to be able to send e.g. MPEG4 videos or
breast tomosynthesis images.

.. highlight:: text
               
For instance, here is the result of sending one MPEG4 video on a
Ubuntu 18.04 box::

  $ storescu localhost 4242 XC000000.dcm 
  E: No presentation context for: (VVp) 1.2.840.10008.5.1.4.1.1.77.1.4.1
  E: Store SCU Failed: 0006:0208 DIMSE No valid Presentation Context ID

This error message is unrelated to Orthanc (especially if you have set
the :ref:`configuration option <configuration>`
``UnknownSopClassAccepted`` to ``true``). To properly adapt the
configuration file, first determine the DICOM tag ``SOPClassUID`` ()
and the transfer syntax of the file, which can be done by using the
``dcm2xml`` command-line tool::

  $ dcm2xml XC000000.dcm | grep -E 'data-set xfer|"SOPClassUID"'
  <data-set xfer="1.2.840.10008.1.2.4.102" name="MPEG-4 AVC/H.264 High Profile / Level 4.1">
  <element tag="0008,0016" vr="UI" vm="1" len="32" name="SOPClassUID">1.2.840.10008.5.1.4.1.1.77.1.4.1</element>

Secondly, create a copy of the default ``storescu.cfg`` configuration
file, e.g. on Ubuntu 18.04::

  $ cp /etc/dcmtk/storescu.cfg /tmp/storescu.cfg

Edit this file so as to replace one of the 128 preconfigured
presentation contexts, using this information::

  $ diff /etc/dcmtk/storescu.cfg storescu.cfg 
  198c198
  < PresentationContext128 = VideoPhotographicImageStorage\MPEG2
  ---
  > PresentationContext128 = 1.2.840.10008.5.1.4.1.1.77.1.4.1\MPEG4

Obviously, you can replace more predefinitions if other pairs of SOP
class UID and transfer syntax are needed. Finally, run ``storescu``
using this new configuration::

  $ storescu -xf /tmp/storescu.cfg Default localhost 4242 XC000000.dcm
  
Note that the ``storescu`` command from the `dcm4che project
<https://www.dcm4che.org/>`__ might be more easy to use in such
situations.
