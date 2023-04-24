import pytest

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest

from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
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
    @testing.skip("firebird=2", reason="This test hangs in Firebird 2.0")
    def test_insert_from_select(self):
        pass


@pytest.mark.skip(reason="These tests hangs in Firebird 3.0.")
class CompoundSelectTest(_CompoundSelectTest):
    @testing.skip("firebird=3", reason="This test hangs in Firebird 3.0")
    def test_limit_offset_aliased_selectable_in_unions(self):
        pass


class NumericTest(_NumericTest):
    @testing.skip(
        "firebird+fdb=4", reason="This test hangs in Firebird 4.0 with fdb"
    )
    def test_enotation_decimal_large(self):
        return


class RowCountTest(_RowCountTest):
    @testing.skip(
        "firebird+fdb=4", reason="This test hangs in Firebird 4.0 with fdb"
    )
    def test_update_rowcount2(self):
        pass
