"""
.. dialect:: firebird+firebird
    :name: firebird
    :dbapi: firebird-driver
    :connectstring: firebird+firebird://user:password@host:port/path/to/db[?key=value&key=value...]
    :url: https://pypi.org/project/firebird-driver/

    The firebird-driver package provides driver for Python 3.8+ and Firebird 3+. 
    This driver uses new Firebird OO API provided by fbclient library.
"""  # noqa

from math import modf

from sqlalchemy import util
from sqlalchemy import types as sqltypes
from .base import FBDialect

import firebird.driver
from firebird.driver import driver_config


class _binary_firebird:
    def bind_processor(self, dialect):
        def process(value):
            return None if value is None else bytes(value)

        return process


class BINARY_firebird(_binary_firebird, sqltypes.BINARY):
    pass


class VARBINARY_firebird(_binary_firebird, sqltypes.VARBINARY):
    pass


class LargeBinary_firebird(_binary_firebird, sqltypes.LargeBinary):
    pass


class FBDialect_firebird(FBDialect):
    name = "firebird.firebird"
    driver = "firebird-driver"
    supports_statement_cache = True

    colspecs = util.update_copy(
        FBDialect.colspecs,
        {
            sqltypes.BINARY: BINARY_firebird,
            sqltypes.VARBINARY: VARBINARY_firebird,
            sqltypes.LargeBinary: LargeBinary_firebird,
        },
    )

    @classmethod
    def import_dbapi(cls):
        return firebird.driver

    @util.memoized_property
    def _isolation_lookup(self):
        return {
            "AUTOCOMMIT": "autocommit",
            "READ COMMITTED": "read_committed",
            "REPEATABLE READ": "repeatable_read",
            "SERIALIZABLE": "serializable",
        }

    def get_isolation_level_values(self, dbapi_connection):
        return list(self._isolation_lookup)

    def set_isolation_level(self, dbapi_connection, level):
        dbapi_connection.set_isolation_level(self._isolation_lookup[level])

    def set_readonly(self, connection, value):
        connection.readonly = value

    def get_readonly(self, connection):
        return connection.readonly

    def set_deferrable(self, connection, value):
        connection.deferrable = value

    def get_deferrable(self, connection):
        return connection.deferrable

    def do_terminate(self, dbapi_connection) -> None:
        dbapi_connection.terminate()

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")

        qry = url.query
        if qry.get("fb_client_library"):
            # Set driver_config.fb_client_library and remove it from remaining keys passed to .connect()
            driver_config.fb_client_library.value = qry["fb_client_library"]
            qry = remove_keys(qry, {"fb_client_library"})

        if opts.get("port"):
            opts["host"] = "%s/%s" % (opts["host"], opts["port"])
            del opts["port"]

        opts.update(qry)
        return ([], opts)

    def do_rollback(self, dbapi_connection):
        if dbapi_connection.is_active():
            dbapi_connection.rollback()

    def do_commit(self, dbapi_connection):
        if dbapi_connection.is_active():
            dbapi_connection.commit()

    def _get_server_version_info(self, connection):
        dbapi_connection = connection.connection.dbapi_connection
        minor, major = modf(dbapi_connection.info.engine_version)
        return (int(major), int(minor))


def remove_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


dialect = FBDialect_firebird
