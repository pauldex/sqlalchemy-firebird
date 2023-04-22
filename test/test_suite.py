import pytest

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest

from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
from sqlalchemy.testing.suite import DateTimeTZTest as _DateTimeTZTest
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import RowCountTest as _RowCountTest


@pytest.mark.skip(
    reason="These tests fails in Firebird because a DELETE FROM <table> with self-referencing FK raises integrity errors."
)
class CTETest(_CTETest):
    pass


@pytest.mark.skip(reason="These tests hangs in Firebird 2.5.")
class InsertBehaviorTest(_InsertBehaviorTest):
    pass


@pytest.mark.skip(reason="These tests hangs in Firebird 3.0.")
class CompoundSelectTest(_CompoundSelectTest):
    pass


@pytest.mark.skip(reason="These tests hangs in Firebird 4.0.")
class DateTimeTZTest(_DateTimeTZTest):
    pass


class NumericTest(_NumericTest):
    @testing.skip("firebird", reason="This test hangs in Firebird 4.0")
    def test_enotation_decimal_large(self):
        return


@pytest.mark.skip(reason="These tests hangs in Firebird 4.0.")
class RowCountTest(_RowCountTest):
    pass
