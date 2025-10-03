"""Generalized logging utility"""

import logging
from enum import IntEnum

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S"
)

_internal_logger = logging.getLogger("GenAI For Audio")
_internal_logger.setLevel(logging.INFO)


class LogLevels(IntEnum):
    """Logging levels to show trace"""

    OFF = 0
    ON = 1


def log(message, log_level: LogLevels = LogLevels.ON):
    """Generalized custom logger"""
    if log_level > LogLevels.OFF:
        _internal_logger.log(logging.INFO, message)
