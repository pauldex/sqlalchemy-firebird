sqlalchemy-firebird
===================
An external SQLAlchemy dialect for Firebird
-------------------------------------------
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

| This replaces SQLAlchemy's internal Firebird dialect which is not being
| maintained and will be removed in a future version.
|

Installation:

::

    pip install sqlalchemy-firebird

Sample connection URI:

::

    firebird://sysdba:scott_tiger@localhost//home/paul/databases/sqla_test.fdb

