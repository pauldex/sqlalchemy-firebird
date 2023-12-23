from sqlalchemy import types as sqltypes


class _FBString(sqltypes.String):
    render_bind_cast = True

    def __init__(self, length=None, charset=None, **kwargs):
        super().__init__(length, **kwargs)
        self.charset = charset


class _FBCHAR(_FBString, sqltypes.CHAR):
    __visit_name__ = "CHAR"

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)


class _FBVARCHAR(_FBString, sqltypes.VARCHAR):
    __visit_name__ = "VARCHAR"

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)


class _FBNumeric(sqltypes.Numeric):
    render_bind_cast = True

    def bind_processor(self, dialect):
        return None  # Dialect supports_native_decimal = True (no processor needed)


class _FBFLOAT(_FBNumeric, sqltypes.FLOAT):
    __visit_name__ = "FLOAT"


class _FBDOUBLE_PRECISION(_FBNumeric, sqltypes.DOUBLE_PRECISION):
    __visit_name__ = "DOUBLE PRECISION"


class _FBDATE(sqltypes.DATE):
    render_bind_cast = True


class _FBTIME(sqltypes.TIME):
    render_bind_cast = True


class _FBTIMESTAMP(sqltypes.TIMESTAMP):
    render_bind_cast = True


class _FBSMALLINT(sqltypes.Integer):
    __visit_name__ = "SMALLINT"
    render_bind_cast = True


class _FBINTEGER(sqltypes.Integer):
    __visit_name__ = "INTEGER"
    render_bind_cast = True


class _FBBIGINT(sqltypes.Integer):
    __visit_name__ = "BIGINT"
    render_bind_cast = True


class _FBINT128(sqltypes.Integer):
    __visit_name__ = "INT128"
    render_bind_cast = True


class _FBBinaryBase:
    def bind_processor(self, dialect):
        def process(value):
            return None if value is None else bytes(value)

        return process


class _FBBINARY(_FBBinaryBase, sqltypes.BINARY):
    pass


class _FBVARBINARY(_FBBinaryBase, sqltypes.VARBINARY):
    pass


# Todo: DECFLOAT and NCHAR/NVARCHAR (legacy types with ISO8859_1 charset)
