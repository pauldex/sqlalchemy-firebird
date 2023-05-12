from packaging import version

from sqlalchemy import exc
from sqlalchemy import schema as sa_schema
from sqlalchemy import sql
from sqlalchemy import text
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy import __version__ as SQLALCHEMY_VERSION
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy.sql import compiler
from sqlalchemy.sql import expression
from sqlalchemy.types import BIGINT
from sqlalchemy.types import BINARY
from sqlalchemy.types import BLOB
from sqlalchemy.types import BOOLEAN
from sqlalchemy.types import DATE
from sqlalchemy.types import FLOAT
from sqlalchemy.types import INTEGER
from sqlalchemy.types import Integer
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


RESERVED_WORDS_INITIAL = {
    "active",
    "add",
    "admin",
    "after",
    "all",
    "alter",
    "and",
    "any",
    "as",
    "asc",
    "ascending",
    "at",
    "auto",
    "avg",
    "before",
    "begin",
    "between",
    "bigint",
    "bit_length",
    "blob",
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
    "commit",
    "committed",
    "computed",
    "conditional",
    "connect",
    "constraint",
    "containing",
    "count",
    "create",
    "cross",
    "cstring",
    "current",
    "current_connection",
    "current_date",
    "current_role",
    "current_time",
    "current_timestamp",
    "current_transaction",
    "current_user",
    "cursor",
    "database",
    "date",
    "day",
    "dec",
    "decimal",
    "declare",
    "default",
    "delete",
    "desc",
    "descending",
    "disconnect",
    "distinct",
    "do",
    "domain",
    "double",
    "drop",
    "else",
    "end",
    "entry_point",
    "escape",
    "exception",
    "execute",
    "exists",
    "exit",
    "external",
    "extract",
    "fetch",
    "file",
    "filter",
    "float",
    "for",
    "foreign",
    "from",
    "full",
    "function",
    "gdscode",
    "generator",
    "gen_id",
    "global",
    "grant",
    "group",
    "having",
    "hour",
    "if",
    "in",
    "inactive",
    "index",
    "inner",
    "input_type",
    "insensitive",
    "insert",
    "int",
    "integer",
    "into",
    "is",
    "isolation",
    "join",
    "key",
    "leading",
    "left",
    "length",
    "level",
    "like",
    "long",
    "lower",
    "manual",
    "max",
    "maximum_segment",
    "merge",
    "min",
    "minute",
    "module_name",
    "month",
    "names",
    "national",
    "natural",
    "nchar",
    "no",
    "not",
    "null",
    "numeric",
    "octet_length",
    "of",
    "on",
    "only",
    "open",
    "option",
    "or",
    "order",
    "outer",
    "output_type",
    "overflow",
    "page",
    "pages",
    "page_size",
    "parameter",
    "password",
    "plan",
    "position",
    "post_event",
    "precision",
    "primary",
    "privileges",
    "procedure",
    "protected",
    "rdb$db_key",
    "read",
    "real",
    "record_version",
    "recreate",
    "recursive",
    "references",
    "release",
    "reserv",
    "reserving",
    "retain",
    "returning_values",
    "returns",
    "revoke",
    "right",
    "rollback",
    "rows",
    "row_count",
    "savepoint",
    "schema",
    "second",
    "segment",
    "select",
    "sensitive",
    "set",
    "shadow",
    "shared",
    "singular",
    "size",
    "smallint",
    "snapshot",
    "some",
    "sort",
    "sqlcode",
    "stability",
    "start",
    "starting",
    "starts",
    "statistics",
    "sub_type",
    "sum",
    "suspend",
    "table",
    "then",
    "time",
    "timestamp",
    "to",
    "trailing",
    "transaction",
    "trigger",
    "trim",
    "uncommitted",
    "union",
    "unique",
    "update",
    "upper",
    "user",
    "using",
    "value",
    "values",
    "varchar",
    "variable",
    "varying",
    "view",
    "wait",
    "when",
    "where",
    "while",
    "with",
    "work",
    "write",
    "year",
}

# https://www.firebirdsql.org/file/documentation/html/en/refdocs/fblangref25/firebird-25-language-reference.html#fblangref25-appx03-reskeywords
# This set is for Firebird versions >= 2.5.1
RESERVED_WORDS_25 = {
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
    "bit_length",
    "blob",
    "both",
    "by",
    "case",
    "cast",
    "char",
    "char_length",
    "character",
    "character_length",
    "check",
    "close",
    "collate",
    "column",
    "commit",
    "connect",
    "constraint",
    "count",
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
    "decimal",
    "declare",
    "default",
    "delete",
    "deleting",
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
    "integer",
    "into",
    "is",
    "join",
    "leading",
    "left",
    "like",
    "long",
    "lower",
    "max",
    "maximum_segment",
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
    "on",
    "only",
    "open",
    "or",
    "order",
    "outer",
    "parameter",
    "plan",
    "position",
    "post_event",
    "precision",
    "primary",
    "procedure",
    "rdb$db_key",
    "real",
    "record_version",
    "recreate",
    "recursive",
    "references",
    "release",
    "returning_values",
    "returns",
    "revoke",
    "right",
    "rollback",
    "row_count",
    "rows",
    "savepoint",
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
    "sum",
    "table",
    "then",
    "time",
    "timestamp",
    "to",
    "trailing",
    "trigger",
    "trim",
    "union",
    "unique",
    "update",
    "updating",
    "upper",
    "user",
    "using",
    "value",
    "values",
    "varchar",
    "variable",
    "varying",
    "view",
    "when",
    "where",
    "while",
    "with",
    "year",
}

# https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref30/firebird-30-language-reference.html#fblangref30-appx03-reskeywords
RESERVED_WORDS_30 = {
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
    "integer",
    "into",
    "is",
    "join",
    "leading",
    "left",
    "like",
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
    "rdb$db_key",
    "rdb$record_version",
    "real",
    "record_version",
    "recreate",
    "recursive references",
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
    "to",
    "trailing",
    "trigger",
    "trim",
    "true",
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
    "varchar",
    "variable",
    "varying",
    "var_pop",
    "var_samp",
    "view",
    "when",
    "where",
    "while",
    "with",
    "year",
}

# https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-reskeywords-reswords
# This set is also good for Firebird version 5.0 Beta 1
# https://www.firebirdsql.org/file/documentation/release_notes/Firebird-5.0.0-Beta1-ReleaseNotes.pdf
RESERVED_WORDS_40 = {
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
ischema_names = {
    "SMALLINT": SMALLINT,
    "INT": INTEGER,
    "INTEGER": INTEGER,
    "BIGINT": BIGINT,
    "INT128": BIGINT, # TODO: INT128

    "REAL": REAL,
    "FLOAT": FLOAT,
    "DOUBLE PRECISION": DOUBLE_PRECISION,
    "DECFLOAT": FLOAT, # TODO: DEFCLOAT

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

EXPRESSION_SEPARATOR = "||"

class FBCompiler(sql.compiler.SQLCompiler):
    ansi_bind_rules = True

    def visit_empty_set_expr(self, element_types, **kw):
        return "SELECT 1 FROM rdb$database WHERE 1!=1"

    def visit_sequence(self, sequence, **kw):
        return "GEN_ID(%s, 1)" % self.preparer.format_sequence(sequence)
    
    def limit_clause(self, select, **kw):
        return self._handle_limit_fetch_clause(None, select._offset_clause, select._limit_clause, **kw)
    
    def fetch_clause(
        self,
        select,
        fetch_clause=None,
        require_offset=False,
        use_literal_execute_for_simple_int=False,
        **kw,
    ):
        if fetch_clause is None:
            fetch_clause = select._fetch_clause

        return self._handle_limit_fetch_clause(fetch_clause, select._offset_clause, None, **kw)
    
    def _handle_limit_fetch_clause(self, fetch_clause, offset_clause, limit_clause, **kw):
        # Albeit non-standard, ROWS is a better choice than OFFSET / FETCH in Firebird since
        #   it is supported since Firebird 2.5 and it works with expressions.
        # https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-dml-select-rows
        text = ""

        if (fetch_clause is not None) and (offset_clause is not None):
            # OFFSET 2 ROWS FETCH NEXT 5 ROWS ONLY  =>  ROWS 2 + 1 TO 2 + 5
            text += " \n ROWS " + self.process(offset_clause, **kw) + " + 1 TO " + self.process(offset_clause, **kw) + " + " + self.process(fetch_clause, **kw)
        elif (limit_clause is not None) and (offset_clause is not None):
            # LIMIT 5 OFFSET 2  =>  ROWS 2 + 1 TO 2 + 5
            text += " \n ROWS " + self.process(offset_clause, **kw) + " + 1 TO " + self.process(offset_clause, **kw) + " + " + self.process(limit_clause, **kw)
        elif fetch_clause is not None:
            # FETCH NEXT 5 ROWS ONLY  =>  ROWS 1 TO 5
            text += " \n ROWS 1 TO " + self.process(fetch_clause, **kw)
        elif limit_clause is not None:
            # LIMIT 5  =>  ROWS 1 TO 5
            text += " \n ROWS 1 TO " + self.process(limit_clause, **kw)
        elif offset_clause is not None:
            # OFFSET 2 ROWS  =>  ROWS 2 + 1 TO 9223372036854775807
            text += " \n ROWS " + self.process(offset_clause, **kw) + " + 1 TO 9223372036854775807"

        return text

    def visit_substring_func(self, func, **kw):
        s = self.process(func.clauses.clauses[0])
        start = self.process(func.clauses.clauses[1])
        if len(func.clauses.clauses) > 2:
            length = self.process(func.clauses.clauses[2])
            return "SUBSTRING(%s FROM %s FOR %s)" % (s, start, length)
        else:
            return "SUBSTRING(%s FROM %s)" % (s, start)

    def visit_truediv_binary(self, binary, operator, **kw):
        return (
            self.process(binary.left, **kw)
            + " / "
            + "(%s + 0.0)" % self.process(binary.right, **kw)
        )

    def visit_mod_binary(self, binary, operator, **kw):
        return "MOD(%s, %s)" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_now_func(self, fn, **kw):
        return "CURRENT_TIMESTAMP"

    def function_argspec(self, fn, **kw):
        if fn.clauses is not None and len(fn.clauses) > 0:
            return self.process(fn.clause_expr, **kw)

        return ""

    def visit_char_length_func(self, fn, **kw):
        return "CHAR_LENGTH" + self.function_argspec(fn, **kw)

    def visit_length_func(self, fn, **kw):
        return "CHAR_LENGTH" + self.function_argspec(fn, **kw)

    def default_from(self):
        return " FROM rdb$database"
    
    def returning_clause(self, stmt, returning_cols, **kw):
        if self.dialect.using_sqlalchemy2:
            return super().returning_clause(stmt, returning_cols, **kw)
        
        # For SQLAlchemy 1.4 compatibility only. Unneeded in 2.0.
        columns = [
            self._label_returning_column(stmt, c)
            for c in expression._select_iterables(returning_cols)
        ]

        return "RETURNING " + ", ".join(columns)
    

class FBDDLCompiler(sql.compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = self.preparer.format_column(column)

        impl_type = column.type.dialect_impl(self.dialect)
        if isinstance(impl_type, sqltypes.TypeDecorator):
            impl_type = impl_type.impl

        has_identity = (
            column.identity is not None
        )

        if (
            column.primary_key
            and column is column.table._autoincrement_column
            and not has_identity
            and (
                column.default is None
                or (
                    isinstance(column.default, sa_schema.Sequence)
                    and column.default.optional
                )
            )
            and self.dialect.supports_identity_columns
        ):
            colspec += " INTEGER GENERATED BY DEFAULT AS IDENTITY"
        else:
            type_compiler_instance = self.dialect.type_compiler_instance if self.dialect.using_sqlalchemy2 \
                                     else self.dialect.type_compiler

            colspec += " " + type_compiler_instance.process(
                column.type,
                type_expression=column,
                identifier_preparer=self.preparer,
            )
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

            if column.computed is not None:
                colspec += " " + self.process(column.computed)
            if has_identity:
                colspec += " " + self.process(column.identity)

            if not column.nullable and not has_identity:
                colspec += " NOT NULL"
            elif column.nullable and has_identity:
                colspec += " NULL"

        return colspec

    def visit_create_index(
        self, create, include_schema=False, include_table_schema=True, **kw
    ):
        preparer = self.preparer
        index = create.element
        self._verify_index_table(index)

        if index.name is None:
            raise exc.CompileError("CREATE INDEX requires that the index have a name.")

        text = "CREATE "
        if index.unique:
            text += "UNIQUE "

        text += "INDEX %s ON %s " % (
            self._prepared_index_name(index, include_schema=include_schema),
            preparer.format_table(index.table, use_schema=include_table_schema),
        )
        
        if index.expressions is None:
            raise exc.CompileError("CREATE INDEX requires at least one column or expression.")

        first_expression = index.expressions[0] if len(index.expressions) > 0 else index.expressions
        
        if isinstance(first_expression, expression.ColumnClause):
            # INDEX on columns
            text += ", ".join(
                self.sql_compiler.process(expr, include_table=False, literal_binds=True)
                for expr in index.expressions
            )
        else:
            # INDEX on expression
            text += "COMPUTED BY (%s)" % EXPRESSION_SEPARATOR.join(
                    self.sql_compiler.process(expr, include_table=False, literal_binds=True)
                    for expr in index.expressions
                )
        return text
    
    def post_create_table(self, table):
        table_opts = []
        fb_opts = table.dialect_options[self.dialect.name]

        if fb_opts["on_commit"]:
            on_commit_options = fb_opts["on_commit"].replace("_", " ").upper()
            table_opts.append("\n ON COMMIT %s" % on_commit_options)

        return "".join(table_opts)

    def visit_computed_column(self, generated, **kw):
        # TODO: Support GENERATED BY DEFAULT AS ...
        if generated.persisted is not None:
            raise exc.CompileError(
                "Firebird computed columns do not support a persistence "
                "method setting; set the 'persisted' flag to None for "
                "Firebird support."
            )
        return "GENERATED ALWAYS AS (%s)" % self.sql_compiler.process(
            generated.sqltext, include_table=False, literal_binds=True
        )
    
    def get_identity_options(self, identity_options):
        text = []
        if identity_options.start is not None:
            start = identity_options.start
            if self.dialect.server_version_info < (4,):
                # https://firebirdsql.org/file/documentation/release_notes/html/en/4_0/rlsnotes40.html#rnfb40-compat-sql-sequence-start-value
                start -= identity_options.increment if identity_options.increment is not None else 1
            text.append("START WITH %d" % start)
        if identity_options.increment is not None:
            text.append("INCREMENT BY %d" % identity_options.increment)
        return " ".join(text)


class FBTypeCompiler(compiler.GenericTypeCompiler):
    def visit_boolean(self, type_, **kw):
        if self.dialect.server_version_info < (3,):
            return self.visit_SMALLINT(type_, **kw)
        
        return self.visit_BOOLEAN(type_, **kw)

    def visit_datetime(self, type_, **kw):
        return self.visit_TIMESTAMP(type_, **kw)

    def visit_TEXT(self, type_, **kw):
        return "BLOB SUB_TYPE 1"

    def visit_BLOB(self, type_, **kw):
        return "BLOB SUB_TYPE 0"

    def _render_string_type(self, type_, name):
        text = name
        if type_.length:
            text += f"({type_.length})"

        charset = getattr(type_, "charset", None)
        if charset is not None:
            text += f" CHARACTER SET {charset}"

        if type_.collation:
            text += f" COLLATE {type_.collation}"
        return text

    def visit_VARCHAR(self, type_, **kw):
        if not type_.length:
            raise exc.CompileError(
                f"VARCHAR requires a length on dialect {self.dialect.name}."
            )
        return super().visit_VARCHAR(type_, **kw)

    def visit_TIMESTAMP(self, type_, **kw):
        if self.dialect.server_version_info < (4,):
            return super().visit_TIMESTAMP(type_, **kw)
        
        return "TIMESTAMP%s %s" % (
            "(%d)" % type_.precision
            if getattr(type_, "precision", None) is not None
            else "",
            (type_.timezone and "WITH" or "WITHOUT") + " TIME ZONE",
        )

    def visit_TIME(self, type_, **kw):
        if self.dialect.server_version_info < (4,):
            return super().visit_TIME(type_, **kw)
        
        return "TIME%s %s" % (
            "(%d)" % type_.precision
            if getattr(type_, "precision", None) is not None
            else "",
            (type_.timezone and "WITH" or "WITHOUT") + " TIME ZONE",
        )


class FBIdentifierPreparer(sql.compiler.IdentifierPreparer):
    """Install Firebird specific reserved words."""

    # reserved_words is updated when Firebird version is known
    reserved_words = RESERVED_WORDS_40

    illegal_initial_characters = compiler.ILLEGAL_INITIAL_CHARACTERS.union(
        ["_"]
    )


class FBExecutionContext(default.DefaultExecutionContext):
    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            (
                "SELECT GEN_ID(%s, 1) FROM rdb$database"
                % self.dialect.identifier_preparer.format_sequence(seq)
            ),
            type_,
        )


class FBDialect(default.DefaultDialect):
    max_identifier_length = 63

    supports_alter = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = False

    supports_native_boolean = True
    supports_native_decimal = True

    supports_schemas = False
    supports_sequences = True
    sequences_optional = False
    postfetch_lastrowid = False
    use_insertmanyvalues = False

    supports_comments = True
    inline_comments = False
    supports_default_values = True

    supports_default_metavalue = True

    supports_identity_columns = True

    ischema_names = ischema_names

    statement_compiler = FBCompiler
    ddl_compiler = FBDDLCompiler
    type_compiler_cls = FBTypeCompiler
    type_compiler = FBTypeCompiler    # For SQLAlchemy 1.4 compatibility only. Unneeded in 2.0.
    preparer = FBIdentifierPreparer
    execution_ctx_cls = FBExecutionContext

    update_returning = True
    delete_returning = True
    insert_returning = True

    requires_name_normalize = True
    supports_unicode_binds = True
    supports_empty_insert = False
    supports_is_distinct_from = True

    construct_arguments = [
        (
            sa_schema.Table, 
            {
                "on_commit": None,
            },
        ),
    ]

    using_sqlalchemy2 = version.parse(SQLALCHEMY_VERSION).major >= 2


    def initialize(self, connection):
        super().initialize(connection)

        # https://docs.sqlalchemy.org/en/20/core/engines.html
        # max_identifier_length defines ..."the maximum number of characters
        # that may be used in a SQL identifier such as a table_name, column
        # name, or label name".
        #
        # https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html
        # For Firebird version 4.0 and greater, the "...maximum identifier
        # length is 63 characters character set UTF8 (252 bytes)".
        #
        # https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref30/firebird-30-language-reference.html
        # "Length cannot exceed 31 bytes.  Identifiers are stored in character
        # set UNICODE_FSS, which means characters outside the ASCII range are
        # stored using 2 or 3 bytes."
        #
        # https://www.firebirdsql.org/file/documentation/release_notes/Firebird-5.0.0-Beta1-ReleaseNotes.pdf
        # Note that reserved words in Firebird 5 are the same as those in Firebird 4

        if self.server_version_info < (4,):
            self.max_identifier_length = 31
            self.preparer.reserved_words = RESERVED_WORDS_30

        if self.server_version_info < (3,):
            self.supports_native_boolean = False
            self.supports_identity_columns = False
            self.preparer.reserved_words = RESERVED_WORDS_25

    @reflection.cache
    def has_table(self, connection, table_name, schema=None, **kw):
        # Can't have a table whose name is too long.
        if len(table_name) > self.max_identifier_length:
            return False

        has_table_query = """
            SELECT 1 AS has_table
            FROM rdb$relations
            WHERE rdb$relation_name = ?
        """
        tablename = self.denormalize_name(table_name)
        c = connection.exec_driver_sql(has_table_query, (tablename, ))
        return c.first() is not None

    @reflection.cache
    def has_sequence(self, connection, sequence_name, schema=None, **kw):
        """Return ``True`` if the given sequence (generator) exists."""
        has_sequence_query = """
            SELECT 1 AS has_sequence 
            FROM rdb$generators
            WHERE rdb$generator_name = ?
        """
        c = connection.exec_driver_sql(
            has_sequence_query, 
            (self.denormalize_name(sequence_name),)
        )
        return c.first() is not None

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        tables_query = """
            SELECT TRIM(rdb$relation_name) AS relation_name
            FROM rdb$relations
            WHERE rdb$relation_type IN (0 /* TABLE */)
              AND COALESCE(rdb$system_flag, 0) = 0
            ORDER BY rdb$relation_name
        """

        return [
            self.normalize_name(row.relation_name)
            for row in connection.exec_driver_sql(tables_query)
        ]

    @reflection.cache
    def get_temp_table_names(self, connection, schema=None, **kw):
        temp_tables_query = """
            SELECT TRIM(rdb$relation_name) AS relation_name
            FROM rdb$relations
            WHERE rdb$relation_type IN (4 /* TEMPORARY_TABLE_PRESERVE */, 
                                        5 /* TEMPORARY_TABLE_DELETE */)
              AND COALESCE(rdb$system_flag, 0) = 0
            ORDER BY rdb$relation_name
        """
        return [
            self.normalize_name(row.relation_name)
            for row in connection.exec_driver_sql(temp_tables_query)
        ]

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        # see http://www.firebirdfaq.org/faq174/
        views_query = """
            SELECT TRIM(rdb$relation_name) AS relation_name
            FROM rdb$relations
            WHERE rdb$relation_type IN (1 /* VIEW */)
              AND COALESCE(rdb$system_flag, 0) = 0
            ORDER BY rdb$relation_name
        """
        return [
            self.normalize_name(row.relation_name)
            for row in connection.exec_driver_sql(views_query)
        ]

    @reflection.cache
    def get_sequence_names(self, connection, schema=None, **kw):
        sequences_query = """
            SELECT TRIM(rdb$generator_name) AS generator_name
            FROM rdb$generators
            WHERE COALESCE(rdb$system_flag, 0) = 0
        """
        # Do not need ORDER BY
        return [
            self.normalize_name(row.generator_name)
            for row in connection.exec_driver_sql(sequences_query)
        ]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        view_query = """
            SELECT rdb$view_source AS view_source
            FROM rdb$relations
            WHERE rdb$relation_type IN (1 /* VIEW */)
              AND rdb$relation_name = ?
        """
        c = connection.exec_driver_sql(
            view_query, 
			(self.denormalize_name(view_name), )
        )
        row = c.fetchone()
        if row:
            return row.view_source

        raise exc.NoSuchTableError(view_name)

    @reflection.cache
    def get_columns(  # noqa: C901
        self, connection, table_name, schema=None, **kw
    ):
        is_fb25 = self.server_version_info < (3,)
        # Query to extract the details of all the fields of the given table
        columns_query = """
            SELECT TRIM(r.rdb$field_name) AS fname,
                   r.rdb$null_flag AS null_flag,
                   t.rdb$type_name AS ftype,
                   f.rdb$field_sub_type AS stype,
                   f.rdb$field_length / COALESCE(cs.rdb$bytes_per_character, 1) AS flen,
                   f.rdb$field_precision AS fprec,
                   f.rdb$field_scale AS fscale,
                   COALESCE(r.rdb$default_source, f.rdb$default_source) AS fdefault,
                   TRIM(r.rdb$description) AS fcomment,
                   f.rdb$computed_source AS computed_source,
                   r.rdb$identity_type AS identity_type,
                   g.rdb$initial_value AS identity_start,
                   g.rdb$generator_increment AS identity_increment
            FROM rdb$relation_fields r
                 JOIN rdb$fields f
                   ON f.rdb$field_name = r.rdb$field_source
                 JOIN rdb$types t
                   ON t.rdb$type = f.rdb$field_type 
                  AND t.rdb$field_name = 'RDB$FIELD_TYPE'
                 LEFT JOIN rdb$character_sets cs
                        ON cs.rdb$character_set_id = f.rdb$character_set_id
                 LEFT JOIN rdb$generators g
                        ON g.rdb$generator_name = r.rdb$generator_name
            WHERE f.rdb$system_flag = 0 
              AND r.rdb$relation_name = ?
            ORDER BY r.rdb$field_position
        """

        if is_fb25: 
            # Firebird 2.5 doesn't have RDB$GENERATOR_NAME nor RDB$IDENTITY_TYPE in RDB$RELATION_FIELDS
            columns_query = """
                SELECT TRIM(r.rdb$field_name) AS fname,
                       r.rdb$null_flag AS null_flag,
                       t.rdb$type_name AS ftype,
                       f.rdb$field_sub_type AS stype,
                       f.rdb$field_length / COALESCE(cs.rdb$bytes_per_character, 1) AS flen,
                       f.rdb$field_precision AS fprec,
                       f.rdb$field_scale AS fscale,
                       COALESCE(r.rdb$default_source, f.rdb$default_source) AS fdefault,
                       TRIM(r.rdb$description) AS fcomment,
                       f.rdb$computed_source AS computed_source
                FROM rdb$relation_fields r
                     JOIN rdb$fields f 
                       ON f.rdb$field_name = r.rdb$field_source
                     JOIN rdb$types t
                       ON t.rdb$type = f.rdb$field_type
                      AND t.rdb$field_name = 'RDB$FIELD_TYPE'
                      LEFT JOIN rdb$character_sets cs
                             ON cs.rdb$character_set_id = f.rdb$character_set_id
                WHERE f.rdb$system_flag = 0
                  AND r.rdb$relation_name = ?
                ORDER BY r.rdb$field_position
            """ 

        tablename = self.denormalize_name(table_name)
        c = [row for row in connection.exec_driver_sql(columns_query, (tablename,))]

        cols = []
        for row in c:
            name = self.normalize_name(row.fname)

            # Extract data type
            colspec = row.ftype.rstrip()
            coltype = self.ischema_names.get(colspec)
            if coltype is None:
                util.warn(
                    "Did not recognize type '%s' of column '%s'"
                    % (colspec, name)
                )
                coltype = sqltypes.NULLTYPE
            elif issubclass(coltype, Integer) and row.fprec != 0:
                coltype = NUMERIC(precision=row.fprec, scale=row.fscale * -1)
            elif colspec in ("VARYING", "CSTRING"):
                coltype = coltype(row.flen)
            elif colspec == "TEXT":
                coltype = TEXT(row.flen)
            elif colspec == "BLOB":
                coltype = TEXT() if row.stype == 1 else BLOB()
            else:
                coltype = coltype()

            # Extract default value
            defvalue = None
            if row.fdefault is not None:
                # the value comes down as "DEFAULT 'value'": there may be
                # more than one whitespace around the "DEFAULT" keyword
                # and it may also be lower case
                # (see also http://tracker.firebirdsql.org/browse/CORE-356)
                defexpr = row.fdefault.lstrip()
                assert defexpr[:8].rstrip().upper() == "DEFAULT", (
                    "Unrecognized default value: %s" % defexpr
                )
                defvalue = defexpr[8:].strip()
                defvalue = defvalue if defvalue != "NULL" else None
                   
            col_d = {
                "name": name,
                "type": coltype,
                "nullable": not bool(row.null_flag),
                "default": defvalue
            }

            orig_colname = row.fname
            if orig_colname.lower() == orig_colname:
                col_d["quote"] = True

            if row.computed_source is not None:
                col_d["computed"] = {"sqltext": row.computed_source}

            if row.fcomment is not None:
                col_d["comment"] = row.fcomment

            if (not is_fb25) and row.identity_type is not None:
                col_d["identity"] = {
                    "always": row.identity_type == 0,
                    "start": row.identity_start,
                    "increment": row.identity_increment
                }

            if not self.using_sqlalchemy2:
                # For SQLAlchemy 1.4 compatibility only. Unneeded in 2.0.
                col_d["autoincrement"] = "auto"

            cols.append(col_d)

        if cols:
            return cols
        
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)
        
        return reflection.ReflectionDefaults.columns() if self.using_sqlalchemy2 else []

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        pk_query = """
            SELECT TRIM(se.rdb$field_name) AS fname
            FROM rdb$relation_constraints rc
                 JOIN rdb$index_segments se
                   ON se.rdb$index_name = rc.rdb$index_name
            WHERE rc.rdb$constraint_type = 'PRIMARY KEY'
              AND rc.rdb$relation_name = ?
            ORDER BY se.rdb$field_position
        """
        tablename = self.denormalize_name(table_name)
        c = connection.exec_driver_sql(pk_query, (tablename,))

        pkfields = [self.normalize_name(r.fname) for r in c.fetchall()]
        if pkfields:
            return {"constrained_columns": pkfields, "name": None}
        
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)

        return reflection.ReflectionDefaults.pk_constraint() if self.using_sqlalchemy2 else { "name": None, "constrained_columns": [] }

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        fk_query = """
            SELECT TRIM(rc.rdb$constraint_name) AS cname,
                   TRIM(cse.rdb$field_name) AS fname,
                   TRIM(ix2.rdb$relation_name) AS targetrname,
                   TRIM(se.rdb$field_name) AS targetfname,
                   TRIM(rfc.rdb$update_rule) AS update_rule,
                   TRIM(rfc.rdb$delete_rule) AS delete_rule
            FROM rdb$relation_constraints rc
                 JOIN rdb$ref_constraints rfc 
                   ON rfc.rdb$constraint_name = rc.rdb$constraint_name
                 JOIN rdb$indices ix1 
                   ON ix1.rdb$index_name=rc.rdb$index_name
                 JOIN rdb$indices ix2 
                   ON ix2.rdb$index_name=ix1.rdb$foreign_key
                 JOIN rdb$index_segments cse 
                   ON cse.rdb$index_name=ix1.rdb$index_name
                 JOIN rdb$index_segments se 
                   ON se.rdb$index_name=ix2.rdb$index_name
                  AND se.rdb$field_position=cse.rdb$field_position
            WHERE rc.rdb$constraint_type = 'FOREIGN KEY'
              AND rc.rdb$relation_name = ?
            ORDER BY rc.rdb$constraint_name, se.rdb$field_position
        """
        tablename = self.denormalize_name(table_name)
        c = connection.exec_driver_sql(fk_query, (tablename,))

        fks = util.defaultdict(
            lambda: {
                "name": None,
                "constrained_columns": [],
                "referred_schema": None,
                "referred_table": None,
                "referred_columns": [],
                "options": {}
            }
        )

        for row in c:
            cname = self.normalize_name(row.cname)
            fk = fks[cname]
            if not fk["name"]:
                fk["name"] = cname
                fk["referred_table"] = self.normalize_name(row.targetrname)
            fk["constrained_columns"].append(self.normalize_name(row.fname))
            fk["referred_columns"].append(self.normalize_name(row.targetfname))
            if row.update_rule not in ['NO ACTION', 'RESTRICT']:
                fk["options"]["onupdate"] = row.update_rule
            if row.delete_rule not in ['NO ACTION', 'RESTRICT']:
                fk["options"]["ondelete"] = row.delete_rule

        result = list(fks.values())
        if result:
            return result
        
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)
        
        return reflection.ReflectionDefaults.foreign_keys() if self.using_sqlalchemy2 else []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        indexes_query = """
            SELECT TRIM(ix.rdb$index_name) AS index_name,
                   ix.rdb$unique_flag AS unique_flag,
                   TRIM(ic.rdb$field_name) AS field_name,
                   TRIM(ix.rdb$expression_source) expression_source
            FROM rdb$indices ix
                LEFT OUTER JOIN rdb$index_segments ic
                  ON ic.rdb$index_name=ix.rdb$index_name
                LEFT OUTER JOIN rdb$relation_constraints rc
                             ON rc.rdb$index_name = ic.rdb$index_name
            WHERE ix.rdb$relation_name = :relation_name
              AND ix.rdb$foreign_key IS NULL
              AND COALESCE(rc.rdb$constraint_type, '') <> 'PRIMARY KEY'
            ORDER BY ix.rdb$index_name, ic.rdb$field_position
        """
        tablename = self.denormalize_name(table_name)

        # Do not use connection.exec_driver_sql() here. 
        #    During tests we need to commit CREATE INDEX before this query. See provision.py listener.
        c = connection.execute(text(indexes_query), { "relation_name": tablename })

        indexes = util.defaultdict(dict)
        for row in c:
            indexrec = indexes[row.index_name]
            if "name" not in indexrec:
                indexrec["name"] = self.normalize_name(row.index_name)
                indexrec["column_names"] = []
                indexrec["dialect_options"] = {}
                indexrec["unique"] = bool(row.unique_flag)
                if row.expression_source is not None:
                    expr = row.expression_source[1:-1]  # Remove outermost parenthesis added by Firebird
                    indexrec["expressions"] = expr.split(EXPRESSION_SEPARATOR)

            indexrec["column_names"].append(
                self.normalize_name(row.field_name)
            )

        def _get_column_set(tablename):
            colqry = """
                SELECT TRIM(r.rdb$field_name) AS fname
                FROM rdb$relation_fields r
                WHERE r.rdb$relation_name = ?
            """
            return {self.normalize_name(row.fname) 
                    for row in connection.exec_driver_sql(colqry, (tablename,))}

        def _adjust_column_names_for_expressions(result, tablename):
            # Identify which expression elements are columns
            colset = _get_column_set(tablename)
            for i in result:
                expr = i.get("expressions")
                if expr is not None:
                    i["column_names"] = [x if self.normalize_name(x) in colset else None 
                                         for x in expr]
            return result

        result = list(indexes.values())
        if result:
            return _adjust_column_names_for_expressions(result, tablename)
        
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)
        
        return reflection.ReflectionDefaults.indexes() if self.using_sqlalchemy2 else []

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        unique_constraints_query = """
            SELECT TRIM(rc.rdb$constraint_name) AS cname,
                   TRIM(se.rdb$field_name) AS column_name
            FROM rdb$index_segments se
                 JOIN rdb$relation_constraints rc
                   ON rc.rdb$index_name = se.rdb$index_name
                 JOIN rdb$relations r
                   ON r.rdb$relation_name = rc.rdb$relation_name
                  AND r.rdb$system_flag = 0
            WHERE rc.rdb$constraint_type = 'UNIQUE' AND
                  r.rdb$relation_name = ?
            ORDER BY rc.rdb$constraint_name, se.rdb$field_position
        """
        tablename = self.denormalize_name(table_name)
        c = connection.exec_driver_sql(unique_constraints_query, (tablename,))

        ucs = util.defaultdict(
            lambda: {
                "name": None,
                "column_names": []
            }
        )

        for row in c:
            cname = self.normalize_name(row.cname)
            cc = ucs[cname]
            if not cc["name"]:
                cc["name"] = cname
            cc["column_names"].append(self.normalize_name(row.column_name))

        result = list(ucs.values())
        if result:
            return result
        
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)
        
        return reflection.ReflectionDefaults.unique_constraints() if self.using_sqlalchemy2 else []

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, **kw):
        table_comment_query = """
            SELECT TRIM(rdb$description) AS comment
            FROM rdb$relations
            WHERE rdb$relation_name = ?
        """
        tablename = self.denormalize_name(table_name)        
        c = connection.exec_driver_sql(table_comment_query, (tablename,))
        
        row = c.fetchone()
        if row:
            return {"text": row[0]}

        raise exc.NoSuchTableError(table_name)

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        check_constraints_query = """
            SELECT TRIM(rc.rdb$constraint_name) AS cname,
                   TRIM(SUBSTRING(tr.rdb$trigger_source FROM 8 FOR CHAR_LENGTH(tr.rdb$trigger_source) - 8)) AS sqltext
            FROM rdb$relation_constraints rc
                 JOIN rdb$check_constraints ck
                   ON ck.rdb$constraint_name = rc.rdb$constraint_name
                 JOIN rdb$triggers tr
                   ON tr.rdb$trigger_name = ck.rdb$trigger_name AND
                      tr.rdb$trigger_type = 1 /* BEFORE UPDATE */
            WHERE rc.rdb$constraint_type = 'CHECK' AND
                  rc.rdb$relation_name = ?
            ORDER BY rc.rdb$constraint_name
        """
        tablename = self.denormalize_name(table_name)
        c = connection.exec_driver_sql(check_constraints_query, (tablename,))
        
        ccs = util.defaultdict(
            lambda: {
                "name": None,
                "sqltext": None,
            }
        )

        for row in c:
            cname = self.normalize_name(row.cname)
            cc = ccs[cname]
            if not cc["name"]:
                cc["name"] = cname
                cc["sqltext"] = row.sqltext

        result = list(ccs.values())
        if result:
            return result

        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(table_name)
                
        return reflection.ReflectionDefaults.check_constraints() if self.using_sqlalchemy2 else []

    def is_disconnect(self, e, connection, cursor):
        if isinstance(
            e, (self.dbapi.OperationalError, self.dbapi.ProgrammingError)
        ):
            # TODO: Review these messages for Firebird 3+
            for msg in (
                "Error writing data to the connection",
                "Unable to complete network request to host",
                "Invalid connection state",
                "Invalid cursor state",
                "connection shutdown",
            ):
                if msg in str(e):
                    return True

        return False
