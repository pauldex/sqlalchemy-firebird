from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
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
    def unique_constraint_reflection(self):
        return exclusions.closed()
