from sqlalchemy.testing.provision import temp_table_keyword_args


@temp_table_keyword_args.for_db("firebird2")
def _firebird_temp_table_keyword_args(cfg, eng):
    return {
        "prefixes": ["GLOBAL TEMPORARY"],
        "firebird2_on_commit": "PRESERVE ROWS",
    }
