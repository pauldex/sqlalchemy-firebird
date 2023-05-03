import pytest

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest

from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import RowCountTest as _RowCountTest

from sqlalchemy.testing.suite import DateTimeTZTest as _DateTimeTZTest
from sqlalchemy.testing.suite import TimeTZTest as _TimeTZTest


@pytest.mark.skip(
    reason="These tests fails in Firebird because a DELETE FROM <table> with self-referencing FK raises integrity errors."
)
class CTETest(_CTETest):
    pass


class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip(
        lambda config: config.db.dialect.server_version_info == (2, 5),
        "This test hangs in Firebird 2.5",
    )
    def test_insert_from_select(self):
        super()

    @testing.skip(
        lambda config: config.db.dialect.server_version_info == (2, 5),
        "This test hangs in Firebird 2.5",
    )
    def test_insert_from_select_with_defaults(self):
        super()


@pytest.mark.skip(
    reason="Just the skip below is not enough to stop the tests hanging (!?)."
)
class CompoundSelectTest(_CompoundSelectTest):
    @testing.skip(
        lambda config: config.db.dialect.driver == "fdb"
        and config.db.dialect.server_version_info == (3, 0),
        "This test hangs in Firebird 3.0",
    )
    def test_limit_offset_aliased_selectable_in_unions(self):
        super()


class NumericTest(_NumericTest):
    @testing.skip(
        lambda config: config.db.dialect.server_version_info == (3, 0),
        "This test hangs in Firebird 3.0",
    )
    def test_limit_offset_aliased_selectable_in_unions(self):
        super()

    @testing.skip(
        lambda config: config.db.dialect.driver == "fdb"
        and config.db.dialect.server_version_info == (4, 0),
        "This test hangs in Firebird 4.0 with fdb",
    )
    def test_enotation_decimal_large(self):
        super()


class RowCountTest(_RowCountTest):
    @testing.skip(
        lambda config: config.db.dialect.driver == "fdb"
        and config.db.dialect.server_version_info == (4, 0),
        "This test hangs in Firebird 4.0 with fdb",
    )
    def test_update_rowcount2(self):
        super()


# Firebird-driver needs special time zone handling.
#   https://github.com/FirebirdSQL/python3-driver/issues/19#issuecomment-1523045743
class DateTimeTZTest(_DateTimeTZTest):
    def setup_method(self, method):
        super()

        from firebird.driver.types import get_timezone

        self.data = datetime.datetime(
            2012, 10, 15, 12, 57, 18, tzinfo=get_timezone("UTC")
        )


class TimeTZTest(_TimeTZTest):
    def setup_method(self, method):
        super()

        from firebird.driver.types import get_timezone

        self.data = datetime.time(12, 57, 18, tzinfo=get_timezone("UTC"))
