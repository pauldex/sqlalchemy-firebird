from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property
    def temp_table_reflection(self):
        """Target database supports CREATE TEMPORARY TABLE."""
        # For now, skip these tests until we see how
        # https://github.com/sqlalchemy/sqlalchemy/issues/5085
        # plays out.
        return exclusions.closed()
