"""
.. dialect:: firebird+fdb
    :name: fdb
    :dbapi: pyodbc
    :connectstring: firebird+fdb://user:password@host:port/path/to/db[?key=value&key=value...]
    :url: http://pypi.python.org/pypi/fdb/

    fdb is a DBAPI for Firebird.

Arguments
----------

* ``enable_rowcount`` - True by default, setting this to False disables
  the usage of "cursor.rowcount", which SQLAlchemy ordinarily calls upon automatically
  after any UPDATE or DELETE statement.  When disabled, SQLAlchemy's
  ResultProxy will return -1 for result.rowcount.
  
  The behavior can also be controlled on a per-execution basis using the ``enable_rowcount`` option with
  :meth:`.Connection.execution_options`::

      conn = engine.connect().execution_options(enable_rowcount=True)
      r = conn.execute(stmt)
      print r.rowcount

* ``retaining`` - False by default.   Setting this to True will pass the
  ``retaining=True`` keyword argument to the ``.commit()`` and ``.rollback()``
  methods of the DBAPI connection, which can improve performance in some
  situations, but apparently with significant caveats.
  Please read the fdb DBAPI documentation in order to
  understand the implications of this flag.

  .. seealso::

    http://pythonhosted.org/fdb/usage-guide.html#retaining-transactions
    - information on the "retaining" flag.

"""  # noqa

from sqlalchemy import util
from sqlalchemy import __version__ as sqla_version
from re import match
from .base import FBDialect
from .base import FBExecutionContext


class FBExecutionContext_fdb(FBExecutionContext):
    @property
    def rowcount(self):
        if self.execution_options.get(
            "enable_rowcount", self.dialect.enable_rowcount
        ):
            return self.cursor.rowcount
        else:
            return -1


class FBDialect_fdb(FBDialect):
    driver = "fdb"
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_statement_cache = True
    supports_native_decimal = True
    execution_ctx_cls = FBExecutionContext_fdb
    using_dialect_3 = False

    def __init__(self, enable_rowcount=True, retaining=False, **kwargs):
        super(FBDialect_fdb, self).__init__(
            enable_rowcount=enable_rowcount, retaining=retaining, **kwargs
        )
        self.enable_rowcount = enable_rowcount
        self.retaining = retaining
        if enable_rowcount:
            self.supports_sane_rowcount = True

    if sqla_version < "2":

        @classmethod
        def dbapi(cls):
            return __import__("fdb")

    else:

        @classmethod
        def import_dbapi(cls):
            return __import__("fdb")

    def do_rollback(self, dbapi_connection):
        dbapi_connection.rollback(self.retaining)

    def do_commit(self, dbapi_connection):
        dbapi_connection.commit(self.retaining)

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        if opts.get("port"):
            opts["host"] = "%s/%s" % (opts["host"], opts["port"])
            del opts["port"]
        opts.update(url.query)

        util.coerce_kw_type(opts, "type_conv", int)

        return ([], opts)

    def _get_server_version_info(self, connection):
        """Get the version of the Firebird server used by a connection.

        Returns a tuple of (`major`, `minor`, `build`), three integers
        representing the version of the attached server.
        """
        # This is the simpler approach (the other uses the services api),
        # that for backward compatibility reasons returns a string like
        #   LI-V6.3.3.12981 Firebird 2.0
        # where the first version is a fake one resembling the old
        # Interbase signature.
        isc_info_firebird_version = 103
        fbconn = connection.connection

        version = fbconn.db_info(isc_info_firebird_version)

        return self._parse_version_info(version)


    def _parse_version_info(self, version):
        m = match(
                r"\w+-[V|T](\d+)\.(\d+)\.(\d+)\.(\d+)( \w+ (\d+)\.(\d+))?", version
        )
        if not m:
            raise AssertionError(
                    "Could not determine version from string '%s'" % version
            )

        if m.group(5) is not None:
            return tuple([int(x) for x in m.group(6, 7, 4)] + ["firebird"])
        else:
            return tuple([int(x) for x in m.group(1, 2, 3)] + ["interbase"])


    def is_disconnect(self, e, connection, cursor):
        if isinstance(
            e, (self.dbapi.OperationalError, self.dbapi.ProgrammingError)
        ):
            msg = str(e)
            return (
                "Error writing data to the connection" in msg
                or "Unable to complete network request to host" in msg
                or "Invalid connection state" in msg
                or "Invalid cursor state" in msg
                or "connection shutdown" in msg
            )
        else:
            return False

dialect = FBDialect_fdb
