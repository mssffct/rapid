import enum


class UserRole(enum.StrEnum):
    DEMO = "D"
    PLAIN_USER = "PU"
    STAFF_ADMIN = "SA"
    LICENSE_ADMIN = "LA"


class AuthType(enum.StrEnum):
    IP = "IP"
    DB = "DB"
    RADIUS = "RADIUS"
    LDAP = "LDAP"


class MFAType(enum.StrEnum):
    TOTP = "TOTP"
