import operator
import pytest

import sqlalchemy as sa

from packaging import version
from sqlalchemy import __version__ as SQLALCHEMY_VERSION
from sqlalchemy import Index

from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import (
    CTETest as _CTETest,
    ComponentReflectionTest as _ComponentReflectionTest,
    ComponentReflectionTestExtra as _ComponentReflectionTestExtra,
    CompoundSelectTest as _CompoundSelectTest,
    DeprecatedCompoundSelectTest as _DeprecatedCompoundSelectTest,
    IdentityReflectionTest as _IdentityReflectionTest,
    DateTimeTZTest as _DateTimeTZTest,
    TimeTZTest as _TimeTZTest,
    StringTest as _StringTest,
    InsertBehaviorTest as _InsertBehaviorTest,
    NumericTest as _NumericTest,
    RowCountTest as _RowCountTest,
    SimpleUpdateDeleteTest as _SimpleUpdateDeleteTest,
)

from firebird.driver.types import get_timezone


@pytest.mark.skip(
    reason="These tests fails in Firebird because a DELETE FROM <table> with self-referencing FK raises integrity errors."
)
class CTETest(_CTETest):
    pass


class ComponentReflectionTest(_ComponentReflectionTest):
    def test_get_unique_constraints(self, metadata, connection):
        # Clone of super().test_get_unique_constraints() adapted for Firebird.

        schema = None
        uniques = sorted(
            [
                {"name": "unique_a", "column_names": ["a"]},
                # Firebird won't allow two unique index with same set of columns.
                {"name": "unique_a_b_c", "column_names": ["a", "b", "c"]},
                {"name": "unique_c_a", "column_names": ["c", "a"]},
                {"name": "unique_asc_key", "column_names": ["asc", "key"]},
                {"name": "i.have.dots", "column_names": ["b"]},
                {"name": "i have spaces", "column_names": ["c"]},
            ],
            key=operator.itemgetter("name"),
        )
        table = Table(
            "testtbl",
            metadata,
            Column("a", sa.String(20)),
            Column("b", sa.String(30)),
            Column("c", sa.Integer),
            # reserved identifiers
            Column("asc", sa.String(30)),
            Column("key", sa.String(30)),
            schema=schema,
        )
        for uc in uniques:
            table.append_constraint(
                sa.UniqueConstraint(*uc["column_names"], name=uc["name"])
            )
        table.create(connection)

        inspector = inspect(connection)
        reflected = sorted(
            inspector.get_unique_constraints("testtbl", schema=schema),
            key=operator.itemgetter("name"),
        )

        eq_(uniques, reflected)


class ComponentReflectionTestExtra(_ComponentReflectionTestExtra):
    def test_reflect_expression_based_indexes(self, metadata, connection):
        # Clone of super().test_reflect_expression_based_indexes adapted for Firebird.

        using_sqlalchemy2 = version.parse(SQLALCHEMY_VERSION).major >= 2
        if not using_sqlalchemy2:
            # Test from SQLAlchemy 1.4
            t = Table(
                "t",
                metadata,
                Column("x", String(30)),
                Column("y", String(30)),
            )

            Index("t_idx", func.lower(t.c.x), func.lower(t.c.y))

            Index("t_idx_2", t.c.x)

            metadata.create_all(connection)

            insp = inspect(connection)

            expected = [
                {
                    "name": "t_idx",
                    "column_names": [None, None],
                    "unique": False,
                    "expressions": ["lower(x)", "lower(y)"],
                    "dialect_options": {},
                },
                {
                    "name": "t_idx_2",
                    "column_names": ["x"],
                    "unique": False,
                    "dialect_options": {},
                },
            ]

            eq_(insp.get_indexes("t"), expected)
            return

        # Test from SQLAlchemy 2.0

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


class IdentityReflectionTest(_IdentityReflectionTest):
    # ToDo: How to avoid the setup method of this class to run in Firebird < 4.0?

    @testing.skip(
        lambda config: config.db.dialect.server_version_info < (4, 0),
        "GENERATED ... AS IDENTITY columns are supported only in Firebird 4.0+",
    )
    def test_reflect_identity(self):
        super().test_reflect_identity()


# Firebird-driver needs special time zone handling.
#   https://github.com/FirebirdSQL/python3-driver/issues/19#issuecomment-1523045743


class DateTimeTZTest(_DateTimeTZTest):
    data = datetime.datetime(
        2012, 10, 15, 12, 57, 18, tzinfo=get_timezone("UTC")
    )


class TimeTZTest(_TimeTZTest):
    data = datetime.time(12, 57, 18, tzinfo=get_timezone("UTC"))


class StringTest(_StringTest):
    @pytest.mark.skip(
        reason="Firebird does not accept a LIKE 'A%C%Z' in a VARCHAR(2) column"
    )
    def test_dont_truncate_rightside(
        self, metadata, connection, expr, expected
    ):
        super().test_dont_truncate_rightside(
            self, metadata, connection, expr, expected
        )


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

    # ToDo: How to run this test only on Firebird 5.0+?

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


# ToDo: How to skip SequenceTest (from sqlalchemy/test/sql/test_sequences.py) only on Firebird 2.5?
