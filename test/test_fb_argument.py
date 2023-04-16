from sqlalchemy.testing import engines
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures
from unittest.mock import call
from unittest.mock import Mock


class ArgumentTest(fixtures.TestBase):
    def _dbapi(self):
        return Mock(
            paramstyle="qmark",
            connect=Mock(
                return_value=Mock(
                    server_version="UI-V6.3.2.18118 Firebird 2.1",
                    cursor=Mock(return_value=Mock()),
                )
            ),
        )

    def _engine(self, **kw):
        dbapi = self._dbapi()
        kw.update(dict(module=dbapi, _initialize=False))
        engine = engines.testing_engine("firebird://", options=kw)
        return engine

    def test_retaining_flag_default_fdb(self):
        engine = self._engine()
        self._assert_retaining(engine, False)

    def test_retaining_flag_true_fdb(self):
        engine = self._engine(retaining=True)
        self._assert_retaining(engine, True)

    def test_retaining_flag_false_fdb(self):
        engine = self._engine(retaining=False)
        self._assert_retaining(engine, False)

    def _assert_retaining(self, engine, flag):
        conn = engine.connect()
        trans = conn.begin()
        trans.commit()
        eq_(
            engine.dialect.dbapi.connect.return_value.commit.mock_calls,
            [call(flag)],
        )

        trans = conn.begin()
        trans.rollback()
        eq_(
            engine.dialect.dbapi.connect.return_value.rollback.mock_calls,
            [call(flag)],
        )
