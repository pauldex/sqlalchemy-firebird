from pytest.mark import skip
from sqlalchemy.testing.suite import *  # noqa: F401, F403

from sqlalchemy.testing.suite import CTETest as _CTETest

from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest


@skip(reason="These tests fails in Firebird because a DELETE FROM <table> with self-referencing FK raises integrity errors.")
class CTETest(_CTETest):
    pass
