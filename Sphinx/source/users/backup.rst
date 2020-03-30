.. _backup:

Backup
======

The way to backup Orthanc depends on the database back-end that is
used. In any case, you of course have to backup your
:ref:`configuration file <configuration>`.

SQLite
------

By default, Orthanc uses SQLite to store its database. In this case,
all the DICOM files together with the SQLite index are stored directly
in the filesystem. The backup procedure works as follows:

1. Stop Orthanc.
2. Copy the following 3 elements:

   * Your configuration file.
   * The DICOM files (by default, the subdirectories of the
     ``OrthancStorage`` folder next to the configuration file).
   * The SQLite index (by default, the ``OrthancStorage/index*`` files
     next to the configuration file).

3. Restart Orthanc.

It is mandatory to stop Orthanc, as the Orthanc core makes the
assumption that it is the only process to access the SQLite database
at any time.

Karsten Hilbert provided us with a `sample backup script
<https://github.com/jodogne/OrthancContributed/blob/master/Scripts/Backup/2014-01-31-KarstenHilbert.sh>`__
for the official Debian package of Orthanc that automates this backup
procedure. Note that in this script, the call to the SQLite
command-line tool is used to force the `WAL replay
<https://www.sqlite.org/wal.html>`__. This manual replay should not be
necessary for Orthanc >= 0.7.3.


PostgreSQL and MySQL
--------------------

The default SQLite engine is well adapted for DICOM routing or for
image buffering tasks, but not for enterprise scenarios. In such
cases, you are highly recommended to use the `PostgreSQL back-end
<https://www.orthanc-server.com/static.php?page=postgresql>`__ or the
`MySQL/MariaDB back-end
<https://www.orthanc-server.com/static.php?page=mysql>`__.

If using PostgreSQL, you can do hot backups (i.e. while Orthanc is
running), and you benefit from all the flexibility of PostgreSQL
backup. These procedures are out of the scope of this manual.  Please
check the `official backup and restore manual
<https://www.postgresql.org/docs/devel/backup.html>`__.

Similar backup procedures are available for MySQL and MariaDB as
well. Please check the official manual about `database backup methods
<https://dev.mysql.com/doc/refman/8.0/en/backup-methods.html>`__.

Here are some contributed documents:

* `Backup for Windows 10, Orthanc and PostgreSQL plugin <https://blog.goo.ne.jp/wakida_ortho/e/3eb557fd134cf6136d5ba66cf72fd85a>`__ (in Japanese, 2020-02-02).
