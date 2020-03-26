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
was needed for Orthanc, and that both Git and Mercurial have similar
set of features.

If Orthanc were started in 2020, maybe we would have used Git, or
maybe not. But the Orthanc ecosystem is not about versioning
systems. We are entirely dedicated to lowering barriers to entry in
the field of medical imaging. As a consequence, the choice of
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

Read-only access
^^^^^^^^^^^^^^^^

Anybody has full read-only access to all of the Orthanc official
repositories, on our `self-hosted server
<https://hg.orthanc-server.com/>`__.

.. highlight:: bash

Locally cloning one of those Mercurial repositories (say, the main
``orthanc`` repository) is as simple as typing::

  $ hg clone https://hg.orthanc-server.com/orthanc


Write access
^^^^^^^^^^^^

Only the core developers of Orthanc have direct write access to the
Orthanc repositories (through SSH).


Submitting code
^^^^^^^^^^^^^^^

We will of course be extremely grateful for receiving external code
contributions to the Orthanc repositories!

However, one of the weaknesses of our self-hosted infrastructure is
that is does not support automation for `pull requests
<https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests>`__.
This section explains two ways of contributing: by submitting a patch,
or by providing a branch.

Importantly, before any contribution can be accepted into the Orthanc
repositories, its author must sign a :ref:`CLA <cla>`. This allows
both the University Hospital of Liège and the Osimis company to act as
the official guardians of the whole Orthanc ecosystem.


Simple patch
............

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



Submitting a set of changes
...........................

Work-in-progress.



Issue tracker
-------------

This is work-in-progress. Orthanc will most probably move to the
`Roundup issue tracker
<https://en.wikipedia.org/wiki/Roundup_(issue_tracker)>`__ that is
notably used by the Python community.
