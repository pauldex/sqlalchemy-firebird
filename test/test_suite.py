import pytest

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest
from sqlalchemy.testing.suite import DateTimeTZTest as _DateTimeTZTest
from sqlalchemy.testing.suite import TimeTZTest as _TimeTZTest
from sqlalchemy.testing.suite import StringTest as _StringTest

from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import RowCountTest as _RowCountTest
from sqlalchemy.testing.suite import (
    SimpleUpdateDeleteTest as _SimpleUpdateDeleteTest,
)


@pytest.mark.skip(
    reason="These tests fails in Firebird because a DELETE FROM <table> with self-referencing FK raises integrity errors."
)
class CTETest(_CTETest):
    pass


# Firebird-driver needs special time zone handling.
#   https://github.com/FirebirdSQL/python3-driver/issues/19#issuecomment-1523045743
class DateTimeTZTest(_DateTimeTZTest):
    def setup_method(self, method):
        super().setup_method(method)

        from firebird.driver.types import get_timezone

        self.data = datetime.datetime(
            2012, 10, 15, 12, 57, 18, tzinfo=get_timezone("UTC")
        )


class TimeTZTest(_TimeTZTest):
    def setup_method(self, method):
        super().setup_method(method)

        from firebird.driver.types import get_timezone

        self.data = datetime.time(12, 57, 18, tzinfo=get_timezone("UTC"))


class StringTest(_StringTest):
    @testing.fails(
        "Firebird does not accept a LIKE 'A%C%Z' in a VARCHAR(2) column",
    )
    def test_dont_truncate_rightside(
        self, metadata, connection, expr, expected
    ):
        pass


#
# Hanging tests. Run separately with "pytest -m hanging".
#


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.hanging(reason="This test hangs in Firebird 2.5")
    def test_insert_from_select(self, connection):
        super().test_insert_from_select(connection)

    @pytest.mark.hanging(reason="This test hangs in Firebird 2.5")
    def test_insert_from_select_with_defaults(self, connection):
        super().test_insert_from_select_with_defaults(connection)


class NumericTest(_NumericTest):
    @pytest.mark.hanging(
        reason="This test hangs in Firebird 4.0 with fdb",
    )
    def test_enotation_decimal_large(self, do_numeric_test):
        super().test_enotation_decimal_large(do_numeric_test)


class RowCountTest(_RowCountTest):
    @pytest.mark.hanging(
        reason="This test hangs in Firebird 4.0 with fdb and SQLALchemy 2.0+",
    )
    def test_update_rowcount2(self, connection):
        super().test_update_rowcount2(connection)


class SimpleUpdateDeleteTest(_SimpleUpdateDeleteTest):
    @pytest.mark.hanging(
        reason="This test hangs in Firebird 3.0",
    )
    def test_update(self, connection):
        super().test_update(connection)

    @pytest.mark.hanging(
        reason="This test hangs in Firebird 3.0",
    )
    def test_delete(self, connection):
        super().test_delete(connection)
