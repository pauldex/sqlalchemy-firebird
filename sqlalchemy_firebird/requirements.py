from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property
    def autoincrement_insert(self):
        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        return exclusions.closed()

    @property
    def duplicate_key_raises_integrity_error(self):
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        """target database supports constraints without an explicit name."""
        return exclusions.open()

    @property
    def indexes_with_ascdesc(self):
        """target database supports CREATE INDEX with column-level ASC/DESC."""
        return exclusions.closed()

    @property
    def temp_table_names(self):
        return exclusions.open()

    @property
    def time_microseconds(self):
        return exclusions.closed()

    @property
    def unicode_data(self):
        # assumes ?charset=UTF8 in connection URI
        return exclusions.open()

    @property
    def unique_constraint_reflection(self):
        # TODO: Research ways to support this in Firebird
        return exclusions.closed()

    @property
    def comment_reflection(self):
        return exclusions.open()
 
    @property
    def tuple_in(self):
        """ Supports queries like:
        SELECT some_table.id FROM some_table
        WHERE (some_table.x, some_table.z) IN ((2, 'z2'), (3, 'z3'), (4, 'z4'))

        Firebird would have to change the query to something like:
        SELECT some_table.id FROM some_table
        WHERE (some_table.x = 2 and some_table.z = 'z2')
           OR (some_table.x = 3 and some_table.z = 'z3')
           OR (some_table.x = 4 and some_table.z = 'z4')
        """
        # TODO: Research ways to support this in Firebird
        return exclusions.closed()
