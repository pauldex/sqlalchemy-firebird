Developer Notes
===================
Fixing Errors
-------------

* **CompoundSelect and DeprecatedCompoundSelect test failures**

    1. Invalid ORDER BY clause
        a. test_distinct_selectable_in_unions
        b. test_limit_offset_aliased_selectable_in_unions
        c. test_plain_union

    In Firebird the ORDER BY for a UNION must be the **column number** instead of the **column name**.

    2. Token unknown '('
        a. test_limit_offset_selectable_in_unions
        b. test_order_by_selectable_in_unions

    Cannot determine how to fix this problem in Firebird yet.
    Example code:

    ::

        (SELECT some_table.id, some_table.x, some_table.y
        FROM some_table
        WHERE some_table.id = 2 ORDER BY some_table.id)
        UNION
        (SELECT some_table.id, some_table.x, some_table.y
        FROM some_table
        WHERE some_table.id = 3 ORDER BY some_table.id)
        ORDER BY some_table.id

* **Collate**
    Investigate

* **DateTimeMicroseconds**
    Investigate

* **Exception**
    Investigate

* **LikeFunctions**
    Investigate

* **LimitOffset**
    Investigate

* **Numeric**
    Investigate

* **Returning**
    Investigate

* **String**
    Investigate

* **TableDDL**
    Investigate

* **Text**
    Investigate

* **TimeMicroseconds**
    Investigate

* **UnicodeText**
    Investigate

* **UnicodeVarchar**
    Investigate
