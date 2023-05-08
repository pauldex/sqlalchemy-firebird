"""
.. dialect:: firebird+fdb
    :name: fdb
    :dbapi: fdb
    :connectstring: firebird+fdb://user:password@host:port/path/to/db[?key=value&key=value...]
    :url: http://pypi.python.org/pypi/fdb/

    The FDB package provides legacy driver for Python 2 and 3, and Firebird 2.x and 3. 
    This driver uses classic Firebird API provided by fbclient library.
"""  # noqa

from sqlalchemy import util
from sqlalchemy import __version__ as sqla_version
from re import match
from .base import FBDialect


class FBDialect_fdb(FBDialect):
    name = "firebird.fdb"
    driver = "fdb"
    supports_sane_multi_rowcount = False
    supports_statement_cache = True
    supports_native_decimal = True

    if sqla_version < "2":

        @classmethod
        def dbapi(cls):
            return __import__("fdb")

    else:

        @classmethod
        def import_dbapi(cls):
            return __import__("fdb")

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

        Returns a tuple of (`major`, `minor`, `build`, `server_name`), three integers representing the version
        of the attached server and a string representing the name of the server type (firebird or interbase).
        """

        # This is the simpler approach (the other uses the services api),
        # that for backward compatibility reasons returns a string like
        #   LI-V6.3.3.12981 Firebird 2.0
        # where the first version is a fake one resembling the old
        # Interbase signature.
        def parse_version_info0(version):
            m = match(
                r"\w+-[V|T](\d+)\.(\d+)\.(\d+)\.(\d+)( \w+ (\d+)\.(\d+))?",
                version,
            )
            if not m:
                raise AssertionError(
                    "Could not determine version from string '%s'" % version
                )

            if m.group(5) is not None:
                return tuple([int(x) for x in m.group(6, 7, 4)] + ["firebird"])
            else:
                return tuple(
                    [int(x) for x in m.group(1, 2, 3)] + ["interbase"]
                )

        isc_info_firebird_version = 103
        fbconn = connection.connection

        version = fbconn.db_info(isc_info_firebird_version)

        return parse_version_info0(version)


dialect = FBDialect_fdb
