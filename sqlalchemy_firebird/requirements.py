from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    def firebird_3_or_higher(self):
        return exclusions.skip_if(
            lambda config: config.db.dialect.server_version_info < (3,),
            "Only supported in Firebird 3.0+.",
        )

    def firebird_4_or_higher(self):
        return exclusions.skip_if(
            lambda config: config.db.dialect.server_version_info < (4,),
            "Only supported in Firebird 4.0+.",
        )

    #
    # SuiteRequirements
    #

    # 69
    @property
    def foreign_keys_reflect_as_index(self):
        # get_indexes does not returns FK indexes
        return exclusions.closed()

    # 82
    @property
    def unique_constraints_reflect_as_index(self):
        return exclusions.open()

    # 174
    @property
    def implicitly_named_constraints(self):
        return exclusions.open()

    # 213
    @property
    def sql_expression_limit_offset(self):
        # Firebird accepts expression with (non-standard) "ROWS m TO n" syntax.
        return exclusions.open()

    # 222
    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        return exclusions.closed()

    # 234
    @property
    def parens_in_union_contained_select_wo_limit_offset(self):
        return exclusions.closed()

    # 260
    @property
    def nullsordering(self):
        return exclusions.open()

    # 291
    @property
    def window_functions(self):
        return exclusions.open()

    # 296
    @property
    def ctes(self):
        return exclusions.open()

    # 318
    @property
    def autoincrement_insert(self):
        return exclusions.closed()

    @property
    def empty_inserts(self):
        return self.firebird_4_or_higher()

    # 488
    @property
    def implements_get_lastrowid(self):
        # Firebird does not have a LAST ROWID function.
        return exclusions.closed()

    # 532
    @property
    def views(self):
        return exclusions.open()

    # 551
    @property
    def foreign_key_constraint_name_reflection(self):
        return exclusions.open()

    # 637
    @property
    def reflects_pk_names(self):
        # get_pk_constraint always returns "name": None.
        return exclusions.closed()

    # 654
    @property
    def comment_reflection(self):
        return exclusions.open()

    # 659
    @property
    def comment_reflection_full_unicode(self):
        return self.firebird_4_or_higher()

    # 699
    @property
    def foreign_key_constraint_option_reflection_ondelete(self):
        return exclusions.open()

    # 707
    @property
    def fk_constraint_option_reflection_ondelete_noaction(self):
        return exclusions.open()

    # 711
    @property
    def foreign_key_constraint_option_reflection_onupdate(self):
        return exclusions.open()

    # 727
    @property
    def temp_table_names(self):
        return exclusions.open()

    # 732
    @property
    def has_temp_table(self):
        return exclusions.open()

    # 737
    @property
    def temporary_tables(self):
        return exclusions.open()

    # 755
    @property
    def indexes_with_ascdesc(self):
        # Firebird does not support bidirectional indices per column.
        return exclusions.closed()

    # 760
    @property
    def reflect_indexes_with_ascdesc(self):
        # Firebird does not support bidirectional indices per column.
        return exclusions.closed()

    # 766
    @property
    def indexes_with_expressions(self):
        return exclusions.open()

    # 771
    @property
    def reflect_indexes_with_expressions(self):
        return exclusions.open()

    # 782
    @property
    def check_constraint_reflection(self):
        return exclusions.open()

    # 777
    @property
    def unique_constraint_reflection(self):
        return exclusions.open()

    # 787
    @property
    def duplicate_key_raises_integrity_error(self):
        # Firebird fdb driver does not raises IntegrityError.
        return exclusions.closed()

    # 795
    @property
    def unbounded_varchar(self):
        # Firebird requires a length for VARCHAR data types.
        return exclusions.closed()

    # 810
    @property
    def unicode_data(self):
        # assumes ?charset=UTF8 in connection URI
        return exclusions.open()

    # 819
    @property
    def unicode_ddl(self):
        # assumes ?charset=UTF8 in connection URI
        return exclusions.open()

    # 847
    @property
    def datetime_timezone(self):
        # Time zone support added in Firebird 4.
        return self.firebird_4_or_higher()

    # 862
    @property
    def date_implicit_bound(self):
        return exclusions.closed()

    # 871
    @property
    def time_implicit_bound(self):
        return exclusions.closed()

    # 880
    @property
    def datetime_implicit_bound(self):
        return exclusions.closed()

    # 889
    @property
    def datetime_microseconds(self):
        # Firebird does not support microseconds.
        return exclusions.closed()

    # 947
    @property
    def time_microseconds(self):
        # Firebird does not support microseconds.
        return exclusions.closed()

    # 1106
    @property
    def precision_numerics_enotation_small(self):
        return exclusions.open()

    # 1112
    @property
    def precision_numerics_enotation_large(self):
        # Increased maximum precision of NUMERIC and DECIMAL to 38 digits in Firebird 4.
        return self.firebird_4_or_higher()

    # 1199
    @property
    def precision_generic_float_type(self):
        # Firebird FLOAT does not ensure precision of 7 decimal digits after the decimal point.

        # https://firebirdsql.org/file/documentation/html/en/refdocs/fblangref40/firebird-40-language-reference.html#fblangref40-datatypes-floattypes-approx
        #   The FLOAT data type defaults to a 32-bit single precision floating-point type with an
        #   approximate precision of 7 decimal digits after the decimal point (24 binary digits).
        #   To ensure the safety of storage, rely on 6 decimal digits of precision.

        return exclusions.closed()

    # 1274
    @property
    def savepoints(self):
        return exclusions.open()

    # 1330
    @property
    def order_by_col_from_union(self):
        # Firebird does not support ORDER BY alias in UNIONs.
        return exclusions.closed()

    # 1365
    def get_order_by_collation(self, config):
        return "UTF8"

    # 1580
    @property
    def computed_columns(self):
        return exclusions.open()

    # 1628
    @property
    def identity_columns(self):
        return self.firebird_3_or_higher()

    @property
    def identity_columns_standard(self):
        return self.firebird_3_or_higher()

    # 1642
    @property
    def regexp_match(self):
        return exclusions.closed()

    # 1652
    @property
    def fetch_first(self):
        return exclusions.open()

    # 1667
    @property
    def fetch_no_order_by(self):
        return exclusions.open()

    #
    # DefaultRequirements
    #

    # 1061
    @property
    def array_type(self):
        # Firebird ARRAY type not implemented.
        return exclusions.closed()

    # 1993
    @property
    def uuid_data_type(self):
        # Firebird does not have a native UUID data type.
        return exclusions.closed()

    #
    # Workarounds for Firebird 2.5/fdb
    #

    @property
    def autoincrement_without_sequence(self):
        # Disables entire IdentityAutoincrementTest on Firebird 2.5 (does not have autoincrement)
        return self.firebird_3_or_higher()

    @property
    def insert_from_select(self):
        # Avoids hanging tests on Firebird 2.5
        return self.firebird_3_or_higher()
