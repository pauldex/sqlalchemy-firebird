sqlalchemy-firebird
###################

An external SQLAlchemy dialect for Firebird
===========================================
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. image:: https://github.com/pauldex/sqlalchemy-firebird/workflows/sqlalchemy-firebird/badge.svg
    :target: https://github.com/pauldex/sqlalchemy-firebird

----

| This replaces SQLAlchemy's internal Firebird dialect which is not being maintained
 and will be removed in a future version.

****

**Installation**

::

    pip install sqlalchemy-firebird

|
|  Connection URI samples for Firebird server installed on local machine using default port (3050):

::

    [Linux]
    firebird://username:password@localhost///home/paulgd/projects/databases/my_project.fdb

    [Windows]
    firebird://username:password@localhost/c:/projects/databases/my_project.fdb

----

**Code of Conduct**

As with SQLAlchemy, sqlalchemy-firebird places great emphasis on polite, thoughtful, and
constructive communication between users and developers.
We use the SQLAlchemy `Code of Conduct <http://www.sqlalchemy.org/codeofconduct.html>`_.

----

**License**

sqlalchemy-firebird is distributed under the `MIT license
<http://www.opensource.org/licenses/mit-license.php>`_.
