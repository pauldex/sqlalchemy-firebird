# sqlalchemy-firebird

An external SQLAlchemy dialect for Firebird.

This will replace SQLAlchemy's internal Firebird dialect which is not being maintained.

Sample connection URI:

```
firebird2://sysdba:scott_tiger@localhost//home/gord/git/sqlalchemy-firebird/sqla_test.fdb
```

The dialect identifier is currently "firebird2" to avoid conflicts with the internal dialect.
Eventually both `firebird://` and `firebird2://` will be equivalent.
