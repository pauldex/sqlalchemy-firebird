from sqlalchemy.dialects import registry
import pytest

# setup default dialect for sqlalchemy
try:
    import firebird.driver  # is firebird-driver available?

    registry.register(
        "firebird", "sqlalchemy_firebird.firebird", "FBDialect_firebird"
    )
except ImportError:
    registry.register("firebird", "sqlalchemy_firebird.fdb", "FBDialect_fdb")

registry.register("firebird.fdb", "sqlalchemy_firebird.fdb", "FBDialect_fdb")
registry.register(
    "firebird.firebird", "sqlalchemy_firebird.firebird", "FBDialect_firebird"
)

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

# this happens after pytest.register_assert_rewrite to avoid pytest warning
from sqlalchemy.testing.plugin.pytestplugin import *  # noqa: F401, E402, F403
