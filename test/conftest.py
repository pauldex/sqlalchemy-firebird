from sqlalchemy.dialects import registry
import pytest

registry.register("firebird", "sqlalchemy_firebird.fdb", "FBDialect_fdb")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

# this happens after pytest.register_assert_rewrite to avoid pytest warning
from sqlalchemy.testing.plugin.pytestplugin import *
