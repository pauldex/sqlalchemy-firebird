import datetime as dt

from typing import Any
from typing import Optional
from sqlalchemy import Dialect, types as sqltypes


class _FBString(sqltypes.String):
    render_bind_cast = True

    def __init__(self, length=None, charset=None, **kwargs):
        super().__init__(length, **kwargs)
        self.charset = charset


class _FBCHAR(_FBString, sqltypes.CHAR):
    __visit_name__ = "CHAR"

    def __init__(self, length=None, charset=None, **kwargs):
        super().__init__(length, charset, **kwargs)


class _FBVARCHAR(_FBString, sqltypes.VARCHAR):
    __visit_name__ = "VARCHAR"

    def __init__(self, length=None, charset=None, **kwargs):
        super().__init__(length, charset, **kwargs)


class _FBNumeric(sqltypes.Numeric):
    render_bind_cast = True

    def bind_processor(self, dialect):
        return None  # Dialect supports_native_decimal = True (no processor needed)


class _FBFLOAT(_FBNumeric, sqltypes.FLOAT):
    __visit_name__ = "FLOAT"


class _FBDOUBLE_PRECISION(_FBNumeric, sqltypes.DOUBLE_PRECISION):
    __visit_name__ = "DOUBLE PRECISION"


class _FBDECFLOAT(_FBNumeric, sqltypes.FLOAT):
    __visit_name__ = "DECFLOAT"


class _FBDATE(sqltypes.DATE):
    render_bind_cast = True


class _FBTIME(sqltypes.TIME):
    render_bind_cast = True


class _FBTIMESTAMP(sqltypes.TIMESTAMP):
    render_bind_cast = True


class _FBInteger(sqltypes.Integer):
    render_bind_cast = True


class _FBSMALLINT(_FBInteger):
    __visit_name__ = "SMALLINT"


class _FBINTEGER(_FBInteger):
    __visit_name__ = "INTEGER"


class _FBBIGINT(_FBInteger):
    __visit_name__ = "BIGINT"


class _FBINT128(_FBInteger):
    __visit_name__ = "INT128"


class _FBBOOLEAN(sqltypes.BOOLEAN):
    render_bind_cast = True


class _FBLargeBinary(sqltypes.LargeBinary):
    render_bind_cast = True

    def __init__(
        self,
        length=None,
        subtype=0,
        segment_size=None,
        charset=None,
        collation=None,
        **kwargs,
    ):
        super().__init__(length, **kwargs)
        self.subtype = subtype
        self.segment_size = segment_size
        self.charset = charset
        self.collation = collation

    def bind_processor(self, dialect):
        def process(value):
            return None if value is None else bytes(value)

        return process


class _FBBLOB(_FBLargeBinary, sqltypes.BLOB):
    __visit_name__ = "BLOG SUB_TYPE BINARY"

    def __init__(
        self,
        length=None,
        segment_size=None,
        **kwargs,
    ):
        super().__init__(length, 0, segment_size, **kwargs)


class _FBTEXT(_FBLargeBinary, sqltypes.TEXT):
    __visit_name__ = "BLOG SUB_TYPE TEXT"

    def __init__(
        self,
        length=None,
        segment_size=None,
        charset=None,
        collation=None,
        **kwargs,
    ):
        super().__init__(length, 1, segment_size, charset, collation, **kwargs)


class _FBNumericInterval(_FBNumeric):
    # NUMERIC(18,9) -- Used for _FBInterval storage
    def __init__(self):
        super().__init__(precision=18, scale=9)


class _FBInterval(sqltypes.Interval):
    """A type for ``datetime.timedelta()`` objects.

    Value is stored as number of days.
    """

    # ToDo: Fix operations with TIME datatype (operand must be in seconds, not in days)
    #   https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref50/firebird-50-language-reference.html#fblangref50-datatypes-datetimeops

    impl = _FBNumericInterval
    cache_ok = True

    def __init__(self):
        super().__init__(native=False)

    def bind_processor(self, dialect: Dialect):
        impl_processor = self.impl_instance.bind_processor(dialect)
        if impl_processor:
            fixed_impl_processor = impl_processor

            def process(value: Optional[dt.timedelta]):
                dt_value = (
                    value.total_seconds() / 86400
                    if value is not None
                    else None
                )
                return fixed_impl_processor(dt_value)

        else:

            def process(value: Optional[dt.timedelta]):
                return (
                    value.total_seconds() / 86400
                    if value is not None
                    else None
                )

        return process

    def result_processor(self, dialect: Dialect, coltype: Any):
        impl_processor = self.impl_instance.result_processor(dialect, coltype)
        if impl_processor:
            fixed_impl_processor = impl_processor

            def process(value: Any) -> Optional[dt.timedelta]:
                dt_value = fixed_impl_processor(value)
                if dt_value is None:
                    return None
                return dt.timedelta(days=dt_value)

        else:

            def process(value: Any) -> Optional[dt.timedelta]:
                return dt.timedelta(days=value) if value is not None else None

        return process
