import pytest
from sqlalchemy import Index

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest
from sqlalchemy.testing.suite import (
    ComponentReflectionTestExtra as _ComponentReflectionTestExtra,
)
from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
from sqlalchemy.testing.suite import (
    DeprecatedCompoundSelectTest as _DeprecatedCompoundSelectTest,
)
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


class ComponentReflectionTestExtra(_ComponentReflectionTestExtra):
    def test_reflect_expression_based_indexes(self, metadata, connection):
        # Clone of super().test_reflect_expression_based_indexes adapted for Firebird.
        t = Table(
            "t",
            metadata,
            Column("x", String(30)),
            Column("y", String(30)),
            Column("z", String(30)),
        )

        Index("t_idx", func.lower(t.c.x), t.c.z, func.lower(t.c.y))
        # Maximum allowed for database page size = 8K
        long_str = "long string " * 42
        Index("t_idx_long", func.coalesce(t.c.x, long_str))
        Index("t_idx_2", t.c.x)

        metadata.create_all(connection)

        insp = inspect(connection)

        expected = [
            {
                "name": "t_idx_2",
                "column_names": ["x"],
                "unique": False,
                "dialect_options": {},
            }
        ]

        def completeIndex(entry):
            if testing.requires.index_reflects_included_columns.enabled:
                entry["include_columns"] = []
                entry["dialect_options"] = {
                    f"{connection.engine.name}_include": []
                }
            else:
                entry.setdefault("dialect_options", {})

        completeIndex(expected[0])

        class lower_index_str(str):
            def __eq__(self, other):
                # test that lower and x or y are in the string
                return "lower" in other and ("x" in other or "y" in other)

        class coalesce_index_str(str):
            def __eq__(self, other):
                # test that coalesce and the string is in other
                return "coalesce" in other.lower() and long_str in other

        expr_index = {
            "name": "t_idx",
            "column_names": [None, "z", None],
            "expressions": [
                lower_index_str("lower(x)"),
                "z",
                lower_index_str("lower(y)"),
            ],
            "unique": False,
        }
        completeIndex(expr_index)
        expected.insert(0, expr_index)

        expr_index_long = {
            "name": "t_idx_long",
            "column_names": [None],
            "expressions": [coalesce_index_str(f"coalesce(x, '{long_str}')")],
            "unique": False,
        }
        completeIndex(expr_index_long)
        expected.append(expr_index_long)

        eq_(insp.get_indexes("t"), expected)
        m2 = MetaData()
        t2 = Table("t", m2, autoload_with=connection)

        self.compare_table_index_with_expected(
            t2, expected, connection.engine.name
        )


class CompoundSelectTest(_CompoundSelectTest):
    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_distinct_selectable_in_unions(self):
        super().test_distinct_selectable_in_unions()

    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_limit_offset_aliased_selectable_in_unions(self):
        super().test_limit_offset_aliased_selectable_in_unions()

    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_plain_union(self):
        super().test_plain_union()


class DeprecatedCompoundSelectTest(_DeprecatedCompoundSelectTest):
    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_distinct_selectable_in_unions(self):
        super().test_distinct_selectable_in_unions()

    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_limit_offset_aliased_selectable_in_unions(self):
        super().test_limit_offset_aliased_selectable_in_unions()

    @pytest.mark.skip(reason="Firebird does not support ORDER BY alias")
    def test_plain_union(self):
        super().test_plain_union()


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

    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (3,),
        "Only supported in Firebird 3.0+.",
    )
    def test_insert_from_select_autoinc(self, connection):
        super().test_insert_from_select_autoinc(connection)


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

    # ToDo: Run this test only on Firebird 5.0+

    # @testing.skip(
    #     lambda config: config.db.dialect.server_version_info < (5, 0),
    #     "Multiple rows UPDATE RETURNING are supported only in Firebird 5.0+",
    # )
    # def test_update_delete_rowcount_return_defaults(self, connection, implicit_returning, dml, **kw):
    #     super().test_update_delete_rowcount_return_defaults(connection, implicit_returning, dml, **kw)


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
