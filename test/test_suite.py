from sqlalchemy.testing.suite import *  # noqa: F401, F403
from sqlalchemy.testing.suite import BooleanTest as _BooleanTest
from sqlalchemy.testing.suite import (
    CastTypeDecoratorTest as _CastTypeDecoratorTest,
)
from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
)
from sqlalchemy.testing.suite import CompoundSelectTest as _CompoundSelectTest
from sqlalchemy.testing.suite import DateTest as _DateTest
from sqlalchemy.testing.suite import (
    DateTimeCoercedToDateTimeTest as _DateTimeCoercedToDateTimeTest,
)
from sqlalchemy.testing.suite import DateTimeTest as _DateTimeTest
from sqlalchemy.testing.suite import (
    DeprecatedCompoundSelectTest as _DeprecatedCompoundSelectTest,
)
from sqlalchemy.testing.suite import (
    DifficultParametersTest as _DifficultParametersTest,
)
from sqlalchemy.testing.suite import (
    ExpandingBoundInTest as _ExpandingBoundInTest,
)
from sqlalchemy.testing.suite import (
    IdentityAutoincrementTest as _IdentityAutoincrementTest,
)
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import IntegerTest as _IntegerTest
from sqlalchemy.testing.suite import (
    LongNameBlowoutTest as _LongNameBlowoutTest,
)
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import StringTest as _StringTest
from sqlalchemy.testing.suite import TableDDLTest as _TableDDLTest
from sqlalchemy.testing.suite import TextTest as _TextTest
from sqlalchemy.testing.suite import UnicodeTextTest as _UnicodeTextTest
from sqlalchemy.testing.suite import UnicodeVarcharTest as _UnicodeVarcharTest


class BooleanTest(_BooleanTest):
    @testing.skip("firebird")
    def test_render_literal_bool(self):
        # "table unknown"
        return


class CastTypeDecoratorTest(_CastTypeDecoratorTest):
    @testing.skip("firebird")
    def test_special_type(self):
        # "table unknown"
        return


class ComponentReflectionTest(_ComponentReflectionTest):
    @testing.skip("firebird")
    def test_get_comments(self):
        """
        Test asserts a comment is on COMMENT_TABLE.

        I'm not able to find where a comment is associated with this table.
        Skip this one for now...
        """
        return

    @testing.skip("firebird")
    def test_get_table_names(self):
        # most combinations are skipped (schemas) or fail for us (views)
        return


class CompoundSelectTest(_CompoundSelectTest):
    """Firebird requires ORDER BY column position number for UNIONs"""

    @testing.skip("firebird")
    def test_plain_union(self):
        return

    @testing.skip("firebird")
    def test_distinct_selectable_in_unions(self):
        return

    @testing.skip("firebird")
    def test_limit_offset_aliased_selectable_in_unions(self):
        return


class DateTest(_DateTest):
    @testing.skip("firebird")
    def test_select_direct(self):
        # NotImplementedError: Don't know how to literal-quote value
        return


class DateTimeCoercedToDateTimeTest(_DateTimeCoercedToDateTimeTest):
    @testing.skip("firebird")
    def test_select_direct(self):
        # NotImplementedError: Don't know how to literal-quote value
        return


class DateTimeTest(_DateTimeTest):
    @testing.skip("firebird")
    def test_select_direct(self):
        # NotImplementedError: Don't know how to literal-quote value
        return


class DeprecatedCompoundSelectTest(_DeprecatedCompoundSelectTest):
    @testing.skip("firebird")
    def test_distinct_selectable_in_unions(self):
        # invalid ORDER BY clause
        return

    @testing.skip("firebird")
    def test_limit_offset_aliased_selectable_in_unions(self):
        # invalid ORDER BY clause
        return

    @testing.skip("firebird")
    def test_plain_union(self):
        # invalid ORDER BY clause
        return


class DifficultParametersTest(_DifficultParametersTest):
    @testing.skip("firebird")
    def test_round_trip(self):
        """
        SQLAlchemy 1.4.43
        Invalid column names in temp table

        """
        return

    @testing.skip("firebird")
    def test_round_trip_same_named_column(self):
        """
        SQLAlchemy 1.4.46
        Invalid column names in temp table

        """
        return

    @testing.skip("firebird")
    def test_standalone_bindparam_escape(self):
        """
        SQLAlchemy 1.4.46
        Invalid column names in temp table

        """
        return

    @testing.skip("firebird")
    def test_standalone_bindparam_escape_expanding(self):
        """
        SQLAlchemy 1.4.46
        Invalid column names in temp table

        """
        return


# class ExpandingBoundInTest(_ExpandingBoundInTest):
# @testing.skip("firebird")
# def test_null_in_empty_set_is_false(self):
#     # TODO: investigate why this formerly working test now fails
#     return


class IdentityAutoincrementTest(_IdentityAutoincrementTest):
    @testing.skip("firebird")
    def test_autoincrement_with_identity(self):
        # fails on Firebird 4.0
        return


class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip("firebird")
    def test_autoclose_on_insert(self):
        # TODO: investigate why when the real test fails it hangs the test
        #       run on class teardown (after `DROP TABLE autoinc_pk`)
        return

    @testing.skip("firebird")
    def test_insert_from_select_with_defaults(self):
        # TODO: investigate why this formerly working test now fails
        return


class IntegerTest(_IntegerTest):
    @testing.skip("firebird")
    def test_literal(self):
        # Table unknown
        return


class LongNameBlowoutTest(_LongNameBlowoutTest):
    @testing.skip("firebird")
    def test_long_convention_name(self):
        # fails on Firebird 4.0
        return


class NumericTest(_NumericTest):
    @testing.skip("firebird")
    def test_float_as_float(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_numeric_as_decimal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_numeric_as_float(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_numeric_null_as_decimal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_numeric_null_as_float(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_precision_decimal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_render_literal_float(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_render_literal_numeric(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_render_literal_numeric_asfloat(self):
        # Table unknown
        return


class SimpleUpdateDeleteTest:
    """Some of these tests can hang the test run."""

    pass


class StringTest(_StringTest):
    @testing.skip("firebird")
    def test_literal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_backslashes(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_non_ascii(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_quoting(self):
        # Table unknown
        return


class TableDDLTest(_TableDDLTest):
    @testing.skip("firebird")
    def test_create_table_schema(self):
        """Do not test schemas

        In Firebird, a schema is the same thing as a database.  According to
        the Firebird reference manual, "The CREATE DATABASE statement creates
        a new database. You can use CREATE DATABASE or CREATE SCHEMA. They are
        synonymous."  See:
        https://firebirdsql.org/file/documentation/reference_manuals/fblangref25-en/html/fblangref25-ddl-db.html
        """
        return


class TextTest(_TextTest):
    @testing.skip("firebird")
    def test_literal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_backslashes(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_non_ascii(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_percentsigns(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_quoting(self):
        # Table unknown
        return


class TimeTest:
    """Some of these tests can hang the test run."""

    pass


class UnicodeTextTest(_UnicodeTextTest):
    @testing.skip("firebird")
    def test_literal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_non_ascii(self):
        # Table unknown
        return


class UnicodeVarcharTest(_UnicodeVarcharTest):
    @testing.skip("firebird")
    def test_literal(self):
        # Table unknown
        return

    @testing.skip("firebird")
    def test_literal_non_ascii(self):
        # Table unknown
        return
