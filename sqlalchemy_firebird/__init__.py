# firebird/__init__.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy.dialects import registry as _registry

from .base import BIGINT
from .base import BLOB
from .base import CHAR
from .base import DATE
from .base import FLOAT
from .base import NUMERIC
from .base import SMALLINT
from .base import TEXT
from .base import TIME
from .base import TIMESTAMP
from .base import VARCHAR
from . import base  # noqa
from . import fdb  # noqa
from . import provision  # noqa

# Not supporting kinterbase
# from . import kinterbasdb  # noqa

__version__ = "0.7.5"

base.dialect = dialect = fdb.dialect

_registry.register("firebird", "sqlalchemy_firebird.fdb", "FBDialect_fdb")

__all__ = (
    "SMALLINT",
    "BIGINT",
    "FLOAT",
    "FLOAT",
    "DATE",
    "TIME",
    "TEXT",
    "NUMERIC",
    "FLOAT",
    "TIMESTAMP",
    "VARCHAR",
    "CHAR",
    "BLOB",
    "dialect",
)
