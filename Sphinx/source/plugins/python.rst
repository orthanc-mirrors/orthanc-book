.. _python-plugin:


Python plugin for Orthanc
=========================

.. contents::

Work-in-progress.



Samples
-------

Extending the REST API
......................

.. highlight:: python

Here is a basic Python script that registers two new routes in the
REST API::

  import orthanc
  import pprint

  def OnRest(output, uri, **request):
      pprint.pprint(request)
      print('Accessing uri: %s' % uri)
      output.AnswerBuffer('ok\n', 'text/plain')
    
  orthanc.RegisterRestCallback('/(to)(t)o', OnRest)
  orthanc.RegisterRestCallback('/tata', OnRest)

.. highlight:: json

Here is the associated minimal configuration file for Orthanc
(provided the Python script is saved as ``rest.py``)::

  {
    "Plugins" : [ "." ],
    "PythonScript" : "rest.py",
    "PythonVerbose" : false
  }

.. highlight:: bash

The route can then be accessed as::

  $ curl http://localhost:8042/toto
  ok

