from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy import text
from sqlalchemy.testing import engines
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures


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
        metadata.create_all(testing.db)
        connection.execute(t.insert().values(dict(name="dante")))
        connection.execute(t.insert().values(dict(name="alighieri")))
        eq_(
            connection.execute(
                select(func.count(t.c.id)).where(func.length(t.c.name) == 5)
            ).scalar(),
            1,
        )

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
        t = Table("t1", metadata, Column("data", String(10)))
        metadata.create_all(engine)
        with engine.begin() as conn:
            r = conn.execute(
                t.insert(), [{"data": "d1"}, {"data": "d2"}, {"data": "d3"}]
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
                t.insert(), [{"data": "d1"}, {"data": "d2"}, {"data": "d3"}]
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
