from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.testing import AssertsExecutionResults
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures


class DomainReflectionTest(fixtures.TestBase, AssertsExecutionResults):
    """Test Firebird domains"""

    __only_on__ = "firebird"

    @classmethod
    def setup_class(cls):
        with testing.db.begin() as con:
            try:
                con.exec_driver_sql(
                    "CREATE DOMAIN int_domain AS INTEGER DEFAULT "
                    "42 NOT NULL"
                )
                con.exec_driver_sql("CREATE DOMAIN str_domain AS VARCHAR(255)")
                con.exec_driver_sql(
                    "CREATE DOMAIN rem_domain AS BLOB SUB_TYPE TEXT"
                )
                con.exec_driver_sql(
                    "CREATE DOMAIN img_domain AS BLOB SUB_TYPE " "BINARY"
                )
            except ProgrammingError as e:
                if "attempt to store duplicate value" not in str(e):
                    raise e
            con.exec_driver_sql("""CREATE GENERATOR gen_testtable_id""")
            con.exec_driver_sql(
                """CREATE TABLE testtable (question int_domain,
                                       answer str_domain DEFAULT 'no answer',
                                       remark rem_domain DEFAULT '',
                                       photo img_domain,
                                       d date,
                                       t time,
                                       dt timestamp,
                                       redundant str_domain DEFAULT NULL)"""
            )
            con.exec_driver_sql(
                "ALTER TABLE testtable "
                "ADD CONSTRAINT testtable_pk PRIMARY KEY "
                "(question)"
            )
            con.exec_driver_sql(
                "CREATE TRIGGER testtable_autoid FOR testtable "
                "   ACTIVE BEFORE INSERT AS"
                "   BEGIN"
                "     IF (NEW.question IS NULL) THEN"
                "       NEW.question = gen_id(gen_testtable_id, 1);"
                "   END"
            )

    @classmethod
    def teardown_class(cls):
        with testing.db.begin() as con:
            con.exec_driver_sql("DROP TABLE testtable")
            con.exec_driver_sql("DROP DOMAIN int_domain")
            con.exec_driver_sql("DROP DOMAIN str_domain")
            con.exec_driver_sql("DROP DOMAIN rem_domain")
            con.exec_driver_sql("DROP DOMAIN img_domain")
            con.exec_driver_sql("DROP GENERATOR gen_testtable_id")

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

        metadata = MetaData()
        table = Table("testtable", metadata, autoload_with=testing.db)
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
