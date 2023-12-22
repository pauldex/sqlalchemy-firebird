import operator
import pytest

import sqlalchemy as sa

from packaging import version
from sqlalchemy import __version__ as SQLALCHEMY_VERSION
from sqlalchemy import Index
from sqlalchemy.testing import is_false
from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import (
    CTETest as _CTETest,
    ComponentReflectionTest as _ComponentReflectionTest,
    ComponentReflectionTestExtra as _ComponentReflectionTestExtra,
    CompoundSelectTest as _CompoundSelectTest,
    DeprecatedCompoundSelectTest as _DeprecatedCompoundSelectTest,
    IdentityColumnTest as _IdentityColumnTest,
    IdentityReflectionTest as _IdentityReflectionTest,
    DateTimeTZTest as _DateTimeTZTest,
    TimeTZTest as _TimeTZTest,
    StringTest as _StringTest,
    InsertBehaviorTest as _InsertBehaviorTest,
    NumericTest as _NumericTest,
    RowCountTest as _RowCountTest,
    SimpleUpdateDeleteTest as _SimpleUpdateDeleteTest,
)

import sys

if sys.version_info.major == 2:
    try:
        from firebird.driver.types import get_timezone
    except ImportError:

        def get_timezone(timezone=None):
            # TODO:  fdb version implementation
            pass

else:
    try:
        from firebird.driver.types import get_timezone
    except ImportError as e:

        def get_timezone(timezone=None):
            # TODO:  fdb version implementation
            pass


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

    def test_get_temp_table_indexes(self, connection):
        # Clone of super().test_get_temp_table_indexes() adapted for Firebird.
        insp = inspect(connection)
        table_name = self.temp_table_name()
        indexes = insp.get_indexes(table_name)
        for ind in indexes:
            ind.pop("dialect_options", None)
        expected = [
            {
                "unique": False,
                "column_names": ["foo"],
                "name": "user_tmp_ix",
                "descending": False,
            }
        ]
        if testing.requires.index_reflects_included_columns.enabled:
            expected[0]["include_columns"] = []
        eq_(
            [idx for idx in indexes if idx["name"] == "user_tmp_ix"],
            expected,
        )


class ComponentReflectionTestExtra(_ComponentReflectionTestExtra):
    def test_reflect_descending_indexes(self, metadata, connection):
        t = Table(
            "t",
            metadata,
            Column("x", String(30)),
            Column("y", String(30)),
            Column("z", String(30)),
        )

        Index("t_idx_2", t.c.x, firebird_descending=True)

        metadata.create_all(connection)

        insp = inspect(connection)

        expected = [
            {
                "name": "t_idx_2",
                "column_names": ["x"],
                "unique": False,
                "dialect_options": {},
                "descending": True,
            }
        ]

        eq_(insp.get_indexes("t"), expected)
        m2 = MetaData()
        t2 = Table("t", m2, autoload_with=connection)

        self.compare_table_index_with_expected(
            t2, expected, connection.engine.name
        )

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
                    "descending": False,
                },
                {
                    "name": "t_idx_2",
                    "column_names": ["x"],
                    "unique": False,
                    "dialect_options": {},
                    "descending": False,
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
            }
        ]

        def completeIndex(entry):
            entry.setdefault("unique", False)
            entry.setdefault("descending", False)
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
        }
        completeIndex(expr_index)
        expected.insert(0, expr_index)

        expr_index_long = {
            "name": "t_idx_long",
            "column_names": [None],
            "expressions": [coalesce_index_str(f"coalesce(x, '{long_str}')")],
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


class IdentityColumnTest(_IdentityColumnTest):
    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (4,),
        "GENERATED ALWAYS AS IDENTITY columns are supported only in Firebird 4.0+",
    )
    def test_select_all(self, connection):
        super().test_select_all(connection)

    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (4,),
        "GENERATED ALWAYS AS IDENTITY columns are supported only in Firebird 4.0+",
    )
    def test_insert_always_error(self, connection):
        super().test_insert_always_error(connection)


class IdentityReflectionTest(_IdentityReflectionTest):
    # Clone of IdentityReflectionTest adapted for Firebird.

    @classmethod
    def define_tables(cls, metadata):
        firebird_4_or_higher = config.db.dialect.server_version_info >= (4,)

        Table(
            "t1",
            metadata,
            Column("normal", Integer),
            Column("id1", Integer, Identity()),
        )

        Table(
            "t2",
            metadata,
            Column(
                "id2",
                Integer,
                Identity(
                    always=firebird_4_or_higher,
                    start=2,
                    increment=3 if firebird_4_or_higher else None,
                ),
            ),
        )

    def test_reflect_identity(self):
        firebird_4_or_higher = config.db.dialect.server_version_info >= (4,)

        insp = inspect(config.db)

        cols = insp.get_columns("t1")
        for col in cols:
            if col["name"] == "normal":
                is_false("identity" in col)
            elif col["name"] == "id1":
                if "autoincrement" in col:
                    is_true(col["autoincrement"])
                eq_(col["default"], None)
                is_true("identity" in col)
                self.check(
                    col["identity"],
                    dict(
                        always=False,
                        start=1 if firebird_4_or_higher else 0,
                        increment=1,
                    ),
                    approx=True,
                )

    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (4,),
        "GENERATED ALWAYS AS IDENTITY columns are supported only in Firebird 4.0+",
    )
    def test_reflect_identity_v4(self):
        insp = inspect(config.db)

        cols = insp.get_columns("t2")
        for col in cols:
            if col["name"] == "id2":
                if "autoincrement" in col:
                    is_true(col["autoincrement"])
                eq_(col["default"], None)
                is_true("identity" in col)
                self.check(
                    col["identity"],
                    dict(
                        always=True,
                        start=2,
                        increment=3,
                    ),
                    approx=False,
                )


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


class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip_if(
        lambda config: config.db.dialect.driver == "fdb",
        "Driver fdb returns erroneous 'returns_rows = True'.",
    )
    @testing.variation("style", ["plain", "return_defaults"])
    @testing.variation("executemany", [True, False])
    def test_no_results_for_non_returning_insert(
        self, connection, style, executemany
    ):
        super().test_no_results_for_non_returning_insert(
            connection, style, executemany
        )

    @requirements.autoincrement_insert  # missing in SQLAlchemy
    def test_autoclose_on_insert_implicit_returning(self, connection):
        super().test_autoclose_on_insert_implicit_returning(connection)


class RowCountTest(_RowCountTest):
    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (5,),
        "Multiple rows UPDATE/DELETE RETURNING are supported only in Firebird 5.0+",
    )
    @testing.variation("implicit_returning", [True, False])
    @testing.variation(
        "dml",
        [
            ("update", testing.requires.update_returning),
            ("delete", testing.requires.delete_returning),
        ],
    )
    def test_update_delete_rowcount_return_defaults(
        self, connection, implicit_returning, dml
    ):
        super().test_update_delete_rowcount_return_defaults(
            connection, implicit_returning, dml, None
        )


class SimpleUpdateDeleteTest(_SimpleUpdateDeleteTest):
    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (5,),
        "Multiple rows UPDATE RETURNING are supported only in Firebird 5.0+",
    )
    @testing.variation("criteria", ["rows", "norows", "emptyin"])
    @testing.requires.update_returning
    def test_update_returning(self, connection, criteria):
        super().test_update_returning(connection, criteria)

    @testing.skip_if(
        lambda config: config.db.dialect.server_version_info < (5,),
        "Multiple rows DELETE RETURNING are supported only in Firebird 5.0+",
    )
    @testing.variation("criteria", ["rows", "norows", "emptyin"])
    @testing.requires.delete_returning
    def test_delete_returning(self, connection, criteria):
        super().test_delete_returning(connection, criteria)
