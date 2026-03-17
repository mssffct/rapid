import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler


ROTATINGSIZE = 32 * 1024 * 1024

LOGGING_FORMATTERS = {
    "verbose": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
    "trace": "%(levelname)s %(asctime)s %(message)s",
}

LOGDIR = os.path.join("logs")

FILEHANDLER_CONFIG = {
    "mode": "a",
    "maxBytes": ROTATINGSIZE,
    "backupCount": 3,
    "encoding": "utf-8",
}

ERRORFILE = "error.log"
COREFILE = "core.log"
AUTHFILE = "auth.log"
GENERALFILE = "general.log"

LOG_HANDLERS = {
    "errorsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + ERRORFILE,
        "formatter": LOGGING_FORMATTERS.get("verbose"),
    },
    "coreLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + COREFILE,
        "formatter": LOGGING_FORMATTERS.get("verbose"),
    },
    "authLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + AUTHFILE,
        "formatter": LOGGING_FORMATTERS.get("verbose"),
    },
    "generalLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + GENERALFILE,
        "formatter": LOGGING_FORMATTERS.get("verbose"),
    },
}

LOGGING_DATE_FMT = "%d-%m-%Y %H:%M:%S"


def get_logger(mod_name: str, level: str = logging.INFO) -> logging.Logger:
    ins = LOG_HANDLERS.get(mod_name)
    fmt = ins.pop("formatter")
    handler = RotatingFileHandler(**ins)
    handler.setFormatter(logging.Formatter(fmt, LOGGING_DATE_FMT))
    logger = logging.getLogger(mod_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
