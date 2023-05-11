from sqlalchemy import types as sqltypes


class _StringType(sqltypes.String):
    """Base for Firebird string types."""

    def __init__(self, length=None, charset=None, **kwargs):
        super().__init__(length, **kwargs)
        self.charset = charset


class CHAR(_StringType, sqltypes.CHAR):
    """Firebird CHAR type"""

    __visit_name__ = "CHAR"

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)


class VARCHAR(_StringType, sqltypes.VARCHAR):
    """Firebird VARCHAR type"""

    __visit_name__ = "VARCHAR"

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)


class DOUBLE_PRECISION(sqltypes.Float):

    """The SQL DOUBLE PRECISION type."""

    __visit_name__ = "DOUBLE PRECISION"
