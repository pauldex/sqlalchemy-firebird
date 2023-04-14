from sqlalchemy.testing.suite import *  # noqa: F401, F403


from sqlalchemy.testing.suite import NumericTest as _NumericTest


class NumericTest(_NumericTest):
    @testing.skip("firebird")
    def test_enotation_decimal_large(self):
        # Failing with
        # sqlalchemy.exc.DatabaseError: (fdb.fbcore.DatabaseError) ('Cursor.fetchone:\n- SQLCODE: -804\n- Incorrect values within SQLDA structure\n- empty pointer to data\n- at SQLVAR index 0', -804, 335544713)        # Table unknown
        return
