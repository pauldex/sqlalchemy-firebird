sqlalchemy-firebird
###################

An external SQLAlchemy dialect for Firebird
===========================================
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. image:: https://github.com/pauldex/sqlalchemy-firebird/workflows/sqlalchemy-firebird/badge.svg
    :target: https://github.com/pauldex/sqlalchemy-firebird

----

| This package provides a `Firebird <https://firebirdsql.org/en/start/>`_ dialect for `SQLAlchemy <https://www.sqlalchemy.org>`_ using the `firebird-driver <https://firebird-driver.readthedocs.io/en/latest>`_ and/or `fdb <https://fdb.readthedocs.io/en/latest>`_ driver.

****

**Installation**

::

    pip install sqlalchemy-firebird

If you are using Python 3.8 or greater, SQLAlchemy 2.0+ and firebird-driver will be automatically installed.
Python 3.6 and 3.7 will automatically install and use SQLAlchemy < 2.0 and fdb instead.

Connection URI samples for Firebird server installed on local machine using default port (3050):

::

    [Linux]
    # Use the fdb driver (Python 3.6/3.7)
    firebird+fdb://username:password@localhost///home/testuser/projects/databases/my_project.fdb
    # Use the firebird-driver driver (Python 3.8+)
    firebird+firebird://username:password@localhost///home/testuser/projects/databases/my_project.fdb

    [Windows]
    # Use the fdb driver (Python 3.6/3.7)
    firebird+fdb://username:password@localhost/c:/projects/databases/my_project.fdb
    # Use the firebird-driver driver (Python 3.8+)
    firebird+firebird://username:password@localhost/c:/projects/databases/my_project.fdb

****

**Usage**

For example, to connect to a Firebird server installed on a local Windows machine using the default port and firebird-driver:

::

    db_uri = "firebird+firebird://username:password@localhost/c:/projects/databases/my_project.fdb"
    from sqlalchemy import create_engine
    engine = create_engine(db_uri, echo=True)

Connecting to different types of Firebird servers, databases, or drivers is done simply by changing the db_uri string
used in the call to create_engine.

----

**Code of Conduct**

As with SQLAlchemy, sqlalchemy-firebird places great emphasis on polite, thoughtful, and
constructive communication between users and developers.
We use the SQLAlchemy `Code of Conduct <http://www.sqlalchemy.org/codeofconduct.html>`_.

----

**License**

sqlalchemy-firebird is distributed under the `MIT license
<http://www.opensource.org/licenses/mit-license.php>`_.
