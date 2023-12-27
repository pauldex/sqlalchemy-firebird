from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures
from sqlalchemy.testing import is_instance_of
from sqlalchemy.testing import is_not_none

import sqlalchemy.types as sa_types
import sqlalchemy_firebird.types as fb_types


class TypesTest(fixtures.TestBase):
    @testing.provide_metadata
    def test_infinite_float(self, connection):
        metadata = self.metadata
        t = Table("t", metadata, Column("data", Float))
        metadata.create_all(testing.db)
        connection.execute(t.insert(), dict(data=float("inf")))
        eq_(connection.execute(t.select()).fetchall(), [(float("inf"),)])

    @testing.provide_metadata
    def test_blob_options(self, connection):
        def assert_column(col: Column, expected_type, **expected_options):
            is_instance_of(col.type, expected_type)

            if expected_options:
                for k, v in expected_options.items():
                    actual = getattr(col.type, k, None)
                    is_not_none(actual, f'"{col}" type does not have "{k}".')
                    eq_(actual, v)

        metadata = self.metadata
        t = Table(
            "test_blob_options",
            metadata,
            Column("b", sa_types.BLOB()),
            Column("fb", fb_types._FBBLOB()),
            Column("fbs", fb_types._FBBLOB(segment_size=100)),
            Column("t", sa_types.TEXT()),
            Column("ft", fb_types._FBTEXT()),
            Column("fts", fb_types._FBTEXT(segment_size=200)),
            Column("ftc", fb_types._FBTEXT(charset="ISO8859_1")),
            Column(
                "ftcc",
                fb_types._FBTEXT(charset="ISO8859_1", collation="PT_BR"),
            ),
        )
        metadata.create_all(testing.db)

        m2 = MetaData()
        rt = Table("test_blob_options", m2, autoload_with=testing.db)

        assert_column(rt.columns["b"], fb_types._FBBLOB)
        assert_column(rt.columns["fb"], fb_types._FBBLOB)
        assert_column(rt.columns["fbs"], fb_types._FBBLOB, segment_size=100)

        assert_column(rt.columns["t"], sa_types.TEXT)
        assert_column(rt.columns["ft"], fb_types._FBTEXT)
        assert_column(rt.columns["fts"], fb_types._FBTEXT, segment_size=200)
        assert_column(rt.columns["ftc"], fb_types._FBTEXT, charset="ISO8859_1")
        assert_column(
            rt.columns["ftcc"],
            fb_types._FBTEXT,
            charset="ISO8859_1",
            collation="PT_BR",
        )
