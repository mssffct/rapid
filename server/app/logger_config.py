import os
import logging
import logging.config

from app.core.types.logger import LoggerHandler, LogLevels

ROTATINGSIZE = 32 * 1024 * 1024

LOGGING_FORMATTERS = {
    "verbose": {
        "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
    },
    "trace": {"format": "%(levelname)s %(asctime)s %(message)s"},
}
LOGGING_HANDLERS = {
    "coreFile": LoggerHandler(
        level=LogLevels.DEBUG,
        formatter="verbose",
        filename="core.log",
        maxBytes=ROTATINGSIZE
    )
}


def setup_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": LOGGING_FORMATTERS,
        "handlers": LOGGING_HANDLERS
    }

    logging.config.dictConfig(log_config)

