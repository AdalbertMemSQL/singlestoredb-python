
What's New
==========

This document outlines features and improvements from each release.

.. note:: All releases before v1.0.0 are considered pre-release and
   are for non-production testing and evaluation, and may include
   changes to the API.

v0.5.3 - January 9, 2023
--------------------------
* Fixed issue with parsing numeric results

v0.5.2 - December 14, 2022
--------------------------
* Fixed issues with unbuffered reads

v0.5.1 - December 9, 2022
-------------------------
* Added 32-bit Windows and aarch64 Linux packages
* Added option to log queries

v0.5.0 - December 8, 2022 (**API CHANGES**)
-------------------------------------------
* ! Query parameter syntax has changed from ``:1`` for positional
  and ``:key`` for dictionary keys to ``%s`` for positional and ``%(key)s``
  for dictionary keys
* ! ``results_format`` connection parameter has changed to ``results_type``
* High-performance C extension added
* Added ``ssl_verify_cert`` and ``ssl_verify_identity`` connection options
* Add Python 3.11 support

v0.4.0 - October 19, 2022
-------------------------
* Add Python 3.6 support

v0.3.3 - September 21, 2022
---------------------------
* Add ``ssl_cipher`` option to connections
* Add ``show`` accessor for database ``SHOW`` commands

v0.3.2 - September 14, 2022
---------------------------
* Fixes for PyMySQL compatibility

v0.3.1 - September 9, 2022
--------------------------
* Changed cipher in PyMySQL connection for SingleStoreDB Cloud compatibility

v0.3.0 - September 9, 2022
--------------------------
* Changed autocommit=True by default

v0.2.0 - August 5, 2022
-----------------------
* Changed to pure Python driver
* Add workspace management objects
* Added ``auth.get_jwt`` function for retrieving JWTs

v0.1.0 - May 6, 2022
--------------------
* DB-API compliant connections
* HTTP API support
* Cluster manager interface
