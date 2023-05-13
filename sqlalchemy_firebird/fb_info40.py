"""Provide Firebird 4.0 specific information.

    Variables:
        MAX_IDENTIFIER_LENGTH -> int
        RESERVED_WORDS -> set
        ISCHEMA_NAMES -> dict

.._Firebird 4.0:
    https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-intro

.._Firebird 5.0:
    https://www.firebirdsql.org/file/documentation/release_notes/Firebird-5.0.0-Beta1-ReleaseNotes.pdf

"""

from packaging import version

from sqlalchemy import __version__ as SQLALCHEMY_VERSION
from sqlalchemy.types import BIGINT
from sqlalchemy.types import BINARY
from sqlalchemy.types import BLOB
from sqlalchemy.types import BOOLEAN
from sqlalchemy.types import DATE
from sqlalchemy.types import FLOAT
from sqlalchemy.types import INTEGER
from sqlalchemy.types import NUMERIC
from sqlalchemy.types import REAL
from sqlalchemy.types import SMALLINT
from sqlalchemy.types import TEXT
from sqlalchemy.types import TIME
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import VARBINARY

from .types import CHAR
from .types import VARCHAR
from .types import DOUBLE_PRECISION

# https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html
# For Firebird version 4.0 and greater, the "...maximum identifier length is 63 characters
# character set UTF8 (252 bytes)".
MAX_IDENTIFIER_LENGTH = 63

# https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-reskeywords-reswords
# This set is also good for Firebird version 5.0 Beta 1
# Note that reserved words in Firebird 5 are the same as those in Firebird 4
RESERVED_WORDS = {
    "add",
    "admin",
    "all",
    "alter",
    "and",
    "any",
    "as",
    "at",
    "avg",
    "begin",
    "between",
    "bigint",
    "binary",
    "bit_length",
    "blob",
    "boolean",
    "both",
    "by",
    "case",
    "cast",
    "char",
    "character",
    "character_length",
    "char_length",
    "check",
    "close",
    "collate",
    "column",
    "comment",
    "commit",
    "connect",
    "constraint",
    "corr",
    "count",
    "covar_pop",
    "covar_samp",
    "create",
    "cross",
    "current",
    "current_connection",
    "current_date",
    "current_role",
    "current_time",
    "current_timestamp",
    "current_transaction",
    "current_user",
    "cursor",
    "date",
    "day",
    "dec",
    "decfloat",
    "decimal",
    "declare",
    "default",
    "delete",
    "deleting",
    "deterministic",
    "disconnect",
    "distinct",
    "double",
    "drop",
    "else",
    "end",
    "escape",
    "execute",
    "exists",
    "external",
    "extract",
    "false",
    "fetch",
    "filter",
    "float",
    "for",
    "foreign",
    "from",
    "full",
    "function",
    "gdscode",
    "global",
    "grant",
    "group",
    "having",
    "hour",
    "in",
    "index",
    "inner",
    "insensitive",
    "insert",
    "inserting",
    "int",
    "int128",
    "integer",
    "into",
    "is",
    "join",
    "lateral",
    "leading",
    "left",
    "like",
    "local",
    "localtime",
    "localtimestamp",
    "long",
    "lower",
    "max",
    "merge",
    "min",
    "minute",
    "month",
    "national",
    "natural",
    "nchar",
    "no",
    "not",
    "null",
    "numeric",
    "octet_length",
    "of",
    "offset",
    "on",
    "only",
    "open",
    "or",
    "order",
    "outer",
    "over",
    "parameter",
    "plan",
    "position",
    "post_event",
    "precision",
    "primary",
    "procedure",
    "publication",
    "rdb$db_key",
    "rdb$error",
    "rdb$get_context",
    "rdb$get_transaction_cn",
    "rdb$record_version",
    "rdb$role_in_use",
    "rdb$set_context",
    "rdb$system_privilege",
    "real",
    "record_version",
    "recreate",
    "recursive",
    "references",
    "regr_avgx",
    "regr_avgy",
    "regr_count",
    "regr_intercept",
    "regr_r2",
    "regr_slope",
    "regr_sxx",
    "regr_sxy",
    "regr_syy",
    "release",
    "resetting",
    "return",
    "returning_values",
    "returns",
    "revoke",
    "right",
    "rollback",
    "row",
    "rows",
    "row_count",
    "savepoint",
    "scroll",
    "second",
    "select",
    "sensitive",
    "set",
    "similar",
    "smallint",
    "some",
    "sqlcode",
    "sqlstate",
    "start",
    "stddev_pop",
    "stddev_samp",
    "sum",
    "table",
    "then",
    "time",
    "timestamp",
    "timezone_hour",
    "timezone_minute",
    "to",
    "trailing",
    "trigger",
    "trim",
    "true",
    "unbounded",
    "union",
    "unique",
    "unknown",
    "update",
    "updating",
    "upper",
    "user",
    "using",
    "value",
    "values",
    "varbinary",
    "varchar",
    "variable",
    "varying",
    "var_pop",
    "var_samp",
    "view",
    "when",
    "where",
    "while",
    "window",
    "with",
    "without",
    "year",
}

# https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-datatypes-syntax-scalar
ISCHEMA_NAMES = {
    "SMALLINT": SMALLINT,
    "INT": INTEGER,
    "INTEGER": INTEGER,
    "BIGINT": BIGINT,
    "INT128": BIGINT,  # TODO: INT128
    "REAL": REAL,
    "FLOAT": FLOAT,
    "DOUBLE PRECISION": FLOAT if version.parse(SQLALCHEMY_VERSION).major < 2 else DOUBLE_PRECISION,
    "DECFLOAT": FLOAT,  # TODO: DECFLOAT
    "BOOLEAN": BOOLEAN,
    "DATE": DATE,
    "TIME": TIME,
    "TIME WITH TIME ZONE": TIME,
    "TIME WITHOUT TIME ZONE": TIME,
    "TIMESTAMP": TIMESTAMP,
    "TIMESTAMP WITH TIME ZONE": TIMESTAMP,
    "TIMESTAMP WITHOUT TIME ZONE": TIMESTAMP,
    "DECIMAL": NUMERIC,
    "NUMERIC": NUMERIC,
    "VARCHAR": VARCHAR,
    "CHAR VARYING": VARCHAR,
    "CHARACTER VARYING": VARCHAR,
    "CHAR": CHAR,
    "CHARACTER": CHAR,
    "BINARY": BINARY,
    "VARBINARY": VARBINARY,
    "BINARY VARYING": VARBINARY,
    # Compatibility
    "SHORT": SMALLINT,
    "LONG": INTEGER,
    "QUAD": FLOAT,
    "TEXT": TEXT,
    "INT64": BIGINT,
    "DOUBLE": FLOAT,
    "VARYING": VARCHAR,
    "CSTRING": CHAR,
    "BLOB": BLOB,
}