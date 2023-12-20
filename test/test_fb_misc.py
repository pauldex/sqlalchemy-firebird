from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy import text
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures


class MiscTest(fixtures.TestBase):
    @testing.provide_metadata
    def test_strlen(self, connection):
        metadata = self.metadata

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
            connection.execute(select(func.count(t.c.id)).where(func.length(t.c.name) == 5)).scalar(),
            1,
        )

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
