import pytest
from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import exc
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import schema
from sqlalchemy import select
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy import text
from sqlalchemy import types as sqltypes
from sqlalchemy import Unicode
from sqlalchemy import update
from sqlalchemy import VARCHAR
from sqlalchemy_firebird import fdb as firebird
from sqlalchemy_firebird import base as fb_base
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql import column
from sqlalchemy.sql import table
from sqlalchemy.testing import assert_raises_message
from sqlalchemy.testing import AssertsCompiledSQL
from sqlalchemy.testing import AssertsExecutionResults
from sqlalchemy.testing import engines
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures
from sqlalchemy.testing.mock import call
from sqlalchemy.testing.mock import Mock
from sqlalchemy.testing.suite import *
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import TableDDLTest as _TableDDLTest
from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
)


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.skip()
    def test_autoclose_on_insert(self):
        # TODO: investigate why when the real test fails it hangs the test
        #       run on class teardown (after `DROP TABLE autoinc_pk`)
        return


class TableDDLTest(_TableDDLTest):
    @pytest.mark.skip()
    def test_create_table_schema(self):
        """Do not test schemas

        In Firebird, a schema is the same thing as a database.  According to
        the Firebird reference manual, "The CREATE DATABASE statement creates
        a new database. You can use CREATE DATABASE or CREATE SCHEMA. They are
        synonymous."  See:
        https://firebirdsql.org/file/documentation/reference_manuals/fblangref25-en/html/fblangref25-ddl-db.html
        """
        return


class ComponentReflectionTest(_ComponentReflectionTest):
    @pytest.mark.skip()
    def test_get_comments(self):
        """
        test asserts a comment is on COMMENT_TABLE

        I'm not able to find where a comment is associated with this table.
        Skip this one for now...
        """
        return


class CompoundSelectTest(_CompoundSelectTest):
    """
    Firebird requires ORDER BY column position number for UNIONs
    """

    @pytest.mark.skip()
    def test_plain_union(self):
        return

    @pytest.mark.skip()
    def test_distinct_selectable_in_unions(self):
        return

    @pytest.mark.skip()
    def test_limit_offset_aliased_selectable_in_unions(self):
        return


class DomainReflectionTest(fixtures.TestBase, AssertsExecutionResults):
    "Test Firebird domains"

    __only_on__ = "firebird"

    @classmethod
    def setup_class(cls):
        con = testing.db.connect()
        try:
            con.execute(
                "CREATE DOMAIN int_domain AS INTEGER DEFAULT " "42 NOT NULL"
            )
            con.execute("CREATE DOMAIN str_domain AS VARCHAR(255)")
            con.execute("CREATE DOMAIN rem_domain AS BLOB SUB_TYPE TEXT")
            con.execute("CREATE DOMAIN img_domain AS BLOB SUB_TYPE " "BINARY")
        except ProgrammingError as e:
            if "attempt to store duplicate value" not in str(e):
                raise e
        con.execute("""CREATE GENERATOR gen_testtable_id""")
        con.execute(
            """CREATE TABLE testtable (question int_domain,
                                   answer str_domain DEFAULT 'no answer',
                                   remark rem_domain DEFAULT '',
                                   photo img_domain,
                                   d date,
                                   t time,
                                   dt timestamp,
                                   redundant str_domain DEFAULT NULL)"""
        )
        con.execute(
            "ALTER TABLE testtable "
            "ADD CONSTRAINT testtable_pk PRIMARY KEY "
            "(question)"
        )
        con.execute(
            "CREATE TRIGGER testtable_autoid FOR testtable "
            "   ACTIVE BEFORE INSERT AS"
            "   BEGIN"
            "     IF (NEW.question IS NULL) THEN"
            "       NEW.question = gen_id(gen_testtable_id, 1);"
            "   END"
        )

    @classmethod
    def teardown_class(cls):
        con = testing.db.connect()
        con.execute("DROP TABLE testtable")
        con.execute("DROP DOMAIN int_domain")
        con.execute("DROP DOMAIN str_domain")
        con.execute("DROP DOMAIN rem_domain")
        con.execute("DROP DOMAIN img_domain")
        con.execute("DROP GENERATOR gen_testtable_id")

    def test_table_is_reflected(self):
        from sqlalchemy.types import (
            Integer,
            Text,
            BLOB,
            String,
            Date,
            Time,
            DateTime,
        )

        metadata = MetaData(testing.db)
        table = Table("testtable", metadata, autoload=True)
        eq_(
            set(table.columns.keys()),
            set(
                [
                    "question",
                    "answer",
                    "remark",
                    "photo",
                    "d",
                    "t",
                    "dt",
                    "redundant",
                ]
            ),
            "Columns of reflected table didn't equal expected " "columns",
        )
        eq_(table.c.question.primary_key, True)

        # disabled per http://www.sqlalchemy.org/trac/ticket/1660
        # eq_(table.c.question.sequence.name, 'gen_testtable_id')

        assert isinstance(table.c.question.type, Integer)
        eq_(table.c.question.server_default.arg.text, "42")
        assert isinstance(table.c.answer.type, String)
        assert table.c.answer.type.length == 255
        eq_(table.c.answer.server_default.arg.text, "'no answer'")
        assert isinstance(table.c.remark.type, Text)
        eq_(table.c.remark.server_default.arg.text, "''")
        assert isinstance(table.c.photo.type, BLOB)
        assert table.c.redundant.server_default is None

        # The following assume a Dialect 3 database

        assert isinstance(table.c.d.type, Date)
        assert isinstance(table.c.t.type, Time)
        assert isinstance(table.c.dt.type, DateTime)


class CompileTest(fixtures.TablesTest, AssertsCompiledSQL):

    __dialect__ = firebird.FBDialect_fdb()

    def test_alias(self):
        t = table("sometable", column("col1"), column("col2"))
        s = select([t.alias()])
        self.assert_compile(
            s,
            "SELECT sometable_1.col1, sometable_1.col2 "
            "FROM sometable AS sometable_1",
        )
        dialect = self.__dialect__
        dialect._version_two = False
        self.assert_compile(
            s,
            "SELECT sometable_1.col1, sometable_1.col2 "
            "FROM sometable sometable_1",
            dialect=dialect,
        )

    def test_varchar_raise(self):
        for type_ in (
            String,
            VARCHAR,
            String(),
            VARCHAR(),
            Unicode,
            Unicode(),
        ):
            type_ = sqltypes.to_instance(type_)
            assert_raises_message(
                exc.CompileError,
                "VARCHAR requires a length on dialect firebird",
                type_.compile,
                dialect=firebird.dialect(),
            )

            t1 = Table("sometable", MetaData(), Column("somecolumn", type_))
            assert_raises_message(
                exc.CompileError,
                r"\(in table 'sometable', column 'somecolumn'\)\: "
                r"(?:N)?VARCHAR requires a length on dialect firebird",
                schema.CreateTable(t1).compile,
                dialect=firebird.dialect(),
            )

    @testing.provide_metadata
    def test_function(self):
        self.assert_compile(func.foo(1, 2), "foo(:foo_1, :foo_2)")
        self.assert_compile(func.current_time(), "CURRENT_TIME")
        self.assert_compile(func.foo(), "foo")
        t = Table(
            "sometable",
            self.metadata,
            Column("col1", Integer),
            Column("col2", Integer),
        )
        self.assert_compile(
            select([func.max(t.c.col1)]),
            "SELECT max(sometable.col1) AS max_1 FROM " "sometable",
        )

    def test_substring(self):
        self.assert_compile(
            func.substring("abc", 1, 2),
            "SUBSTRING(:substring_1 FROM :substring_2 " "FOR :substring_3)",
        )
        self.assert_compile(
            func.substring("abc", 1),
            "SUBSTRING(:substring_1 FROM :substring_2)",
        )

    def test_update_returning(self):
        table1 = table(
            "mytable",
            column("myid", Integer),
            column("name", String(128)),
            column("description", String(128)),
        )
        u = update(table1, values=dict(name="foo")).returning(
            table1.c.myid, table1.c.name
        )
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "mytable.myid, mytable.name",
        )
        u = update(table1, values=dict(name="foo")).returning(table1)
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "mytable.myid, mytable.name, "
            "mytable.description",
        )
        u = update(table1, values=dict(name="foo")).returning(
            func.length(table1.c.name)
        )
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "char_length(mytable.name) AS length_1",
        )

    def test_insert_returning(self):
        table1 = table(
            "mytable",
            column("myid", Integer),
            column("name", String(128)),
            column("description", String(128)),
        )
        i = insert(table1, values=dict(name="foo")).returning(
            table1.c.myid, table1.c.name
        )
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING mytable.myid, mytable.name",
        )
        i = insert(table1, values=dict(name="foo")).returning(table1)
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING mytable.myid, mytable.name, "
            "mytable.description",
        )
        i = insert(table1, values=dict(name="foo")).returning(
            func.length(table1.c.name)
        )
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING char_length(mytable.name) AS "
            "length_1",
        )

    def test_charset(self):
        """Exercise CHARACTER SET  options on string types."""

        columns = [
            (fb_base.CHAR, [1], {}, "CHAR(1)"),
            (
                fb_base.CHAR,
                [1],
                {"charset": "OCTETS"},
                "CHAR(1) CHARACTER SET OCTETS",
            ),
            (fb_base.VARCHAR, [1], {}, "VARCHAR(1)"),
            (
                fb_base.VARCHAR,
                [1],
                {"charset": "OCTETS"},
                "VARCHAR(1) CHARACTER SET OCTETS",
            ),
        ]
        for type_, args, kw, res in columns:
            self.assert_compile(type_(*args, **kw), res)

    def test_quoting_initial_chars(self):
        self.assert_compile(column("_somecol"), '"_somecol"')
        self.assert_compile(column("$somecol"), '"$somecol"')

    @testing.provide_metadata
    @testing.combinations(
        ("no_persisted", "ignore"), ("persisted_none", None), id_="ia"
    )
    def test_column_computed(self, persisted):
        kwargs = {"persisted": persisted} if persisted != "ignore" else {}
        t = Table(
            "t",
            self.metadata,
            Column("x", Integer),
            Column("y", Integer, Computed("x + 2", **kwargs)),
        )
        self.assert_compile(
            schema.CreateTable(t),
            "CREATE TABLE t (x INTEGER, y INTEGER GENERATED "
            "ALWAYS AS (x + 2))",
        )

    @testing.provide_metadata
    @testing.combinations(
        ("persisted_true", True), ("persisted_false", False), id_="ia"
    )
    def test_column_computed_raises(self, persisted):
        t = Table(
            "t",
            self.metadata,
            Column("x", Integer),
            Column("y", Integer, Computed("x + 2", persisted=persisted)),
        )
        assert_raises_message(
            exc.CompileError,
            "Firebird computed columns do not support a persistence method",
            schema.CreateTable(t).compile,
            dialect=firebird.dialect(),
        )


class TypesTest(fixtures.TestBase):
    __only_on__ = "firebird"

    @testing.provide_metadata
    def test_infinite_float(self, connection):
        metadata = self.metadata
        t = Table("t", metadata, Column("data", Float))
        metadata.create_all()
        connection.execute(t.insert(), data=float("inf"))
        eq_(connection.execute(t.select()).fetchall(), [(float("inf"),)])


class MiscTest(fixtures.TestBase):

    __only_on__ = "firebird"

    @testing.provide_metadata
    def test_strlen(self, connection):
        metadata = self.metadata

        # On FB the length() function is implemented by an external UDF,
        # strlen().  Various SA tests fail because they pass a parameter
        # to it, and that does not work (it always results the maximum
        # string length the UDF was declared to accept). This test
        # checks that at least it works ok in other cases.

        t = Table(
            "t1",
            metadata,
            Column("id", Integer, Sequence("t1idseq"), primary_key=True),
            Column("name", String(10)),
        )
        metadata.create_all()
        connection.execute(t.insert(values=dict(name="dante")))
        connection.execute(t.insert(values=dict(name="alighieri")))
        connection.execute(
            select([func.count(t.c.id)], func.length(t.c.name) == 5)
        ).first()[0] == 1

    def test_version_parsing(self):
        for string, result in [
            ("WI-V1.5.0.1234 Firebird 1.5", (1, 5, 1234, "firebird")),
            ("UI-V6.3.2.18118 Firebird 2.1", (2, 1, 18118, "firebird")),
            ("LI-V6.3.3.12981 Firebird 2.0", (2, 0, 12981, "firebird")),
            ("WI-V8.1.1.333", (8, 1, 1, "interbase")),
            ("WI-V8.1.1.333 Firebird 1.5", (1, 5, 333, "firebird")),
        ]:
            eq_(testing.db.dialect._parse_version_info(string), result)

    @testing.provide_metadata
    def test_rowcount_flag(self):
        metadata = self.metadata
        engine = engines.testing_engine(options={"enable_rowcount": True})
        assert engine.dialect.supports_sane_rowcount
        metadata.bind = engine
        t = Table("t1", metadata, Column("data", String(10)))
        metadata.create_all()
        with engine.begin() as conn:
            r = conn.execute(
                t.insert(), {"data": "d1"}, {"data": "d2"}, {"data": "d3"}
            )
            r = conn.execute(
                t.update().where(t.c.data == "d2").values(data="d3")
            )
            eq_(r.rowcount, 1)
            r = conn.execute(t.delete().where(t.c.data == "d3"))
            eq_(r.rowcount, 2)
            r = conn.execute(
                t.delete().execution_options(enable_rowcount=False)
            )
            eq_(r.rowcount, -1)
        engine.dispose()
        engine = engines.testing_engine(options={"enable_rowcount": False})
        assert not engine.dialect.supports_sane_rowcount
        metadata.bind = engine
        with engine.begin() as conn:
            r = conn.execute(
                t.insert(), {"data": "d1"}, {"data": "d2"}, {"data": "d3"}
            )
            r = conn.execute(
                t.update().where(t.c.data == "d2").values(data="d3")
            )
            eq_(r.rowcount, -1)
            r = conn.execute(t.delete().where(t.c.data == "d3"))
            eq_(r.rowcount, -1)
            r = conn.execute(
                t.delete().execution_options(enable_rowcount=True)
            )
            eq_(r.rowcount, 1)
        engine.dispose()

    def test_percents_in_text(self, connection):
        for expr, result in (
            (text("select '%' from rdb$database"), "%"),
            (text("select '%%' from rdb$database"), "%%"),
            (text("select '%%%' from rdb$database"), "%%%"),
            (
                text("select 'hello % world' from rdb$database"),
                "hello % world",
            ),
        ):
            eq_(connection.scalar(expr), result)


class ArgumentTest(fixtures.TestBase):
    def _dbapi(self):
        return Mock(
            paramstyle="qmark",
            connect=Mock(
                return_value=Mock(
                    server_version="UI-V6.3.2.18118 Firebird 2.1",
                    cursor=Mock(return_value=Mock()),
                )
            ),
        )

    def _engine(self, **kw):
        dbapi = self._dbapi()
        kw.update(dict(module=dbapi, _initialize=False))
        engine = engines.testing_engine("firebird://", options=kw)
        return engine

    def test_retaining_flag_default_fdb(self):
        engine = self._engine()
        self._assert_retaining(engine, False)

    def test_retaining_flag_true_fdb(self):
        engine = self._engine(retaining=True)
        self._assert_retaining(engine, True)

    def test_retaining_flag_false_fdb(self):
        engine = self._engine(retaining=False)
        self._assert_retaining(engine, False)

    def _assert_retaining(self, engine, flag):
        conn = engine.connect()
        trans = conn.begin()
        trans.commit()
        eq_(
            engine.dialect.dbapi.connect.return_value.commit.mock_calls,
            [call(flag)],
        )

        trans = conn.begin()
        trans.rollback()
        eq_(
            engine.dialect.dbapi.connect.return_value.rollback.mock_calls,
            [call(flag)],
        )
