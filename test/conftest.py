from sqlalchemy.dialects import registry
import pytest
from sqlalchemy.testing.plugin.pytestplugin import *

registry.register("firebird2", "sqlalchemy_firebird.fdb", "FBDialect_fdb")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")
