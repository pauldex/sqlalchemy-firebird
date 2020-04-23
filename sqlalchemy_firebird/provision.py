from sqlalchemy.testing.provision import temp_table_keyword_args


@temp_table_keyword_args.for_db("firebird")
def _firebird_temp_table_keyword_args(cfg, eng):
    return {
        "prefixes": ["GLOBAL TEMPORARY"],
        "firebird_on_commit": "PRESERVE ROWS",
    }
