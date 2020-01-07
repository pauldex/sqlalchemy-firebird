# firebird/__init__.py
# Copyright (C) 2005-2019 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

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
# Not supporting kinterbase
# from . import kinterbasdb  # noqa


base.dialect = dialect = fdb.dialect

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
