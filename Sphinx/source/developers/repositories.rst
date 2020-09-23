.. _repositories:

Accessing code repositories
===========================

.. contents::

   
Context
-------

The Orthanc server and most of its plugins are versioned using
`Mercurial <https://en.wikipedia.org/wiki/Mercurial>`__ on a
`self-hosted server <https://hg.orthanc-server.com/>`__.

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
<https://hg.orthanc-server.com/>`__. As the ``hg serve`` tool that is
used by our Web server tends to be slow, we recommend people to
locally clone our Mercurial repositories.

.. highlight:: bash

Locally cloning one of those Mercurial repositories (say, the main
``orthanc`` repository) is as simple as typing::

  $ hg clone https://hg.orthanc-server.com/orthanc/

You can then use separate tools such as `TortoiseHg
<https://en.wikipedia.org/wiki/TortoiseHg>`__ to browse the code with
richer features than the Web interface.

.. highlight:: text

You might have to set up a host fingerprint in the Mercurial
configuration. Add the following lines to your ``~/.hgrc`` file::

  [hostfingerprints]
  hg.orthanc-server.com = 1B:29:E6:DE:95:7B:6B:21:59:2C:0E:C4:85:B9:64:C9:08:84:9B:98
  
.. highlight:: bash

For reference, here is the command that was used to generate this SHA1
fingerprint (`click here for more information
<https://wiki.fluidproject.org/display/fluid/Setting+Host+Fingerprints+for+Mercurial>`__)::

  $ openssl s_client -connect hg.orthanc-server.com:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha1 -noout -in /dev/stdin

**Important:** As our certificates are changed periodically, you'll
have to regularly update your configuration file once Mercurial
complains about an unexpected fingerprint.


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
  hg.orthanc-server.com:fingerprints=sha256:6A:D9:B8:88:C2:96:F1:00:B1:5E:CF:80:BB:CC:23:C5:73:18:D1:7C:7A:7B:10:3E:62:1B:08:87:42:F1:1E:BF
  
.. highlight:: bash

For reference, here is the command that was used to generate this
SHA256 fingerprint (`click here for more information
<https://stackoverflow.com/a/56579497/881731>`__)::

  $ openssl s_client -connect hg.orthanc-server.com:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha256 -noout -in /dev/stdin
  

Write access
^^^^^^^^^^^^

Only the core developers of Orthanc have direct write access to the
Orthanc repositories (through SSH). Core developers can clone a
repository with write access as follows::

  $ hg clone ssh://hg@hg.orthanc-server.com/public/orthanc/


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

Importantly, before any contribution can be accepted into the Orthanc
repositories, its author must sign a :ref:`CLA <cla>`. This allows
both the University Hospital of Liège and the Osimis company to act as
the official guardians of the whole Orthanc ecosystem.

Also, make sure to read our :ref:`FAQ if submitting code
<submitting_code>`.


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
`discussion group
<https://groups.google.com/forum/#!forum/orthanc-users>`__. The core
developers would reintegrate such a patch by typing the following
command on their side::

  $ hg pull
  $ hg up -c default
  $ hg import /tmp/contribution.patch


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
  $ hg bundle /tmp/contribution.bundle https://hg.orthanc-server.com/orthanc

Obviously, make sure to replace
``https://hg.orthanc-server.com/orthanc`` by the location of the
source repository.

Finally, you can submit the file ``/tmp/contribution.bundle`` to the
community, just like for simple patches. Note that this procedure
inherently corresponds to the manual creation of a pull request.

The core developers would reintegrate such a bundle into the mainline
by typing the following commands on their side::

  $ cd /tmp
  $ hg clone https://hg.orthanc-server.com/orthanc/
  $ cd /tmp/orthanc
  $ hg unbundle /tmp/contribution.bundle
  $ hg up -c default
  $ hg merge my-user/my-fix
  

Issue tracker
-------------

The `official bug tracker <https://bugs.orthanc-server.com/>`__ of the
Orthanc project runs thanks to `Bugzilla
<https://en.wikipedia.org/wiki/Bugzilla>`__.

We have done our best to automatically import most of the history
from the old BitBucket bug tracker.

Before posting any issue, make sure to carefully, completely read the
:ref:`page about how to ask support <support>`. In particular, most
issues should first be discussed on the dedicated `discussion group
<https://groups.google.com/forum/#!forum/orthanc-users>`__ before
introducing a bug report.
