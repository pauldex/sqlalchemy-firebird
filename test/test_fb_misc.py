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

    def test_is_disconnect(self, connection):
        try:
            with testing.db.begin() as first_conn:
                con1_id = first_conn.exec_driver_sql(
                    "SELECT CURRENT_CONNECTION FROM rdb$database"
                ).scalar()

                with testing.db.begin() as second_conn:
                    # Kills first_conn
                    second_conn.exec_driver_sql(
                        "DELETE FROM mon$attachments WHERE mon$attachment_id = ?",
                        (con1_id,),
                    )

                # Attemps to read from first_conn
                first_conn.exec_driver_sql(
                    "SELECT CURRENT_CONNECTION FROM rdb$database"
                )

                assert False
        except Exception as err:
            eq_(testing.db.dialect.is_disconnect(err.orig, None, None), True)
