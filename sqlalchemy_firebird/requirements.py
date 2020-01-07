from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    pass

    # this will be where we tweak test requirements based on database/dbapi
    # capabilities, e.g.,
    #
    # @property
    # def nullable_booleans(self):
    #     """Target database allows boolean columns to store NULL."""
    #     # Access Yes/No doesn't allow null
    #     return exclusions.closed()
