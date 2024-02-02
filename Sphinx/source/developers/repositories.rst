.. _repositories:

Accessing code repositories
===========================

.. contents::

   
Context
-------

The Orthanc server and most of its plugins are versioned using
`Mercurial <https://en.wikipedia.org/wiki/Mercurial>`__ on a
`self-hosted server <https://orthanc.uclouvain.be/hg/>`__.

The Orthanc project started back in 2011, back in a time where
Mercurial and `Git <https://en.wikipedia.org/wiki/Git>`__ were equally
popular. Sébastien Jodogne, the original author of Orthanc, decided to
use Mercurial given the higher simplicity of its set of commands, and
given the fact it is safer to use for less experienced users.

As pointed out on `Wikipedia
<https://en.wikipedia.org/wiki/Mercurial>`__, the *"Git vs. Mercurial
[debate] has become one of the holy wars of hacker culture."* We
certainly don't want to endure this debate in the context of the
Orthanc ecosystem.  The fact is that a distributed revision-control
was needed for Orthanc, and that both Git and Mercurial have a similar
set of features.

If Orthanc were started in 2020, maybe we would have used Git, or
maybe not. But the Orthanc ecosystem is not at all about versioning
systems. We want to be entirely dedicated to lowering barriers to
entry in the field of medical imaging. As a consequence, the choice of
Mercurial should be considered as a part of the history, and we simply
ask people to accept it as a fact.

Regarding the reason behind self-hosting, Orthanc was hosted on
`Google Code
<https://en.wikipedia.org/wiki/Google_Developers#Google_Code>`__
between 2012 and 2015, until it was shutdown. In July 2015, Orthanc
was moved to `Bitbucket by Atlassian
<https://en.wikipedia.org/wiki/Bitbucket>`__.  Unfortunately, in July
2019, Bitbucket announced that `Mercurial support would be dropped on
June 2020
<https://bitbucket.org/blog/sunsetting-mercurial-support-in-bitbucket>`__,
forcing us to deal with another migration.

We are of course grateful to Google and Atlassian for having hosted
Orthanc during 8 years. However, we cannot afford the cost of
periodically coping with hosting migrations. We prefer to have a
simpler environment, yet under our full control. As a consequence,
starting Q2 2020, Orthanc is hosted using the official ``hg serve``
tool.


Accessing Mercurial
-------------------

.. _hg-clone:

Read-only access
^^^^^^^^^^^^^^^^

Anybody has full read-only access to all of the Orthanc official
repositories, on our `self-hosted server
<https://orthanc.uclouvain.be/hg/>`__. As the ``hg serve`` tool that is
used by our Web server tends to be slow, we recommend people to
locally clone our Mercurial repositories.

.. highlight:: bash

Locally cloning one of those Mercurial repositories (say, the main
``orthanc`` repository) is as simple as typing::

  $ hg clone https://orthanc.uclouvain.be/hg/orthanc/

You can then use separate tools such as `TortoiseHg
<https://en.wikipedia.org/wiki/TortoiseHg>`__ to browse the code with
richer features than the Web interface.


Recent versions of Mercurial
............................

.. highlight:: text

While cloning the repository, you might face an error similar to::

  abort: error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)

In such a case, you must explicitly add the cryptographic fingerprint
of our code server using a more recent option than the
``hostfingerprints`` option. To this end, edit the `configuration file
<https://www.mercurial-scm.org/doc/hgrc.5.html#files>`__ of Mercurial
(by default on Microsoft Windows, ``%USERPROFILE%\Mercurial.ini``),
and add the following lines::

  [hostsecurity]
  orthanc.uclouvain.be:fingerprints=sha256:30:1d:d8:b6:a2:50:23:6a:a1:b7:da:66:b6:aa:2f:fa:59:f3:9d:cd:ed:f8:2c:49:14:57:25:39:84:b9:60:db
  
.. highlight:: bash

For reference, here is the command that was used to generate this
SHA256 fingerprint (`click here for more information
<https://stackoverflow.com/a/56579497/881731>`__)::

  $ openssl s_client -servername orthanc.uclouvain.be -connect orthanc.uclouvain.be:443 \
    < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha256 -noout -in /dev/stdin
  
**Important:** As our certificates are changed periodically, you'll
have to regularly update your configuration file once Mercurial
complains about an unexpected fingerprint.


Old versions of Mercurial
^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: text

For old versions of Mercurial that do not support SHA256, add the
following lines to your ``~/.hgrc`` file::

  [hostfingerprints]
  orthanc.uclouvain.be = 69:C0:EF:E7:05:BB:2A:0B:88:EA:E8:00:C6:1A:95:A3:53:74:C1:D4

.. highlight:: bash

For reference, here is the command that was used to generate this SHA1
fingerprint (`click here for more information
<https://wiki.fluidproject.org/display/fluid/Setting+Host+Fingerprints+for+Mercurial>`__)::

  $ openssl s_client -servername orthanc.uclouvain.be -connect orthanc.uclouvain.be:443 \
    < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha1 -noout -in /dev/stdin


Write access
^^^^^^^^^^^^

Only the core developers of Orthanc have direct write access to the
Orthanc repositories (through SSH). Core developers can clone a
repository with write access as follows::

  $ hg clone ssh://hg@orthanc.uclouvain.be/public/orthanc/


.. _hg-contributing:

Submitting code
^^^^^^^^^^^^^^^

We will of course be extremely grateful for receiving external code
contributions to the Orthanc repositories!

However, one of the weaknesses of our self-hosted infrastructure is
that is does not support automation for `pull requests
<https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests>`__.
This section explains the `two accepted ways for communicating
contributions
<https://www.mercurial-scm.org/wiki/CommunicatingChanges>`__: by
submitting a patch, or by exchanging a bundle.


Code quality
............

* Your code **must follow the C++03 standard** (C++11 is not accepted
  for maximum cross-platform compatibility on older platforms).

* The continuous integration servers at UCLouvain check that Orthanc
  properly compiles on Ubuntu 16.04, on `Linux Standard Base systems
  <https://refspecs.linuxfoundation.org/lsb.shtml>`__ using the `LSB
  SDB 5.0.0
  <http://ftp.linuxfoundation.org/pub/lsb/bundles/released-5.0.0/sdk/>`__,
  on FreeBSD, on Microsoft Visual Studio 2008 (32 bit), on Microsoft
  Visual Studio 2015 (64 bit), and on Apple OS X 10.9
  "Mavericks". Submitted code might have to be adapted to compile on
  these platforms. Architecture-dependant code should be located in
  the `Orthanc::Toolbox
  <https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancFramework/Sources/Toolbox.h>`__
  and `Orthanc::SystemToolbox
  <https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancFramework/Sources/SystemToolbox.h>`__
  static classes.

* Please stick to the :ref:`coding style <coding-style>` of Orthanc.

* Your individual contributions should be kept **as small as
  possible**, and should be focused on one very specific issue or
  feature. Large architectural changes are reserved for the core
  development team of Orthanc, as we must follow our `long-term
  roadmap
  <https://orthanc.uclouvain.be/hg/orthanc/file/default/TODO>`__.

* Unit testing is mandatory. Integration tests should be submitted to
  the `dedicated repository
  <https://orthanc.uclouvain.be/hg/orthanc-tests/file/default>`__.

* All the contributions will be carefully reviewed. Some contributions
  may be modified, yet even rejected. A rejection might for instance
  occur if your contribution does not match the Orthanc roadmap, does
  not meet our high-quality code standards, or breaks backward
  compatibility. Please be sure that we warmly welcome and appreciate
  your contributions, but be aware of the fact that we are quite
  strict, and that the review process might take time. This is why the
  recommended way of contributing to Orthanc is always by
  :ref:`creating contributed plugins <creating-plugins>`.

* If intellectual property is of importance to you, make sure to
  carefully read our :ref:`FAQ about the licensing of submitted code
  <submitting_code>`. If you are concerned about intellectual
  property, consider creating plugins instead of submitting code
  directly to the core project.


.. _hg-patch:

Simple patch (import/export)
............................

.. highlight:: bash
             
If you want to propose a simple contribution, the most direct way of
passing it on the Orthanc community is by creating a **simple patch**.

First make sure to pull the latest version of the code repository,
then work on your modification in the ``default`` branch (i.e. in the
mainline code)::

  $ hg pull
  $ hg up -c default
  [...make your modifications...]

Once your contribution is done, here is how to export a patch::

  $ hg export -r default > /tmp/contribution.patch

Once the patch is ready, you can send the ``/tmp/contribution.patch``
file to the Orthanc community, e.g. by submitting it onto our official
`Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__. The core
developers would reintegrate such a patch by typing the following
command on their side::

  $ hg pull
  $ hg up -c default
  $ hg import /tmp/contribution.patch

NB: If the ``hg export`` command was run on Microsoft Windows, one
might have to convert the end-of-lines from DOS (CR/LF) to UNIX (LF
only) using the ``dos2unix`` command on the patch file, before running
``hg import``.  Otherwise, errors like ``Hunk #1 FAILED`` might show
up.

  
.. _hg-bundle:

Exchanging a bundle
...................

.. highlight:: bash
             
If your contribution is made of several changesets (commits), you
should work in a dedicated branch, then submit a Mercurial bundle for
this branch.

First make sure to pull the latest version of the code repository,
then create a branch, say ``my-user/my-fix``, that derives from the
``default`` branch (which corresponds to the mainline code)::

  $ hg pull
  $ hg up -c default
  $ hg branch my-user/my-fix

WARNING: Please chose an unique, explicit name for your branch, and
make sure that your username is included within for traceability! The
name ``my-user/my-fix`` is only here for the purpose of the example.
  
You can then do all the modifications as required (including ``hg
add``, ``hg rm``, and ``hg commit``) in the branch
``my-user/my-fix``. When you're done, create a Mercurial bundle that
gathers all your changes against the source repository as follows::

  $ hg commit -m 'submitting my fix'
  $ hg bundle /tmp/contribution.bundle https://orthanc.uclouvain.be/hg/orthanc

Obviously, make sure to replace
``https://orthanc.uclouvain.be/hg/orthanc`` by the location of the
source repository.

Finally, you can submit the file ``/tmp/contribution.bundle`` to the
community, just like for simple patches. Note that this procedure
inherently corresponds to the manual creation of a pull request.

The core developers would reintegrate such a bundle into the mainline
by typing the following commands on their side::

  $ cd /tmp
  $ hg clone https://orthanc.uclouvain.be/hg/orthanc/
  $ cd /tmp/orthanc
  $ hg unbundle /tmp/contribution.bundle
  $ hg up -c default
  $ hg merge my-user/my-fix


.. _hg-submitting:

Submitting contributions
........................

Contributed patches and bundles must be sent by e-mail, either to
`Sébastien Jodogne <mailto:sebastien.jodogne@uclouvain.be>`__
(UCLouvain) or to `Alain Mazy <mailto:am@orthanc.team>`__ (Orthanc
Team).
  

Issue tracker
-------------

The `official bug tracker <https://orthanc.uclouvain.be/bugs/>`__ of the
Orthanc project runs thanks to `Bugzilla
<https://en.wikipedia.org/wiki/Bugzilla>`__.

We have done our best to automatically import most of the history
from the old BitBucket bug tracker.

Before posting any issue, make sure to carefully, completely read the
:ref:`page about how to ask support <support>`. In particular, most
issues should first be discussed on the dedicated `Orthanc Users discussion forum
<https://discourse.orthanc-server.org>`__ before
introducing a bug report.
