Why your contribution may not be accepted ?
===========================================

Nowadays, with a little help from a LLM, anyone is able to contribute to open-source.  
Therefore, maintainers receive a lot of contributions from users who want a specific feature to be implemented.  

LLMs are able to write the code, document the feature, and even add some tests so why would 
the maintainer not accept the contributions ?  After all, accepting the contribution would only require 5 minutes of the maintainer's time right ?

Not quite.

1. A new feature extends the scope of the software and therefore increases the maintenance workload; 
   not only when the feature is added but possibly for the next 20 or 30 years so the maintainer 
   usually wants to make sure the feature is really useful to a majority of users; not just to a single user.
2. Even when a contribution seems to do the job, that does not make it the ideal implementation.  
   The maintainer needs to deeply understand each part of the contribution to make sure it does not break 
   another feature or make the code harder to maintain in the future.  
   Reviewing code, especially code that looks correct, often takes more time than writing it.  This can easily require hours of work.
3. Orthanc is maintained by Sébastien Jodogne, who is already very busy with his main job as a university professor 
   and by `Orthanc Team <https://orthanc.team/>`__ that is a very small company with only 2 people who have decided to 
   share their work; which does not mean they work for free.

So, don't be surprised if we don't accept your contribution or if we ask you to fund its integration e.g. by `purchasing a support contract <https://orthanc.team/>`__.  
What you see as 5 minutes of work is very likely a few hours work now, and dozens of hours over the long term.

If you would like a feature to be integrated, the best approach is to start a thread in the `user's forum <https://discourse.orthanc-server.org/>`__ first 
and discuss it with us before writing any code. Alternatively, consider `funding the development <https://opencollective.com/orthanc>`__: this is what keeps Orthanc alive.