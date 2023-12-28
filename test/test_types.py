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


TEST_CHARSET = "UTF8"
TEST_COLLATION = "UNICODE_CI"


def eq_col(col: Column, expected_type, **expected_options):
    is_instance_of(col.type, expected_type)

    if expected_options:
        for k, v in expected_options.items():
            actual = getattr(col.type, k, None)
            is_not_none(actual, f'"{col}" type does not have "{k}".')
            eq_(actual, v)


class TypesTest(fixtures.TestBase):
    @testing.provide_metadata
    def test_infinite_float(self, connection):
        t = Table("test_infinite_float", self.metadata, Column("data", Float))
        self.metadata.create_all(testing.db)
        connection.execute(t.insert(), dict(data=float("inf")))
        eq_(connection.execute(t.select()).fetchall(), [(float("inf"),)])

    @testing.provide_metadata
    def test_blob_types(self, connection):
        t = Table(
            "test_blob_types",
            self.metadata,
            Column("b", sa_types.BLOB()),
            Column("fb", fb_types._FBBLOB()),
            Column("fbs", fb_types._FBBLOB(segment_size=100)),
            Column("t", sa_types.TEXT()),
            Column("ft", fb_types._FBTEXT()),
            Column("fts", fb_types._FBTEXT(segment_size=200)),
            Column("ftc", fb_types._FBTEXT(charset=TEST_CHARSET)),
            Column(
                "ftcc",
                fb_types._FBTEXT(
                    charset=TEST_CHARSET, collation=TEST_COLLATION
                ),
            ),
        )
        self.metadata.create_all(testing.db)

        rm = MetaData()
        rt = Table("test_blob_types", rm, autoload_with=testing.db)

        eq_col(rt.columns["b"], fb_types._FBBLOB)
        eq_col(rt.columns["fb"], fb_types._FBBLOB)
        eq_col(rt.columns["fbs"], fb_types._FBBLOB, segment_size=100)
        eq_col(rt.columns["t"], sa_types.TEXT)
        eq_col(rt.columns["ft"], fb_types._FBTEXT)
        eq_col(rt.columns["fts"], fb_types._FBTEXT, segment_size=200)
        eq_col(rt.columns["ftc"], fb_types._FBTEXT, charset=TEST_CHARSET)
        eq_col(
            rt.columns["ftcc"],
            fb_types._FBTEXT,
            charset=TEST_CHARSET,
            collation=TEST_COLLATION,
        )

    @testing.provide_metadata
    def test_character_types(self, connection):
        t = Table(
            "test_character_types",
            self.metadata,
            Column("c", sa_types.CHAR()),
            Column("cl", sa_types.CHAR(length=10)),
            Column("nc", sa_types.NCHAR()),
            Column("ncl", sa_types.NCHAR(length=11)),
            Column("vc", sa_types.VARCHAR()),
            Column("vcl", sa_types.VARCHAR(length=12)),
            Column("nvc", sa_types.NVARCHAR()),
            Column("nvcl", sa_types.NVARCHAR(length=13)),
            Column("fc", fb_types._FBCHAR()),
            Column("fcl", fb_types._FBCHAR(length=20)),
            Column("fclc", fb_types._FBCHAR(length=21, charset=TEST_CHARSET)),
            Column(
                "fclcc",
                fb_types._FBCHAR(
                    length=22, charset=TEST_CHARSET, collation=TEST_COLLATION
                ),
            ),
            Column("fb", fb_types._FBBINARY()),
            Column("fbl", fb_types._FBBINARY(length=31)),
            Column("fnc", fb_types._FBNCHAR()),
            Column("fncl", fb_types._FBNCHAR(length=32)),
            Column("fvc", fb_types._FBVARCHAR()),
            Column("fvcl", fb_types._FBVARCHAR(length=33)),
            Column(
                "fvclc", fb_types._FBVARCHAR(length=34, charset=TEST_CHARSET)
            ),
            Column(
                "fvclcc",
                fb_types._FBVARCHAR(
                    length=35, charset=TEST_CHARSET, collation=TEST_COLLATION
                ),
            ),
            Column("fvb", fb_types._FBVARBINARY()),
            Column("fvbl", fb_types._FBVARBINARY(length=36)),
            Column("fnvc", fb_types._FBNVARCHAR()),
            Column("fnvcl", fb_types._FBNVARCHAR(length=37)),
        )
        self.metadata.create_all(testing.db)

        rm = MetaData()
        rt = Table("test_character_types", rm, autoload_with=testing.db)

        eq_col(rt.columns["c"], fb_types._FBCHAR),
        eq_col(rt.columns["cl"], fb_types._FBCHAR, length=10),
        eq_col(rt.columns["nc"], fb_types._FBNCHAR),
        eq_col(rt.columns["ncl"], fb_types._FBNCHAR, length=11),
        eq_col(rt.columns["vc"], fb_types._FBTEXT),
        eq_col(rt.columns["vcl"], fb_types._FBVARCHAR, length=12),
        eq_col(
            rt.columns["nvc"],
            fb_types._FBTEXT,
            charset=fb_types.NATIONAL_CHARSET,
        ),
        eq_col(rt.columns["nvcl"], fb_types._FBNVARCHAR, length=13),
        eq_col(rt.columns["fc"], fb_types._FBCHAR),
        eq_col(rt.columns["fcl"], fb_types._FBCHAR, length=20),
        eq_col(
            rt.columns["fclc"],
            fb_types._FBCHAR,
            length=21,
            charset=TEST_CHARSET,
        ),
        eq_col(
            rt.columns["fclcc"],
            fb_types._FBCHAR,
            length=22,
            charset=TEST_CHARSET,
            collation=TEST_COLLATION,
        ),
        eq_col(rt.columns["fb"], fb_types._FBBINARY),
        eq_col(rt.columns["fbl"], fb_types._FBBINARY, length=31),
        eq_col(rt.columns["fnc"], fb_types._FBNCHAR),
        eq_col(rt.columns["fncl"], fb_types._FBNCHAR, length=32),
        eq_col(rt.columns["fvc"], fb_types._FBTEXT, charset=TEST_CHARSET)
        eq_col(rt.columns["fvcl"], fb_types._FBVARCHAR, length=33),
        eq_col(
            rt.columns["fvclc"],
            fb_types._FBVARCHAR,
            length=34,
            charset=TEST_CHARSET,
        ),
        eq_col(
            rt.columns["fvclcc"],
            fb_types._FBVARCHAR,
            length=35,
            charset=TEST_CHARSET,
            collation=TEST_COLLATION,
        ),
        eq_col(
            rt.columns["fvb"],
            fb_types._FBTEXT,
            charset=fb_types.BINARY_CHARSET,
        )
        eq_col(rt.columns["fvbl"], fb_types._FBVARBINARY, length=36),
        eq_col(
            rt.columns["fnvc"],
            fb_types._FBTEXT,
            charset=fb_types.NATIONAL_CHARSET,
        )
        eq_col(rt.columns["fnvcl"], fb_types._FBNVARCHAR, length=37),

    @testing.provide_metadata
    def test_integer_types(self, connection):
        is_firebird_5_or_higher = testing.requires.firebird_5_or_higher.enabled
        large_int_type = (
            fb_types._FBINT128
            if is_firebird_5_or_higher
            else fb_types._FBBIGINT
        )

        t = Table(
            "test_integer_types",
            self.metadata,
            Column("si", sa_types.SMALLINT),
            Column("i", sa_types.INTEGER),
            Column("bi", sa_types.BIGINT),
            Column("fsi", fb_types._FBSMALLINT),
            Column("fi", fb_types._FBINTEGER),
            Column("fbi", fb_types._FBBIGINT),
            Column("fli", large_int_type),
        )
        self.metadata.create_all(testing.db)

        rm = MetaData()
        rt = Table("test_integer_types", rm, autoload_with=testing.db)

        eq_col(rt.columns["si"], fb_types._FBSMALLINT),
        eq_col(rt.columns["i"], fb_types._FBINTEGER),
        eq_col(rt.columns["bi"], fb_types._FBBIGINT),
        eq_col(rt.columns["fsi"], fb_types._FBSMALLINT),
        eq_col(rt.columns["fi"], fb_types._FBINTEGER),
        eq_col(rt.columns["fbi"], fb_types._FBBIGINT),
        eq_col(rt.columns["fli"], large_int_type),
