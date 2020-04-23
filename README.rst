sqlalchemy-firebird
===================
An external SQLAlchemy dialect for Firebird
-------------------------------------------
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

| This will replace SQLAlchemy's internal Firebird dialect which is not being maintained.
|

Sample connection URI:

::

    firebird://sysdba:scott_tiger@localhost//home/gord/git/sqlalchemy-firebird/sqla_test.fdb

The dialect identifier is currently "firebird" to avoid conflicts with
the internal dialect. Eventually both ``firebird://`` and
``firebird://`` will be equivalent.
