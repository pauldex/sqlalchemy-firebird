"""
.. dialect:: firebird+fdb
    :name: fdb
    :dbapi: fdb
    :connectstring: firebird+fdb://user:password@host:port/path/to/db[?key=value&key=value...]
    :url: http://pypi.python.org/pypi/fdb/

    The FDB package provides legacy driver for Python 2 and 3, and Firebird 2.x and 3. 
    This driver uses classic Firebird API provided by fbclient library.
"""  # noqa

from math import modf

from sqlalchemy import util
from .base import FBDialect

import fdb

class FBDialect_fdb(FBDialect):
    name = "firebird.fdb"
    driver = "fdb"
    supports_statement_cache = True

    @classmethod
    def import_dbapi(cls):
        return fdb

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        if opts.get("port"):
            opts["host"] = "%s/%s" % (opts["host"], opts["port"])
            del opts["port"]
        opts.update(url.query)

        util.coerce_kw_type(opts, "type_conv", int)

        return ([], opts)

    def _get_server_version_info(self, connection):
        dbapi_connection = connection.connection.dbapi_connection
        minor, major = modf(dbapi_connection.engine_version)
        return (int(major), int(minor))


dialect = FBDialect_fdb
