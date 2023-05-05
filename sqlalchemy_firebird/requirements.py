from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property
    def array_type(self):
        # TODO:  implement Firebird ARRAY type - see visit_ARRAY in base.py
        return exclusions.closed()

    @property
    def autoincrement_insert(self):
        return exclusions.closed()

    @property
    def check_constraint_reflection(self):
        # added
        # return exclusions.open()
        # TODO: fix 3 errors
        return exclusions.closed()

    @property
    def comment_reflection(self):
        return exclusions.open()

    @property
    def computed_columns(self):
        """Supports computed columns"""
        return exclusions.open()

    @property
    def ctes(self):
        # added
        # return exclusions.open()
        # TODO: fix 14 errors
        return exclusions.closed()

    @property
    def date_implicit_bound(self):
        # added
        return exclusions.closed()

    @property
    def datetime_implicit_bound(self):
        # added
        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        # Firebird does not support microseconds.
        return exclusions.closed()

    @property
    def datetime_timezone(self):
        # added
        # Time zone support added in Firebird 4.
        # return exclusions.skip_if("firebird<4")
        # TODO:  fix 2 errors
        return exclusions.closed()

    @property
    def duplicate_key_raises_integrity_error(self):
        # Firebird fdb driver does not raises IntegrityError.
        return exclusions.closed()

    @property
    def fetch_first(self):
        # added
        # return exclusions.open()
        # TODO:  fix 3 errors
        return exclusions.closed()

    @property
    def fetch_no_order_by(self):
        # added
        return exclusions.open()

    @property
    def fk_constraint_option_reflection_ondelete_noaction(self):
        # added
        # return exclusions.open()
        # TODO:  fix 1 errors
        return exclusions.closed()

    @property
    def floats_to_four_decimals(self):
        # removed
        # TODO: removing causes 1 error
        return exclusions.closed()

    @property
    def foreign_key_constraint_name_reflection(self):
        # added
        return exclusions.open()

    @property
    def foreign_key_constraint_option_reflection_ondelete(self):
        # added
        # return exclusions.open()
        # TODO:  fix 1 errors
        return exclusions.closed()

    @property
    def foreign_key_constraint_option_reflection_onupdate(self):
        # added
        # return exclusions.open()
        # TODO:  fix 2 errors
        return exclusions.closed()

    @property
    def foreign_keys_reflect_as_index(self):
        # added
        # get_indexes does not returns FK indexes
        return exclusions.closed()

    # TODO: adding causes 1 errors
    # @property
    # def get_order_by_collation(self, config):
    #     # added
    #     return "UTF8"

    @property
    def has_temp_table(self):
        # added
        return exclusions.open()

    @property
    def identity_columns(self):
        # added
        # Identity Column Type added in Firebird 3.
        # return exclusions.skip_if("firebird<3")
        # TODO:  fix 3 errors
        return exclusions.closed()

    @property
    def implements_get_lastrowid(self):
        # added
        # Firebird does not have a LAST ROWID function.
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        """Target database supports constraints without an explicit name."""
        return exclusions.open()

    @property
    def indexes_with_ascdesc(self):
        # Firebird does not support bidirectional indices.
        return exclusions.closed()

    @property
    def indexes_with_expressions(self):
        # added
        # return exclusions.open()
        # TODO:  fix 1 errors
        return exclusions.closed()

    @property
    def nullsordering(self):
        # added
        return exclusions.open()

    @property
    def order_by_col_from_union(self):
        # added
        # Firebird does not support ORDER BY alias in UNIONs.
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_wo_limit_offset(self):
        return exclusions.closed()

    @property
    def precision_generic_float_type(self):
        # Firebird FLOAT does not ensure precision of 7 decimal digits after the decimal point.

        # https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-datatypes-floattypes-approx
        #   The FLOAT data type defaults to a 32-bit single precision floating-point type with an
        #   approximate precision of 7 decimal digits after the decimal point (24 binary digits).
        #   To ensure the safety of storage, rely on 6 decimal digits of precision.
        return exclusions.closed()

    @property
    def precision_numerics_enotation_large(self):
        # added
        # Increased maximum precision of NUMERIC and DECIMAL to 38 digits in Firebird 4.
        # return exclusions.skip_if("firebird<4")
        # TODO:  fix 2 errors
        return exclusions.closed()

    @property
    def precision_numerics_enotation_small(self):
        # added
        return exclusions.open()

    @property
    def reflect_indexes_with_ascdesc(self):
        # added
        # Firebird does not support bidirectional indices.
        return exclusions.closed()

    @property
    def reflect_indexes_with_expressions(self):
        # added
        return exclusions.open()

    @property
    def reflects_pk_names(self):
        # added
        # get_pk_constraint always returns "name": None.
        return exclusions.closed()

    @property
    def regexp_match(self):
        # added
        return exclusions.closed()

    @property
    def sane_rowcount_w_returning(self):
        # removed
        # TODO: removing causes 2 errors
        return exclusions.closed()

    @property
    def savepoints(self):
        # added
        return exclusions.open()

    @property
    def sql_expression_limit_offset(self):
        # Firebird accepts expression with (non-standard) "ROWS m TO n" syntax.
        # added
        return exclusions.open()

    @property
    def temp_table_names(self):
        return exclusions.open()

    @property
    def temporary_tables(self):
        # added
        return exclusions.open()

    @property
    def time_implicit_bound(self):
        # added
        return exclusions.closed()

    @property
    def time_microseconds(self):
        # Firebird does not support microseconds.
        return exclusions.closed()

    # @property
    # def tuple_in(self):
    #     """Supports queries like:
    #     SELECT some_table.id FROM some_table
    #     WHERE (some_table.x, some_table.z) IN ((2, 'z2'), (3, 'z3'), (4, 'z4'))
    #
    #     Firebird would have to change the query to something like:
    #     SELECT some_table.id FROM some_table
    #     WHERE (some_table.x = 2 and some_table.z = 'z2')
    #        OR (some_table.x = 3 and some_table.z = 'z3')
    #        OR (some_table.x = 4 and some_table.z = 'z4')
    #     """  # noqa
    #     # removed
    #     # TODO: Research ways to support this in Firebird
    #     return exclusions.closed()

    @property
    def unbounded_varchar(self):
        # Firebird requires a length for VARCHAR data types.
        return exclusions.closed()

    @property
    def unicode_data(self):
        # assumes ?charset=UTF8 in connection URI
        return exclusions.open()

    @property
    def unicode_ddl(self):
        # assumes ?charset=UTF8 in connection URI
        return exclusions.open()

    @property
    def unique_constraint_reflection(self):
        # TODO: Research ways to support this in Firebird
        # changed
        # return exclusions.open()
        # TODO:  fix 4 errors
        return exclusions.closed()

    @property
    def unique_constraints_reflect_as_index(self):
        # added
        return exclusions.open()

    @property
    def uuid_data_type(self):
        # Firebird does not have a native UUID data type.
        return exclusions.closed()

    @property
    def views(self):
        # added
        return exclusions.open()

    @property
    def window_functions(self):
        # added
        return exclusions.open()
