.. _coding-style:
.. highlight:: c++

Coding style
============

.. contents::

The developers of Orthanc should follow these `C++ Programming Style
Guidelines <http://geosoft.no/development/cppstyle.html>`__, that are
similar to the so-called "`BSD/Allman style
<https://en.wikipedia.org/wiki/Indent_style#Allman_style>`__", with
some adaptations that are described below. A compliant Eclipse
formatter is `available in the Orthanc distribution
<https://hg.orthanc-server.com/orthanc/file/default/OrthancFramework/Resources/Graveyard/EclipseCodingStyle.xml>`__ (not maintained anymore).

Licensing
---------

Do not forget to include licensing information (GPLv3 with OpenSSL
exception) in each ``.cpp`` and ``.h``.

Tabulations
-----------

No tab characters. Replace 1 tab by 2 spaces.

Strengthened Rules
------------------

* Rule 31: Use ``COLOR_RED`` instead of ``Color::RED``
* Rule 34: Use the suffix ``.cpp``
* Rule 35: A single header file must contain a single public class
* Rule 72: Use the Example 2 style (aka. Allman style, used by MSDN
  and Visual Studio)::

    while (!done)
    {
      doSomething();
      done = moreToDo();
    }


Replaced Rules
--------------

* Rule 6: The names of the methods are camel-case to move the coding style closer to that of the .NET framework.
* Rule 36:

  * One-liners are always ok in a ``.h``,
  * High-performance code is also allowed but only with the inline
    keyword (the code being moved at the end of the header)

* Rule 40: Use ``#pragma once`` in each header file (cf. `Wikipedia
  <https://en.wikipedia.org/wiki/Pragma_once>`__)
* Rules 73 and 80: Use Visual Studio's default style that does not add
  two whitespaces in front of public, protected, private and case::

    class SomeClass : public BaseClass
    {
    public:
      ...
    protected:
      ...
    private:
      ...
    };


Additional Rules
----------------

* Use C++ exceptions, avoid error codes.
* Use the `RAII design pattern <https://en.wikipedia.org/wiki/RAII>`__ (Resource Allocation Is Initialization) wherever possible.
* No C-style casting, use ``static_cast``, ``reinterpret_cast``,
  ``dynamic_cast`` and ``const_cast``.
* Never use ``using namespace`` in header files (except inside inline
  implementations).
* Complement to rule 20: ``Finalize`` is the complementary word to
  ``Initialize``.
* Minimize the number of #include in header files.
* Never use ``catch (...)``, except when protecting non-Orthanc code.
* To ease unit testing, favor the `JavaBeans
  <https://en.wikipedia.org/wiki/Java_beans>`__ conventions:

  * Single constructor without argument,
  * Use getters/setters.


Conventions for pointers and references
---------------------------------------

Except when clearly stated in the documentation:

* A function that receives a **reference** to an object as an argument
  is not responsible for the lifecycle of the object, and must not
  ``delete`` it. The object is allowed to keep this reference in a
  member variable. The caller must ensure that the referenced object
  will not be freed between the object that references it.
* A function that receives a **pointer** to an object as an argument
  takes the ownership of the object.
* A function that returns a **reference** to an object indicates that
  the object should not be freed by the caller.
* A function that returns a **pointer** to an object transfers its
  ownership to the caller. Occasionally, a pointer is also returned to
  indicate the presence or the absence (represented by ``NULL``) of
  some resource: In such a case, the pointer must not be freed.
