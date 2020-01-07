from sqlalchemy.dialects import registry
import pytest

registry.register("firebird2", "sqlalchemy_firebird.fdb", "FBDialect_fdb")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
