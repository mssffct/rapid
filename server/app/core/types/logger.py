import dataclasses
import enum


@dataclasses.dataclass
class LoggerHandler:
    level: str
    formatter: str
    filename: str
    maxBytes: int
    backupCount: int = 3
    mode: str = "a"
    encoding: str = "utf-8"



class LogLevels(enum.StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"