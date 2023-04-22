from sqlalchemy import types as sqltypes

class _StringType(sqltypes.String):
    """Base for Firebird string types."""

    def __init__(self, charset=None, **kw):
        self.charset = charset
        super(_StringType, self).__init__(**kw)


class VARCHAR(_StringType, sqltypes.VARCHAR):
    """Firebird VARCHAR type"""

    __visit_name__ = "VARCHAR"

    def __init__(self, length=None, **kwargs):
        super(VARCHAR, self).__init__(length=length, **kwargs)


class CHAR(_StringType, sqltypes.CHAR):
    """Firebird CHAR type"""

    __visit_name__ = "CHAR"

    def __init__(self, length=None, **kwargs):
        super(CHAR, self).__init__(length=length, **kwargs)
