from sqlalchemy import column
from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import schema
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import table
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy import Unicode
from sqlalchemy import update
from sqlalchemy import VARCHAR
from sqlalchemy.sql import sqltypes
from sqlalchemy.testing import assert_raises_message
from sqlalchemy.testing import AssertsCompiledSQL
from sqlalchemy.testing import fixtures

from sqlalchemy_firebird import fdb as firebird
from sqlalchemy_firebird import base as fb_base
from sqlalchemy_firebird.fdb import FBDialect_fdb


class CompileTest(fixtures.TablesTest, AssertsCompiledSQL):
    __dialect__ = FBDialect_fdb()

    def test_alias(self):
        t = table("sometable", column("col1"), column("col2"))
        s = select(t.alias())
        self.assert_compile(
            s,
            "SELECT sometable_1.col1, sometable_1.col2 "
            "FROM sometable AS sometable_1",
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
                dialect=self.__dialect__,
            )

            t1 = Table("sometable", MetaData(), Column("somecolumn", type_))
            assert_raises_message(
                exc.CompileError,
                r"\(in table 'sometable', column 'somecolumn'\)\: "
                r"(?:N)?VARCHAR requires a length on dialect firebird",
                schema.CreateTable(t1).compile,
                dialect=self.__dialect__,
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
            select(func.max(t.c.col1)),
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
        u = (
            update(table1)
            .values(dict(name="foo"))
            .returning(table1.c.myid, table1.c.name)
        )
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "mytable.myid, mytable.name",
        )
        u = update(table1).values(dict(name="foo")).returning(table1)
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "mytable.myid, mytable.name, "
            "mytable.description",
        )
        u = (
            update(table1)
            .values(dict(name="foo"))
            .returning(func.length(table1.c.name))
        )
        self.assert_compile(
            u,
            "UPDATE mytable SET name=:name RETURNING "
            "CHAR_LENGTH(mytable.name) AS length_1",
        )

    def test_insert_returning(self):
        table1 = table(
            "mytable",
            column("myid", Integer),
            column("name", String(128)),
            column("description", String(128)),
        )
        i = (
            insert(table1)
            .values(dict(name="foo"))
            .returning(table1.c.myid, table1.c.name)
        )
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING mytable.myid, mytable.name",
        )
        i = insert(table1).values(dict(name="foo")).returning(table1)
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING mytable.myid, mytable.name, "
            "mytable.description",
        )
        i = (
            insert(table1)
            .values(dict(name="foo"))
            .returning(func.length(table1.c.name))
        )
        self.assert_compile(
            i,
            "INSERT INTO mytable (name) VALUES (:name) "
            "RETURNING CHAR_LENGTH(mytable.name) AS "
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
