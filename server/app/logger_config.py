import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler


ROTATINGSIZE = 32 * 1024 * 1024

class ColoredFormatter(logging.Formatter):
    def __init__(self, datefmt: str,  strfmt: str | None = None):
        super(ColoredFormatter, self).__init__()
        self.datefmt = datefmt
        self.strfmt = strfmt or "%(levelname)s %(asctime)s %(message)s"

        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        self.formats = {
            logging.DEBUG: grey + self.strfmt + reset,
            logging.INFO: grey + self.strfmt + reset,
            logging.WARNING: yellow + self.strfmt + reset,
            logging.ERROR: red + self.strfmt + reset,
            logging.CRITICAL: bold_red + self.strfmt + reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

LOGGING_FORMATTERS = {
    "verbose": "%(levelname)s %(asctime)s %(module)s:%(lineno)d %(message)s",
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
    handler.setFormatter(ColoredFormatter(LOGGING_DATE_FMT, fmt))
    logger = logging.getLogger(mod_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
