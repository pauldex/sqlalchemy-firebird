from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Table
from sqlalchemy import testing
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures


class TypesTest(fixtures.TestBase):
    __only_on__ = "firebird"

    @testing.provide_metadata
    def test_infinite_float(self, connection):
        metadata = self.metadata
        t = Table("t", metadata, Column("data", Float))
        metadata.create_all(testing.db)
        connection.execute(t.insert(), dict(data=float("inf")))
        eq_(connection.execute(t.select()).fetchall(), [(float("inf"),)])
